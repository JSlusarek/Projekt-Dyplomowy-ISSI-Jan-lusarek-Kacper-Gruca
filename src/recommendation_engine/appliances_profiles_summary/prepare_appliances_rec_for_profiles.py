import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join("../../")))
import pickle
from src.recommendation_engine.recommend_best_device_per_group import recommend_best_per_group
from src.recommendation_engine.comparing_devices import comparing_devices

df = pd.read_parquet("../../../Data/GRID/grid_with_profiles.parquet")
df[df.select_dtypes(include=['float']).columns] = df.select_dtypes(include=['float']).round(1)

# delete balanced profiles
df = df[df["profile"] != "Balanced"]
df.drop(columns=["optimal_score", "unique_parameter",], inplace=True)

unique_profiles = df["profile"].unique()
appliance_recommendations_for_profiles = {}

for profile in unique_profiles:
    appliance_recommendations_for_profiles[profile] = recommend_best_per_group(profile_label=profile, df=df, comparing_dict=comparing_devices)

with open("../../src/recommendation_engine/pickles/appliance_recommendations_for_profiles.pkl", "wb") as f:
    pickle.dump(appliance_recommendations_for_profiles, f)
