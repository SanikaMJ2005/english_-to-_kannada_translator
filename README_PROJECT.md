# English → Kannada Translator (Python + Flask)

This small project provides a simple web UI to translate English text to Kannada.

## Features
- Uses `googletrans` if available for better translations.
- Falls back to a tiny built-in dictionary for basic phrases if `googletrans` is not installed.

## Setup
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python app.py
```

Open http://localhost:5000 in your browser.

## Files
- `app.py` – Flask app and translation logic
- `templates/index.html` – Simple web UI
- `requirements.txt` – Python dependencies

If `googletrans` fails or is not installed, the app will use a small fallback dictionary.
