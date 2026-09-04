from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TIMEOUT = 20

HEADERS = {
    "User-Agent": "BrewScope-Monitor/1.0 (educational market-monitoring prototype)"
}

PRICE_RE = re.compile(
    r"(?:₹|Rs\.?\s*)\s?([0-9]{1,4}(?:[,][0-9]{3})?(?:\.[0-9]{1,2})?)"
)

ML_RE = re.compile(
    r"\b([1-9][0-9]{1,3})\s?(?:ml|mL)\b",
    re.I
)


def clean_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    text = " ".join(soup.stripped_strings)
    return re.sub(r"\s+", " ", text)


def extract_signals(html: str, base_url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    text = clean_text(html)

    prices = sorted({
        round(float(x.replace(",", "")), 2)
        for x in PRICE_RE.findall(text)
    })

    headings = []

    for tag in soup.find_all(["h1", "h2", "h3"]):
        t = " ".join(tag.stripped_strings).strip()

        if 4 <= len(t) <= 100:
            headings.append(t)

    links = []

    for a in soup.find_all("a", href=True):
        label = " ".join(a.stripped_strings).strip()
        href = urljoin(base_url, a["href"])

        keywords = [
            "coffee",
            "cold brew",
            "latte",
            "cappuccino",
            "black",
            "mocha",
            "protein",
            "focus",
        ]

        if label and any(k in label.lower() for k in keywords):
            links.append({
                "label": label,
                "href": href
            })

    links = links[:200]

    canonical = text[:400000]

    return {
        "title": (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else ""
        ),
        "h1": headings[:10],
        "prices": prices[:100],
        "product_like_links": links,
        "text_hash": hashlib.sha256(
            canonical.encode("utf-8", "ignore")
        ).hexdigest(),
        "text_excerpt": canonical[:1500],
    }


def load_json(p, default):
    if not p.exists():
        return default

    try:
        return json.loads(
            p.read_text(encoding="utf-8")
        )
    except Exception:
        return default


def classify_change(old: dict | None, new: dict) -> list[dict]:
    if not old:
        return [{
            "type": "new_source_snapshot",
            "detail": "First successful observation recorded."
        }]

    events = []

    if old.get("text_hash") != new.get("text_hash"):
        events.append({
            "type": "page_content_changed",
            "detail": "Source page content changed since previous check."
        })

    old_prices = set(old.get("prices", []))
    new_prices = set(new.get("prices", []))

    added_prices = sorted(new_prices - old_prices)
    removed_prices = sorted(old_prices - new_prices)

    if added_prices:
        events.append({
            "type": "price_signal_added",
            "detail": f"New observed price signals: {added_prices}"
        })

    if removed_prices:
        events.append({
            "type": "price_signal_removed",
            "detail": (
                "Previously observed price signals no longer found: "
                f"{removed_prices}"
            )
        })

    old_links = {
        x["label"]
        for x in old.get("product_like_links", [])
    }

    new_links = {
        x["label"]
        for x in new.get("product_like_links", [])
    }

    for x in sorted(new_links - old_links)[:20]:
        events.append({
            "type": "product_or_link_added",
            "detail": f"New product-like listing/link detected: {x}"
        })

    for x in sorted(old_links - new_links)[:20]:
        events.append({
            "type": "product_or_link_removed",
            "detail": (
                "Previously observed listing/link no longer detected: "
                f"{x}"
            )
        })

    return events


def main():
    sources = load_json(
        DATA / "sources.json",
        []
    )

    state = load_json(
        DATA / "monitor_state.json",
        {}
    )

    changes = load_json(
        DATA / "changes.json",
        []
    )

    checked = datetime.now(timezone.utc).isoformat()

    run_events = []

    for s in sources:
        key = s["url"]

        try:
            r = requests.get(
                s["url"],
                headers=HEADERS,
                timeout=TIMEOUT
            )

            r.raise_for_status()

            sig = extract_signals(
                r.text,
                s["url"]
            )

            sig["checked_at"] = checked
            sig["http_status"] = r.status_code

            events = classify_change(
                state.get(key),
                sig
            )

            if not events:
                events = [{
                    "type": "no_change",
                    "detail": (
                        "No material change detected "
                        "since previous check."
                    )
                }]

            run_events.append({
                "brand": s["brand"],
                "url": s["url"],
                "checked_at": checked,
                "events": events
            })

            state[key] = sig | {
                "brand": s["brand"],
                "kind": s.get("kind", "source")
            }

        except Exception as e:
            run_events.append({
                "brand": s["brand"],
                "url": s["url"],
                "checked_at": checked,
                "events": [{
                    "type": "monitor_error",
                    "detail": str(e)
                }]
            })

    # Keep a rolling 100-event history.
    changes = (run_events + changes)[:100]

    (
        DATA / "monitor_state.json"
    ).write_text(
        json.dumps(
            state,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    (
        DATA / "changes.json"
    ).write_text(
        json.dumps(
            changes,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


if __name__ == "__main__":
    main()
