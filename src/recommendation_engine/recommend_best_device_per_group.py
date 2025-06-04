import pandas as pd


def rank_all_devices_by_profile(profile_label: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Zwraca ranking urządzeń (liczba wygranych) dla danego profilu.
    """
    filtered = df[df["profile"] == profile_label]
    device_counts = (
        filtered["optimal_device"]
        .value_counts()
        .reset_index()
    )
    return device_counts

def recommend_best_per_group(profile_label: str, df: pd.DataFrame, comparing_dict: dict) -> dict:
    """
    Dla danego profilu wybiera najlepsze urządzenie z każdej zdefiniowanej grupy porównawczej.
    
    Zwraca słownik: {grupa: najlepsze_urzadzenie}
    """
    ranked = rank_all_devices_by_profile(profile_label, df)
    ranked_dict = dict(zip(ranked["optimal_device"], ranked["count"]))

    best_per_group = {}
    for group_name, devices in comparing_dict.items():
        best_device = None
        best_score = -1
        for device in devices:
            if ranked_dict.get(device, 0) > best_score:
                best_device = device
                best_score = ranked_dict.get(device, 0)
        best_per_group[group_name] = best_device
    return best_per_group
