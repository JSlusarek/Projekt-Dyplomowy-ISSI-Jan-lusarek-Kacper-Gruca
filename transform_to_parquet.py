import os
import polars as pl

source_dir = "Data/CSV"
target_dir = "Data/Parquet"

def remove_csv_extensions(filename):
    if filename.endswith(".csv.gz"):
        return filename[:-7]
    elif filename.endswith(".csv"):
        return filename[:-4]
    elif filename.endswith(".gz"):
        return filename[:-3]
    return filename

for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith(".csv") or file.endswith(".csv.gz"):
            source_file = os.path.join(root, file)
            relative_path = os.path.relpath(source_file, source_dir)

            base_path = remove_csv_extensions(relative_path)
            target_file = base_path + ".parquet"
            final_target_path = os.path.join(target_dir, target_file)

            os.makedirs(os.path.dirname(final_target_path), exist_ok=True)

            try:
                print(f"Próba konwersji: {source_file}")
                df = pl.read_csv(source_file)
                if df.is_empty():
                    print(f"Pusty plik: {source_file}, pomijam.")
                    continue
                df.write_parquet(final_target_path)
                print(f"Zapisano: {final_target_path}")
            except Exception as e:
                print(f"Błąd przy przetwarzaniu pliku {source_file}: {e}")
