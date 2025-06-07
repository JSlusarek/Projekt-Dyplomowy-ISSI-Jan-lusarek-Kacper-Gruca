import sys
import os
sys.path.append(os.path.abspath(os.path.join("../../")))
import pandas as pd
from src.recommendation_engine.recommend_best_device_per_group import recommend_best_per_group
from src.recommendation_engine.comparing_devices import comparing_devices
from src.comparisons.household import Kitchen, Bathroom, Room


df_water_boiling = Kitchen.compare_water_boiling_devices(liters=1.5)
df_cooking = Kitchen.compare_cooking_devices(time_minutes=30)
df_heating = Kitchen.compare_heating_devices(time_minutes=30)
df_coffee = Kitchen.compare_coffee_devices(cups=1)
df_robots = Kitchen.compare_multicookers(recipe_complexity=1.5)
df_heaters = Bathroom.compare_water_heaters(liters=50)
df_bath = Bathroom.compare_bathing_options()
df_air_heating = Bathroom.compare_bathroom_heating()
df_work = Room.compare_workstations()
df_cooling = Room.compare_cooling_devices(duration_min=60)

chosen_columns = ["name", "energy_kwh", "cost_pln", "time_min", "co2_emission_kg", "device_cost"]

dfs_with_keys = [
    (df_water_boiling, 'boiling_water'),
    (df_cooking, 'cooking'),
    (df_heating, 'heating_food'),
    (df_coffee, 'making_coffee'),
    (df_robots, 'multicookers'),
    (df_heaters, 'water_heating'),
    (df_bath, 'bathing'),
    (df_air_heating, 'bathroom_heating'),
    (df_work, 'workstation'),
    (df_cooling, 'cooling')
]

combined_df = pd.concat([
    df[chosen_columns].assign(category=key) for df, key in dfs_with_keys
], ignore_index=True)

combined_df["time_min"] = round(combined_df["time_min"], 2)
combined_df["energy_kwh"] = round(combined_df["energy_kwh"], 2)
combined_df["co2_emission_kg"] = round(combined_df["co2_emission_kg"], 2)
