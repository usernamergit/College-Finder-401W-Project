#!/usr/bin/env python3
"""Build a safe MySQL load package for one historical Field of Study CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

NEW_ENGLAND = {"CT", "ME", "MA", "NH", "RI", "VT"}
NULL_MARKERS = {"", "NA", "NULL", "PrivacySuppressed", "PS"}

PROGRAM_COLUMNS = {
    "IPEDSCOUNT1": "awards_year_1",
    "IPEDSCOUNT2": "awards_year_2",
    "DEBT_ALL_STGP_ANY_N": "borrower_count",
    "DEBT_ALL_STGP_ANY_MEAN": "mean_debt",
    "DEBT_ALL_STGP_ANY_MDN": "median_debt",
    "EARN_COUNT_WNE_1YR": "earners_count_1yr",
    "EARN_MDN_1YR": "median_earnings_1yr",
    "EARN_COUNT_WNE_4YR": "earners_count_4yr",
    "EARN_MDN_4YR": "median_earnings_4yr",
    "EARN_COUNT_WNE_5YR": "earners_count_5yr",
    "EARN_MDN_5YR": "median_earnings_5yr",
}


def clean(value: str | None) -> str:
    value = "" if value is None else value.strip()
    return "" if value in NULL_MARKERS else value


def sql_text(value: str) -> str:
    return value.replace("'", "''")


def write_rows(path: Path, columns: list[str], rows) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=columns, extrasaction="ignore", lineterminator="\r\n"
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean(row.get(column)) for column in columns})
            count += 1
    return count


def load_statement(path: Path, table: str, columns: list[str], keys: set[str]) -> str:
    variables = [f"@{column}" for column in columns]
    assignments = [
        f"  {column} = @{column}" if column in keys
        else f"  {column} = NULLIF(@{column}, '')"
        for column in columns
    ]
    portable_path = str(path).replace("\\", "/").replace("'", "''")
    return f"""LOAD DATA LOCAL INFILE '{portable_path}'
IGNORE INTO TABLE {table}
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 LINES
({', '.join(variables)})
SET
{',\n'.join(assignments)};
"""


def build(args: argparse.Namespace) -> None:
    merged_path = Path(args.institution_file)
    field_path = Path(args.field_of_study_file)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    new_england_ids: set[str] = set()
    with merged_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"UNITID", "STABBR"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Institution file is missing columns: {sorted(missing)}")
        for row in reader:
            if clean(row["STABBR"]) in NEW_ENGLAND:
                new_england_ids.add(clean(row["UNITID"]))

    cip_codes: dict[str, dict[str, str]] = {}
    credentials: dict[str, dict[str, str]] = {}
    programs: dict[tuple[str, str, str], dict[str, str]] = {}

    with field_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "UNITID", "CIPCODE", "CIPDESC", "CREDLEV", "CREDDESC",
            *PROGRAM_COLUMNS.keys(),
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Field-of-study file is missing columns: {sorted(missing)}")

        for source in reader:
            unit_id = clean(source["UNITID"])
            if unit_id not in new_england_ids:
                continue
            cip = clean(source["CIPCODE"])
            credential = clean(source["CREDLEV"])
            if not cip or not credential:
                continue
            cip_codes.setdefault(cip, {
                "cip_code": cip,
                "cip_display": f"{cip[:2]}.{cip[2:]}" if len(cip) > 2 else cip,
                "cip_description": clean(source["CIPDESC"]),
                "cip_version": args.cip_version,
            })
            credentials.setdefault(credential, {
                "credential_level_id": credential,
                "credential_description": clean(source["CREDDESC"]),
            })
            row = {
                "unit_id": unit_id,
                "cip_code": cip,
                "credential_level_id": credential,
                "release_id": args.release_id,
            }
            row.update({target: clean(source[source_name])
                        for source_name, target in PROGRAM_COLUMNS.items()})
            programs[(unit_id, cip, credential)] = row

    cip_columns = ["cip_code", "cip_display", "cip_description", "cip_version"]
    credential_columns = ["credential_level_id", "credential_description"]
    program_columns = [
        "unit_id", "cip_code", "credential_level_id", "release_id",
        *PROGRAM_COLUMNS.values(),
    ]
    counts = {
        "new_england_institution_ids": len(new_england_ids),
        "cip_codes": write_rows(output_dir / "cip_codes.csv", cip_columns, cip_codes.values()),
        "credential_levels": write_rows(
            output_dir / "credential_levels.csv", credential_columns, credentials.values()
        ),
        "program_snapshots": write_rows(
            output_dir / "program_snapshots.csv", program_columns, programs.values()
        ),
    }

    script = [
        "USE new_england_college_data;",
        "SET SESSION sql_mode = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';",
        f"""INSERT INTO source_release
(release_id, release_label, release_date, institution_academic_year,
 program_academic_year, source_name, source_url)
VALUES ('{sql_text(args.release_id)}', '{sql_text(args.release_label)}',
        '{sql_text(args.release_date)}', NULL, '{sql_text(args.program_year)}',
        'U.S. Department of Education College Scorecard',
        'https://collegescorecard.ed.gov/data/')
ON DUPLICATE KEY UPDATE
  release_label = VALUES(release_label),
  release_date = VALUES(release_date),
  program_academic_year = VALUES(program_academic_year);""",
        load_statement(output_dir / "cip_codes.csv", "cip_code", cip_columns,
                       {"cip_code", "cip_display", "cip_description"}),
        load_statement(output_dir / "credential_levels.csv", "credential_level",
                       credential_columns,
                       {"credential_level_id", "credential_description"}),
        load_statement(output_dir / "program_snapshots.csv", "program_snapshot",
                       program_columns,
                       {"unit_id", "cip_code", "credential_level_id", "release_id"}),
        "-- IGNORE prevents a rerun from replacing existing historical rows with blanks.",
        f"-- Generated rows: {counts}",
    ]
    (output_dir / "02_load_field_of_study.sql").write_text(
        "\n\n".join(script) + "\n", encoding="utf-8"
    )

    print(f"Created field-of-study load files in {output_dir.resolve()}")
    for name, count in counts.items():
        print(f"  {name}: {count:,}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--institution-file", required=True)
    parser.add_argument("--field-of-study-file", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--release-label", required=True)
    parser.add_argument("--release-date", required=True)
    parser.add_argument("--program-year", required=True)
    parser.add_argument("--cip-version", default="2020")
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
