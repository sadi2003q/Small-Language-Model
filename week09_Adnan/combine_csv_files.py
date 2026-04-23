#!/usr/bin/env python3

from __future__ import annotations

import csv
from pathlib import Path


EXCLUDED_FILENAMES = {"combine_result.csv", "combined_results.csv"}


def get_source_dir() -> Path:
    script_dir = Path(__file__).resolve().parent
    candidate = script_dir.parent / "week09_Adnan_Analysis"
    if candidate.is_dir():
        return candidate
    return script_dir


def get_csv_files(source_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in source_dir.glob("*.csv")
        if path.name not in EXCLUDED_FILENAMES
    )


def collect_fieldnames(csv_files: list[Path]) -> list[str]:
    fieldnames: list[str] = []

    for csv_file in csv_files:
        with csv_file.open("r", newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                continue

            for fieldname in reader.fieldnames:
                if fieldname not in fieldnames:
                    fieldnames.append(fieldname)

    if "source_file" not in fieldnames:
        fieldnames.append("source_file")

    return fieldnames


def combine_csv_files(source_dir: Path, output_file: Path) -> int:
    csv_files = get_csv_files(source_dir)
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {source_dir}")

    fieldnames = collect_fieldnames(csv_files)
    row_count = 0

    with output_file.open("w", newline="", encoding="utf-8") as out_handle:
        writer = csv.DictWriter(out_handle, fieldnames=fieldnames)
        writer.writeheader()

        for csv_file in csv_files:
            with csv_file.open("r", newline="", encoding="utf-8-sig") as in_handle:
                reader = csv.DictReader(in_handle)
                if reader.fieldnames is None:
                    continue

                for row in reader:
                    row["source_file"] = csv_file.name
                    writer.writerow({field: row.get(field, "") for field in fieldnames})
                    row_count += 1

    return row_count


def main() -> None:
    source_dir = get_source_dir()
    output_file = source_dir / "combine_result.csv"
    row_count = combine_csv_files(source_dir, output_file)
    print(f"Combined {row_count} rows into {output_file}")


if __name__ == "__main__":
    main()
