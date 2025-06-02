from pathlib import Path
import polars as pl
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# Ustawienia
source_dir = Path("Data/CSV")
target_dir = Path("Data/Parquet")
max_workers = min(6, os.cpu_count() or 4)  # M1: 6 wątków to bezpieczny kompromis

def remove_csv_extensions(path: Path) -> Path:
    if path.suffix == ".gz" and path.stem.endswith(".csv"):
        return path.with_suffix('').with_suffix('')
    return path.with_suffix('')

def convert_csv_to_parquet(source_file: Path):
    try:
        df = pl.read_csv(source_file)
        if df.is_empty():
            print(f"Pusty plik: {source_file}, pomijam.")
            return
        relative_path = source_file.relative_to(source_dir)
        base_path = remove_csv_extensions(relative_path)
        target_file = target_dir / base_path.with_suffix(".parquet")
        target_file.parent.mkdir(parents=True, exist_ok=True)
        df.write_parquet(target_file)
        print(f"✔️ Zapisano: {target_file}")
    except Exception as e:
        print(f"❌ Błąd: {source_file} -> {e}")

def main():
    all_files = [
        f for f in source_dir.rglob("*")
        if f.is_file() and f.name.endswith((".csv", ".csv.gz"))
    ]

    if not all_files:
        print("Brak plików do przetworzenia.")
        return

    print(f"Znaleziono {len(all_files)} plików. Rozpoczynam konwersję...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(convert_csv_to_parquet, f) for f in all_files]
        for future in as_completed(futures):
            future.result()  # Wyłapuje ewentualne wyjątki

if __name__ == "__main__":
    main()
