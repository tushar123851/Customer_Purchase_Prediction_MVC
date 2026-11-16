"""Generate a reproducible synthetic customer purchase dataset."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "customer_data.csv"

def main():
    rng = np.random.default_rng(42)
    n = 5000

    age = rng.integers(18, 66, n)
    annual_income = rng.integers(150_000, 1_500_001, n)
    website_visits = rng.integers(1, 51, n)
    previous_purchases = rng.integers(0, 31, n)
    time_on_website = rng.integers(1, 61, n)
    discount_offered = rng.integers(0, 51, n)

    score = (
        -3.0
        + website_visits * 0.07
        + previous_purchases * 0.10
        + time_on_website * 0.025
        + discount_offered * 0.035
        + (annual_income / 1_000_000) * 0.15
        - age * 0.005
    )
    probability = 1 / (1 + np.exp(-score))
    purchase = rng.binomial(1, probability)

    df = pd.DataFrame({
        "Age": age,
        "Annual_Income": annual_income,
        "Website_Visits": website_visits,
        "Previous_Purchases": previous_purchases,
        "Time_On_Website": time_on_website,
        "Discount_Offered": discount_offered,
        "Purchase": purchase,
    })
    df.to_csv(OUTPUT, index=False)
    print(f"Dataset created: {OUTPUT}")
    print(f"Shape: {df.shape}")
    print("\nTarget distribution:")
    print(df["Purchase"].value_counts().sort_index())

if __name__ == "__main__":
    main()
