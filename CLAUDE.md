# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

A collection of standalone code samples across multiple languages (Python, C, C++, C#) and domains (web scraping, OCR, finance, web serving, deployment infrastructure, algorithms). Components are independent — no runtime dependencies between them.

## Architecture

### Python scripts (root level)
- `hi_world.py` — Interactive CLI greeting with argparse, time-aware messages, multi-language support (en/es/fr/de/pt)
- `fetch_etfs.py` — Selenium headless Chrome scraper for justETF.com, outputs CSV via Pandas
- `google_finance_demo.py` — Selenium scraper for Google Finance exchange rates
- `OCRDemo.py` — Tesseract OCR demo using pytesseract + Pillow

`fetch_etfs.py` and `google_finance_demo.py` share duplicated Selenium boilerplate (Chrome options setup, driver init, cleanup). Changes to one should be evaluated for the other.

### Algorithm implementations (count_pairs)
Same two-pointer pair-counting algorithm in three languages for comparison:
- `count_pairs.c` — Pure C with qsort, malloc/free
- `count_pairs.cpp` — C++ with std::vector, std::sort, `<bits/stdc++.h>` (GCC-only)
- `CountPairs.cs` — C# with Array.Sort, BCL only

All use `n * (n - 1) / 2` which overflows int32 when n > ~65536.

### Flask demo (`flask-demo/`)
Single-route Flask app with Jinja2 template and CSS (glassmorphism, gradients). Runs on `0.0.0.0:5000`.

### Chatwoot deployment (`chatwoot-deployment/`)
Docker Swarm infrastructure for Chatwoot (customer engagement platform):
- `chatwoot-stack.yml` — App + Sidekiq worker services, Traefik labels, 20+ shared env vars
- `postgres-stack.yml` — PostgreSQL (pgvector:pg17) with volume
- `.env.example` — Secret template (must be copied to `.env` before deploying)
- `deployment_instructions.md` — Step-by-step guide (in Spanish)

**Known deployment gaps:** Redis service is referenced but not defined in any stack file. `POSTGRES_DB` is not set in postgres-stack.yml but Chatwoot expects database `caciopea`. PostgreSQL port 5432 is unnecessarily exposed to the host.

### AI-agents (`AI-agents/`)
Separate git repository (not declared as submodule). Contains `templates/ai-agent-briefing.md` — a project scoping template in Spanish.

## Commands

No unified build system. Each component runs independently:

```bash
# Python scripts
python hi_world.py --lang es --name Carlos --banner --time
python fetch_etfs.py          # requires: selenium, webdriver-manager, pandas, Chrome
python google_finance_demo.py # requires: selenium, webdriver-manager, Chrome
python OCRDemo.py             # requires: pytesseract, Pillow, Tesseract binary on PATH

# Flask demo
cd flask-demo && python app.py  # requires: flask

# C
gcc count_pairs.c -o count_pairs && echo "5 2\n1 3 5 7 9" | ./count_pairs

# C++
g++ count_pairs.cpp -o count_pairs && echo "5 2\n1 3 5 7 9" | ./count_pairs

# C#
csc CountPairs.cs && echo "5 2\n1 3 5 7 9" | ./CountPairs

# Docker Swarm deployment
cd chatwoot-deployment
cp .env.example .env  # fill in real secrets
docker stack deploy -c postgres-stack.yml db
docker stack deploy -c chatwoot-stack.yml chatwoot
```

## Key Conventions

- No requirements.txt or pyproject.toml exists — Python dependencies are implicit
- No root `.gitignore` — `.env` files and `__pycache__/` are not excluded
- The chatwoot stack files use `${VARIABLE}` interpolation from `.env` for secrets, but hardcode non-secret config (domain, email, bucket)
- `chatwoot_app` and `chatwoot_worker` share 20+ identical environment variables (should use YAML anchors)
