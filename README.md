# PaisaPilot — Phase 1 starter

A beginner-friendly personal finance tracker prototype built with Python, Flask, SQLite, HTML, CSS and JavaScript.

## Features
- Add income and expense transactions
- View income, expenses and net balance
- Delete transactions
- English, Gujarati and Hindi interface labels
- SQLite database created automatically

## Requirements
- Python 3.10 or newer
- Visual Studio Code
- Internet connection for the first Flask installation

## Run on Windows (PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## Run on macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Project structure
```text
PaisaPilot/
├── app.py
├── requirements.txt
├── README.md
├── paisapilot.db       # created automatically on first run
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/script.js
```

## Important
This is a learning prototype, not production financial software. It has no user accounts, authentication, CSRF protection, encrypted backups, or multi-user isolation. Use fictional/sample transactions only. Do not enter bank passwords, card details, OTPs, or sensitive financial records. Before real users use it, add security controls and obtain a professional security review.
