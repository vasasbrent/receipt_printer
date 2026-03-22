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

**Data flow:** Frontend collects `theme` + `message` + optional `sender_name` → POSTs JSON to Flask `/print` → Flask extracts sender IP and parses User-Agent (OS/browser), then calls an external print script via `subprocess` → print script uses `python-escpos` to send ESC/POS commands to the printer at `192.168.1.178`.

**Note:** `printer_testing.py` is for direct ad-hoc testing. `print_script.py` is the script invoked by the backend — it accepts `theme`, `message`, `sender_name`, `ip`, and `device_info` as CLI args and sends the job to the printer.

## Running

```bash
# Run backend (dev mode) — uv manages the venv and dependencies automatically
uv run --with flask --with flask_limiter site/back/backend.py          # serves on 0.0.0.0:8000

# Production
# --chdir avoids a conflict with Python's built-in 'site' module
uv run --with gunicorn gunicorn --chdir site/back -w 4 -b 0.0.0.0:8000 'backend:receipt_backend_app'

# Test printer directly (requires printer on local network)
uv run --with escpos print/printer_testing.py
```

## Key details

- Rate limiting: 3 requests/minute per IP on `/print`, 10/min global fallback (via `flask-limiter`)
- Printer profile: `TM-T88V`, local IP `192.168.1.178`, port 9100 (ESC/POS default)
- Three themes — `note`, `memo`, `poem` — each renders a different ASCII art header on the receipt
- Message max length: 512 characters (enforced in the frontend `textarea`)
- Reference PDFs for the printer (user manual + technical reference) are in `reference/`
