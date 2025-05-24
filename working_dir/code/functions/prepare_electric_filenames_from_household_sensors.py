import os
import pandas as pd


def prepare_electric_filenames_from_household_sensors(folder_path: str) -> pd.DataFrame:
    """
    Collect metadata from 'electric' sensor files in a given folder.

    This function scans a directory for Parquet files with 'electric' in the filename,
    extracts the home ID, electric tag (e.g. 'electric-mains_electric-combined'),
    and the subcircuit name (if applicable, e.g. 'shower' from 'electric-subcircuit_shower').

    Parameters
    ----------
    folder_path : str
        Path to the directory containing Parquet sensor files.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the following columns:
        - home_id : int
        - electric : str
        - subcircuit : str or None
        - filename : str
    """
    data_to_process = pd.DataFrame()

    for filename in os.listdir(folder_path):
        if "electric" in filename and not filename.startswith("._"):
            parts = filename.split("_")
            parts[-1] = parts[-1].rsplit(".", 1)[0]  # remove .parquet

            home_id = int(parts[0].split("home")[-1])

            # Join all parts containing "electric" into a single string
            electric = "_".join(part for part in parts if "electric" in part)

            # Extract subcircuit name if applicable
            subcircuit = None
            if "electric-subcircuit" in filename:
                subcircuit = parts[-1]  # Last part is subcircuit name

            row = {
                "home_id": home_id,
                "electric": electric,
                "subcircuit": subcircuit,
                "filename": filename,
            }
            data_to_process = pd.concat([data_to_process, pd.DataFrame([row])], ignore_index=True)
    
    data_to_process = data_to_process.sort_values(by=["home_id", "electric"]).reset_index(drop=True)

    return data_to_process
