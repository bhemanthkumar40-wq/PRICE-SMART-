# SmartPrice AI – Dynamic Pricing Engine

A beginner-friendly, mobile-responsive AI pricing mini project built with Flask and Scikit-learn.

## Features
- Product price recommendation from demand, stock, competitor price and sales per day.
- Random Forest Regression model trained on generated demo data.
- Price increase/decrease/steady recommendation and explanation.
- Recent recommendation history stored locally in JSON.
- Responsive dashboard for phones and desktops.

## Requirements
- Python 3.10 or newer
- Internet connection for installing Python packages

## Run on Windows 10 / 11

1. Extract the ZIP folder.
2. Open Windows Terminal in the `smartprice-ai` folder.
3. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run this once in the current terminal:
   `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
   Then activate again.

4. Install dependencies:

   ```powershell
   py -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   py app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

To open it on another device on the same Wi-Fi, run `py app.py` after changing the final line to:
`app.run(host="0.0.0.0", port=5000, debug=True)`
Then visit `http://YOUR-COMPUTER-IP:5000` on your phone. Both devices must use the same Wi-Fi.

## Deploy free/low-cost on Render

1. Create a GitHub repository and upload all project files (keep the folder structure).
2. Sign in to Render and choose **New + → Web Service**.
3. Connect your GitHub repository.
4. Render detects `render.yaml`, or enter:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Choose an available plan and click **Deploy**.
6. Open the generated `https://....onrender.com` URL.

Note: free hosting availability and limits can change. The demo history uses a local JSON file; on ephemeral hosting it may reset after redeploy/restart. For a persistent production version, connect a database such as PostgreSQL.

## How the model works
The app generates a reproducible sample dataset and trains a Random Forest Regressor when the server starts. It learns a relationship between base price, demand, stock, competitor price, sales velocity and an example target price. The prediction is capped between 70% and 130% of the current price.

This is a learning demonstration, not a production pricing system. The training data is synthetic, and the app does not connect to live competitors, customer records or real sales feeds. Validate pricing decisions before using them commercially.

## Project structure

```text
smartprice-ai/
├── app.py
├── pricing_model.py
├── requirements.txt
├── Procfile
├── render.yaml
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## Suggested resume entry
**SmartPrice AI – Dynamic Pricing Engine**
- Built a responsive dynamic pricing web application using Python, Flask and Scikit-learn.
- Trained a Random Forest Regression model on generated sample data to estimate product prices using demand, inventory, competitor price and sales velocity.
- Developed an interactive dashboard with price recommendations, decision explanations and pricing history.
