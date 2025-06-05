""" 
co2_emission_kg: destymulanta 
cost_pln: destymulanta
normalized_comfort: destymulanta
normalized_failure_rate: destymulanta
device_cost: destymulanta
unique_parameter: stymulanta

Tzn 1 oznacza pierwsze miejsce w sortowaniu od najmniejszej do największej wartości wg wagi,
Moduł z wagi oznacza jej ważność zaś + lub - oznacza czy jest to stymulanta czy destymulanta. 
"""

USER_PROFILES = {
    "EcoFriendly": {
        "co2_emission_kg": 1,                     # zawsze 1
        "cost_pln": [2, 3, 4, 5, 6],
        "normalized_comfort": [2, 3, 4, 5, 6],
        "normalized_failure_rate": [2, 3, 4, 5, 6],
        "device_cost": [2, 3, 4, 5, 6],
        "unique_parameter": [2, 3, 4, 5, 6]
    },
    "Saver": {
        "co2_emission_kg": [2, 3, 4, 5, 6],
        "cost_pln": 1,                            # zawsze 1
        "normalized_comfort": [2, 3, 4, 5, 6],
        "normalized_failure_rate": [2, 3, 4, 5, 6],
        "device_cost": [2, 3, 4, 5, 6],
        "unique_parameter": [2, 3, 4, 5, 6]
    },
    "ComfortSeeker": {
        "co2_emission_kg": [2, 3, 4, 5, 6],
        "cost_pln": [2, 3, 4, 5, 6],
        "normalized_comfort": 1,                  # zawsze 1
        "normalized_failure_rate": [2, 3, 4, 5, 6],
        "device_cost": [2, 3, 4, 5, 6],
        "unique_parameter": [2, 3, 4, 5, 6]
    },
    "Balanced": {
        "co2_emission_kg": [1, 2, 3, 4, 5, 6],
        "cost_pln": [1, 2, 3, 4, 5, 6],
        "normalized_comfort": [1, 2, 3, 4, 5, 6],
        "normalized_failure_rate": [1, 2, 3, 4, 5, 6],
        "device_cost": [1, 2, 3, 4, 5, 6],
        "unique_parameter": [1, 2, 3, 4, 5, 6]
    },
    "QualitySeeker": {
        "co2_emission_kg": [1, 2, 3, 4, 6],
        "cost_pln": [1, 2, 3, 4, 6],
        "normalized_comfort": [1, 2, 3, 4, 6],
        "normalized_failure_rate": [1, 2, 3, 4, 6],
        "device_cost": [1, 2, 3, 4, 6],
        "unique_parameter": 5                     # zawsze 5
    },
    "Budget": {
        "co2_emission_kg": [2, 3, 4, 5, 6],
        "cost_pln": [2, 3, 4, 5, 6],
        "normalized_comfort": [2, 3, 4, 5, 6],
        "normalized_failure_rate": [2, 3, 4, 5, 6],
        "device_cost": 1,                         # zawsze 1
        "unique_parameter": [2, 3, 4, 5, 6]
    },
    "RiskAware": {
        "co2_emission_kg": [2, 3, 4, 5, 6],
        "cost_pln": [2, 3, 4, 5, 6],
        "normalized_comfort": [2, 3, 4, 5, 6],
        "normalized_failure_rate": 1,             # zawsze 1
        "device_cost": [2, 3, 4, 5, 6],
        "unique_parameter": [2, 3, 4, 5, 6]
    }
}
