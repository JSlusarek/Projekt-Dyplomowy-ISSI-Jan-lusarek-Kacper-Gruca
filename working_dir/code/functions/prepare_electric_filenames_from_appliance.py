import pandas as pd
import os


def prepare_electric_filenames_from_appliance(folder_path: str) -> pd.DataFrame:
    """
    Extract metadata from filenames of electric appliance Parquet files in a directory.

    This function scans a folder for files whose names contain the keyword 'electric',
    extracts the home ID, electric type, and the appliance name (if present),
    and returns a structured DataFrame with this metadata.

    Parameters
    ----------
    folder_path : str
        Path to the directory containing Parquet sensor files.

    Returns
    -------
    pd.DataFrame
        A DataFrame sorted by 'home_id' and 'electric', containing the following columns:
        - home_id : int
            The numeric ID extracted from the filename (e.g., 'home47' → 47).
        - electric : str
            The first component of the filename that includes the word 'electric'
            (e.g., 'electric-appliance', 'electric-subcircuit').
        - appliance_name : str
            The last part of the filename, used as the appliance name (e.g., 'microwave').
        - filename : str
            The original filename including extension.
    """

    data_to_process = pd.DataFrame()

    for filename in os.listdir(folder_path):

        if "electric" in filename and not filename.startswith("._"):
            parts = filename.split("_")
            parts[-1] = parts[-1].rsplit(".", 1)[0]  # remove .parquet

            home_id = int(parts[0].split("home")[-1])

            electric = next((part for part in parts if "electric" in part), None)

            # # Extract appliance name if applicable
            appliance_name = None
            if "electric" in filename:
                appliance_name = parts[-1]  # Last part is subcircuit name

            row = {
                "home_id": home_id,
                "electric": electric,
                "appliance_name": appliance_name,
                "filename": filename,
            }
            data_to_process = pd.concat([data_to_process, pd.DataFrame([row])], ignore_index=True)
    
    data_to_process = data_to_process.sort_values(by=["home_id", "electric"]).reset_index(drop=True)

    return data_to_process
