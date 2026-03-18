# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A web app where users submit a themed message that gets printed on an Epson TM-T88V thermal receipt printer over the local network.

## Architecture

```
site/front/          # Static frontend (no build step)
  index.html         # Theme selector + receipt UI + textarea
  script.js          # Theme switching, ASCII headers, submit handler
  style.css          # Receipt-styled UI

site/back/
  backend.py         # Flask API server — single POST /print endpoint
  tmp.py             # Scratch/reference snippet (not a running server)

print/
  printer_testing.py # Direct printer test script using python-escpos
```

**Data flow:** Frontend collects `theme` + `message` → POSTs JSON to Flask `/print` → Flask calls an external print script via `subprocess` → print script uses `python-escpos` to send ESC/POS commands to the printer at `192.168.1.178`.

**Note:** `printer_testing.py` is for direct ad-hoc testing. `print_script.py` is the script invoked by the backend — it accepts `theme` and `message` as CLI args and sends the job to the printer.

**Note:** The frontend submit button currently only logs to the console — the `fetch`/POST call to the backend has not been wired up yet.

## Running

```bash
# Activate venv
source .venv/bin/activate

# Install dependencies (Flask + limiter + ESC/POS library)
pip install flask flask-limiter python-escpos

# Run backend (dev mode)
python site/back/backend.py          # serves on 0.0.0.0:8000

# Production
gunicorn -w 4 -b 0.0.0.0:8000 'site.back.backend:receipt_backend_app'

# Test printer directly (requires printer on local network)
python print/printer_testing.py
```

## Key details

- Rate limiting: 3 requests/minute per IP on `/print`, 10/min global fallback (via `flask-limiter`)
- Printer profile: `TM-T88V`, local IP `192.168.1.178`, port 9100 (ESC/POS default)
- Three themes — `note`, `memo`, `poem` — each renders a different ASCII art header on the receipt
- Message max length: 512 characters (enforced in the frontend `textarea`)
- Reference PDFs for the printer (user manual + technical reference) are in `reference/`
