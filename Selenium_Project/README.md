# Selenium_Project — starter

Quick steps to set up a virtual environment, install dependencies, and run the starter Selenium script on Windows PowerShell.

1. Create and activate a venv (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install --upgrade pip; pip install -r requirements.txt
```

3. Run the starter script (headless):

```powershell
python Selenium.py --url https://ohsnapmacros.com/ --headless
```

4. If you want to see the browser UI for debugging, run:

```powershell
python Selenium.py --url https://ohsnapmacros.com/ --no-headless
```

Notes:

- The script uses webdriver-manager to auto-download the matching ChromeDriver. Make sure Google Chrome is installed. If you prefer Firefox, I can add a Gecko driver variant.
- The script will save a screenshot to `./screenshots/`.
