"""
Train a Random Forest pipeline: Season + Crop + Area -> Yield (Production / Area).
Saves model.pkl and crop_season_meta.json for season/crop recommendation in the web app.
"""

import json
from pathlib import Path
import numpy as np

import pandas as pd
import pickle
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent
DATA_CSV = BASE_DIR / "dataset.csv"
if not DATA_CSV.exists():
    DATA_CSV = BASE_DIR / "crop_yield.csv"

MODEL_PATH = BASE_DIR / "model.pkl"
META_PATH = BASE_DIR / "crop_season_meta.json"


def main() -> None:
    df = pd.read_csv(DATA_CSV)
  
    def assign_conditions(crop):
        crop = crop.lower()

        if "rice" in crop:
            return 80, 30, 70   # wet
        elif "maize" in crop or "sugarcane" in crop:
            return 50, 28, 60   # medium
        elif "bajra" in crop or "millet" in crop:
            return 20, 35, 40   # dry
        else:
            return 40, 30, 50   # default

    df[["Soil_Moisture", "Temperature", "Humidity"]] = df["Crop"].apply(
    lambda c: pd.Series(assign_conditions(c))
        ) # in percentage

    required = {"Production", "Area", "Season", "Crop"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing columns: {sorted(missing)}")

    df = df.copy()
    df["Season"] = df["Season"].astype(str).str.strip()
    df["Crop"] = df["Crop"].astype(str).str.strip()
    df["Yield"] = df["Production"] / df["Area"]
    df = df[df["Area"] > 0].dropna(subset=["Production", "Area", "Season", "Crop"])


    X = df[["Season", "Crop", "Area", "Soil_Moisture", "Temperature", "Humidity"]]
    y = df["Production"]

    preprocess = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                ["Season", "Crop"],
            ),
        ],
        remainder="passthrough",
    )

    pipeline = Pipeline(
        steps=[
            ("prep", preprocess),
            (
                "rf",
                RandomForestRegressor(
                    n_estimators=100,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )
    pipeline.fit(X, y)

    seasons = sorted(df["Season"].unique().tolist())
    crops_by_season = {
        s: sorted(df.loc[df["Season"] == s, "Crop"].unique().tolist())
        for s in seasons
    }

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {"seasons": seasons, "crops_by_season": crops_by_season},
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Trained on {len(df)} rows from {DATA_CSV.name}")
    print(f"Features: Season, Crop, Area, Soil_Moisture, Temperature, Humidity")
    print(f"Saved pipeline to {MODEL_PATH}")
    print(f"Saved season/crop lists to {META_PATH}")


if __name__ == "__main__":
    main()
