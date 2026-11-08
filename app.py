from flask import Flask, render_template, request, jsonify
from pricing_model import PricingModel
from datetime import datetime
import json
from pathlib import Path

app = Flask(__name__)
model = PricingModel()
DATA_FILE = Path("price_history.json")

def read_history():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []

def save_history(record):
    history = read_history()
    history.insert(0, record)
    DATA_FILE.write_text(json.dumps(history[:100], indent=2), encoding="utf-8")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    try:
        product = str(data.get("product", "Product")).strip()[:60] or "Product"
        base_price = float(data["base_price"])
        demand = float(data["demand"])
        stock = float(data["stock"])
        competitor_price = float(data["competitor_price"])
        sales_velocity = float(data["sales_velocity"])

        if not (1 <= base_price <= 1000000):
            raise ValueError("Base price must be between 1 and 1,000,000.")
        if not (0 <= demand <= 100):
            raise ValueError("Demand must be between 0 and 100.")
        if not (0 <= stock <= 10000):
            raise ValueError("Stock must be between 0 and 10,000.")
        if not (1 <= competitor_price <= 1000000):
            raise ValueError("Competitor price must be between 1 and 1,000,000.")
        if not (0 <= sales_velocity <= 1000):
            raise ValueError("Sales per day must be between 0 and 1,000.")

        recommended = model.predict(base_price, demand, stock, competitor_price, sales_velocity)
        recommended = round(max(base_price * 0.70, min(base_price * 1.30, recommended)), 2)
        change = round(((recommended - base_price) / base_price) * 100, 1)

        if change > 1:
            decision = "Increase price"
            reason = "Demand and sales activity support a higher price."
        elif change < -1:
            decision = "Decrease price"
            reason = "Current stock or market competition suggests a lower price."
        else:
            decision = "Keep price steady"
            reason = "The model recommends staying close to the current price."

        record = {
            "product": product,
            "base_price": base_price,
            "recommended_price": recommended,
            "change": change,
            "decision": decision,
            "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p")
        }
        save_history(record)
        return jsonify({
            **record,
            "reason": reason,
            "model": "Random Forest Regressor",
            "disclaimer": "Educational estimate. Review prices before applying them."
        })
    except (KeyError, TypeError, ValueError) as error:
        return jsonify({"error": str(error) or "Please enter valid values."}), 400

@app.route("/api/history")
def history():
    return jsonify(read_history())

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
