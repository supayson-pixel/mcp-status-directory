# MCP Status — health-ranked MCP server directory

Live: https://mcp-status-directory.netlify.app

Plain static site (no build step) ranking Model Context Protocol servers by a dated, evidence-based **health score**, flagging archived/stale projects — the gap left by the official MCP Registry, Glama, Smithery, PulseMCP, mcp.so and awesome lists.

## Contents
- `index.html` — all servers ranked by health; anchors `/#owner-repo`
- `category/*.html` — 9 use-case pages
- `status.html`, `methodology.html`, `submit.html`, `thanks.html`
- `data/servers.json` — raw data (CORS open)
- `llms.txt`, `robots.txt`, `sitemap.xml`, JSON-LD — SEO / chatbot discoverability
- Newsletter via Netlify Forms (`data-netlify="true"`)
- `gen.py` — regenerates every page from the data table

## Data (check of 2026-10-15T06:50Z)
73 servers: 28 Healthy, 40 Stale, 5 Archived. Sources: GitHub search API and direct npm/PyPI lookups (6 packages verified; others marked unchecked). No data is invented.

## Score (0–100)
Repo exists 25 · not archived 20 · last push ≤30d 25 / ≤90d 15 / ≤365d 5 · verified package 20 · stars round(10·log10(stars)/5). Healthy ≥75, Stale 40–74, Broken <40; archived repos always labelled Archived.
