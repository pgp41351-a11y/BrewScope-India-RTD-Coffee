# BrewScope — India RTD Coffee Market & Idea Gap Monitor

## What this is
A GitHub-ready Topic 3 project for an AMS capstone. The frontend is a simple India-only RTD coffee dashboard. The monitoring layer runs separately on a schedule using GitHub Actions.

## Architecture
- `index.html` — GitHub Pages frontend
- `data/current.json` — current verified market dataset + working hypothesis
- `data/changes.json` — competitor/source change history
- `data/sources.json` — monitored Indian/brand URLs
- `scripts/monitor.py` — scheduled fetch + change detection
- `.github/workflows/monitor.yml` — daily automated run

## What the monitor detects
- source page content changes
- new / removed observed price signals
- new / removed product-like links
- source failures

This is a conservative page-change monitor. It does **not** claim perfect semantic understanding of every retailer page. A detected change should be reviewed before being treated as a confirmed competitor move.

## Deployment
1. Create a new GitHub repository.
2. Upload all files in this folder.
3. In Settings → Pages, deploy from the `main` branch root.
4. In Actions, enable workflows if prompted.
5. Run **BrewScope Market Monitor** manually once.
6. The scheduled workflow then runs daily at 06:17 UTC and commits updated monitoring state.

GitHub Actions schedule timing can be delayed by GitHub. The monitor should therefore be described as scheduled, not real-time.

## Academic positioning
Topic 3 requires a small functional web app that watches a real category, tracks competitors, surfaces plausible gaps, and reasons through the opportunity rather than only listing scraped data. The project therefore separates:
1. observed market evidence,
2. change signals,
3. gap interpretation,
4. managerial recommendation.

## Current working opportunity
Sleepy Owl Study / Work Focus Latte — 200 ml, ₹59–₹79, ₹79 ceiling, coffee-first, moderate measured caffeine, controlled sugar, late-night study/work occasion.

## Important limitation
The monitored sources include brand pages and category/product pages. Retailer pages can use dynamic rendering or anti-bot controls, so not every future change will necessarily be captured. A source-level change must be reviewed before it becomes a strategic conclusion.
