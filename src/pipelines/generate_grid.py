import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join("../../")))

from src.comparisons.household import Kitchen, Bathroom, Room
from src.comparisons.grid import compute_all_combinations_parallel

def main():
    output_dir = Path("../../Data/GRID")
    output_dir.mkdir(parents=True, exist_ok=True)

    df_cooking = Kitchen.compare_cooking_devices(time_minutes=30)
    df_heating = Kitchen.compare_heating_devices(time_minutes=30)
    df_coffee = Kitchen.compare_coffee_devices(cups=1)
    df_robots = Kitchen.compare_multicookers(recipe_complexity=1.5)
    df_heaters = Bathroom.compare_water_heaters(liters=50)
    df_bath = Bathroom.compare_bathing_options()
    df_air_heating = Bathroom.compare_bathroom_heating()
    df_work = Room.compare_workstations()
    df_cooling = Room.compare_cooling_devices(duration_min=60)

    locals_dfs = {
        "df_cooking": df_cooking,
        "df_heating": df_heating,
        "df_coffee": df_coffee,
        "df_robots": df_robots,
        "df_heaters": df_heaters,
        "df_bath": df_bath,
        "df_air_heating": df_air_heating,
        "df_work": df_work,
        "df_cooling": df_cooling
    }

    datasets = [
        ("cooking", "df_cooking", [
            "cost_pln", "co2_emission_kg", "normalized_comfort", "normalized_failure_rate", "device_cost"
        ]),
        ("heating", "df_heating", [
            "cost_pln", "co2_emission_kg", "normalized_comfort", "normalized_failure_rate", "device_cost", "heating_quality"
        ]),
        ("coffee", "df_coffee", [
            "cost_pln", "co2_emission_kg", "normalized_comfort", "normalized_failure_rate", "device_cost"
        ]),
        ("robots", "df_robots", [
            "cost_pln", "co2_emission_kg", "normalized_comfort", "normalized_failure_rate", "device_cost", "cooking_quality"
        ]),
        ("heaters", "df_heaters", [
            "cost_pln", "co2_emission_kg", "normalized_comfort", "normalized_failure_rate", "device_cost"
        ]),
        ("bath", "df_bath", [
            "cost_pln", "co2_emission_kg", "normalized_comfort", "normalized_failure_rate", "device_cost"
        ]),
        ("air_heating", "df_air_heating", [
            "cost_pln", "co2_emission_kg", "normalized_comfort", "normalized_failure_rate", "device_cost", "heating_quality"
        ]),
        ("work", "df_work", [
            "cost_pln", "co2_emission_kg", "normalized_comfort", "normalized_failure_rate", "device_cost", "computing_quality"
        ]),
        ("cooling", "df_cooling", [
            "cost_pln", "co2_emission_kg", "normalized_comfort", "normalized_failure_rate", "device_cost", "cooling_quality"
        ]),
    ]

    for name, df_varname, features in datasets:
        try:
            df = locals_dfs[df_varname]
            print(f"🔍 Generowanie siatki wag dla: {name}...")
            results = compute_all_combinations_parallel(df, features, step=1, n_jobs=-1)
            results.to_parquet(output_dir / f"{name}_grid.parquet", index=False)
            print(f"Zapisano: {name}_grid.parquet")
        except KeyError:
            print(f"{df_varname} nie istnieje. Pomijam.")
        except Exception as e:
            print(f"Błąd dla {name}: {e}")

if __name__ == "__main__":
    main()
