# time_to_goal_demo.py
"""
Portfolio demo: Time-to-Goal Fitness
Predicts number of days to reach a target weight using simple ML models.
This is a safe, simplified version for demonstration purposes.
"""

from flask import Flask, request, jsonify
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# === DEMO SYNTHETIC DATA ===
# days vs weight (very simple trend for demo purposes)
days = np.arange(0, 30).reshape(-1, 1)
weights = 90 - 0.3 * days + np.random.normal(0, 0.2, size=len(days))
model = LinearRegression().fit(days, weights)


# === ROUTES ===
@app.route("/")
def index():
    return jsonify({"message": "Welcome to Time-to-Goal Fitness demo!"})


@app.route("/predict", methods=["POST"])
def predict_days():
    """
    Example request:
    curl -X POST http://127.0.0.1:5001/predict \
         -H "Content-Type: application/json" \
         -d '{"goal_weight": 75}'
    """
    data = request.get_json()
    if not data or "goal_weight" not in data:
        return jsonify({"error": "Missing goal_weight"}), 400

    goal_weight = float(data["goal_weight"])

    # DEMO prediction using simple linear regression
    pred_days = (goal_weight - model.intercept_) / model.coef_[0]
    pred_days = round(float(pred_days), 1)

    return jsonify({
        "goal_weight": goal_weight,
        "predicted_days": pred_days,
        "note": "Demo prediction only – full ML pipeline available on request."
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
