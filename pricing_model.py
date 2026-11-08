import numpy as np
from sklearn.ensemble import RandomForestRegressor

class PricingModel:
    """Trains a small demo model on generated example pricing data."""

    def __init__(self):
        rng = np.random.default_rng(42)
        rows = 2500
        base = rng.uniform(100, 5000, rows)
        demand = rng.uniform(0, 100, rows)
        stock = rng.uniform(0, 500, rows)
        competitor = base * rng.uniform(0.75, 1.25, rows)
        velocity = rng.uniform(0, 80, rows)

        demand_factor = (demand - 50) / 100
        stock_factor = (100 - np.minimum(stock, 100)) / 500
        competitor_factor = (competitor - base) / np.maximum(base, 1)
        sales_factor = (velocity - 20) / 200

        target = base * (
            1 + 0.22 * demand_factor
              + 0.12 * stock_factor
              + 0.20 * competitor_factor
              + 0.10 * sales_factor
        )
        target += rng.normal(0, base * 0.025, rows)
        target = np.maximum(target, base * 0.70)

        self.model = RandomForestRegressor(
            n_estimators=100, max_depth=12, random_state=42, n_jobs=-1
        )
        X = np.column_stack([base, demand, stock, competitor, velocity])
        self.model.fit(X, target)

    def predict(self, base_price, demand, stock, competitor_price, sales_velocity):
        features = np.array([[
            base_price, demand, stock, competitor_price, sales_velocity
        ]])
        return float(self.model.predict(features)[0])
