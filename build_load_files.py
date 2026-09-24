#!/usr/bin/env python3
"""Create clean New England CSVs and a MySQL LOAD DATA script."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

NEW_ENGLAND = {"CT", "ME", "MA", "NH", "RI", "VT"}
NULL_MARKERS = {"", "NULL", "PrivacySuppressed", "PS"}

INSTITUTION_COLUMNS = {
    "UNITID": "unit_id", "OPEID": "ope_id", "OPEID6": "ope_id6",
    "INSTNM": "institution_name", "CITY": "city", "STABBR": "state_code",
    "ZIP": "zip_code", "ACCREDAGENCY": "accrediting_agency",
    "INSTURL": "institution_url", "NPCURL": "net_price_calculator_url",
    "LATITUDE": "latitude", "LONGITUDE": "longitude",
}

SNAPSHOT_COLUMNS = {
    "MAIN": "main_campus", "NUMBRANCH": "branch_count",
    "PREDDEG": "predominant_degree", "HIGHDEG": "highest_degree",
    "CONTROL": "control_type", "REGION": "region_code", "LOCALE": "locale_code",
    "CURROPER": "currently_operating", "DISTANCEONLY": "distance_only",
    "UGDS": "undergraduate_enrollment", "ADM_RATE": "admission_rate",
    "SAT_AVG": "average_sat", "ACTCMMID": "act_composite_midpoint",
    "TUITIONFEE_IN": "in_state_tuition", "TUITIONFEE_OUT": "out_of_state_tuition",
    "NPT4_PUB": "average_net_price_public", "NPT4_PRIV": "average_net_price_private",
    "COSTT4_A": "average_cost_of_attendance", "RET_FT4": "full_time_retention_4yr",
    "RET_FTL4": "full_time_retention_lt4yr", "C150_4": "completion_rate_150_4yr",
    "C150_L4": "completion_rate_150_lt4yr", "PCTPELL": "pell_recipient_rate",
    "PCTFLOAN": "federal_loan_rate", "DEBT_MDN": "median_debt_at_repayment",
    "MD_EARN_WNE_1YR": "median_earnings_1yr",
    "MD_EARN_WNE_4YR": "median_earnings_4yr",
    "MD_EARN_WNE_5YR": "median_earnings_5yr",
}

PROGRAM_COLUMNS = {
    "IPEDSCOUNT1": "awards_year_1", "IPEDSCOUNT2": "awards_year_2",
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


def write_rows(path: Path, fieldnames: list[str], rows) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})
            count += 1
    return count


def sql_path(path: Path) -> str:
    # Preserve relative paths so the generated package remains portable.
    return str(path).replace("\\", "/").replace("'", "''")


def load_statement(path: Path, table: str, columns: list[str], key_columns: set[str]) -> str:
    variables = [f"@{c}" for c in columns]
    assignments = []
    for col in columns:
        if col in key_columns:
            assignments.append(f"  {col} = @{col}")
        else:
            assignments.append(f"  {col} = NULLIF(@{col}, '')")
    return f"""LOAD DATA LOCAL INFILE '{sql_path(path)}'
REPLACE INTO TABLE {table}
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 LINES
({', '.join(variables)})
SET\n{',\n'.join(assignments)};\n"""


def build(args: argparse.Namespace) -> None:
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    inst_path = input_dir / "Most-Recent-Cohorts-Institution.csv"
    fos_path = input_dir / "Most-Recent-Cohorts-Field-of-Study.csv"

    institutions = []
    snapshots = []
    new_england_ids = set()
    with inst_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = set(INSTITUTION_COLUMNS) | set(SNAPSHOT_COLUMNS)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Institution file is missing columns: {sorted(missing)}")
        for source in reader:
            if source["STABBR"] not in NEW_ENGLAND:
                continue
            unit_id = clean(source["UNITID"])
            new_england_ids.add(unit_id)
            institutions.append({target: source[source_col] for source_col, target in INSTITUTION_COLUMNS.items()})
            snapshot = {"unit_id": unit_id, "release_id": args.release_id}
            snapshot.update({target: source[source_col] for source_col, target in SNAPSHOT_COLUMNS.items()})
            snapshots.append(snapshot)

    cip_codes: dict[str, dict[str, str]] = {}
    credentials: dict[str, dict[str, str]] = {}
    programs = []
    with fos_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"UNITID", "CIPCODE", "CIPDESC", "CREDLEV", "CREDDESC"} | set(PROGRAM_COLUMNS)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Field-of-study file is missing columns: {sorted(missing)}")
        for source in reader:
            unit_id = clean(source["UNITID"])
            if unit_id not in new_england_ids:
                continue
            cip = clean(source["CIPCODE"])
            display = f"{cip[:2]}.{cip[2:]}" if len(cip) > 2 else cip
            cip_codes.setdefault(cip, {
                "cip_code": cip, "cip_display": display,
                "cip_description": source["CIPDESC"], "cip_version": "2020",
            })
            cred = clean(source["CREDLEV"])
            credentials.setdefault(cred, {
                "credential_level_id": cred,
                "credential_description": source["CREDDESC"],
            })
            row = {
                "unit_id": unit_id, "cip_code": cip,
                "credential_level_id": cred, "release_id": args.release_id,
            }
            row.update({target: source[source_col] for source_col, target in PROGRAM_COLUMNS.items()})
            programs.append(row)

    inst_cols = list(INSTITUTION_COLUMNS.values())
    snap_cols = ["unit_id", "release_id", *SNAPSHOT_COLUMNS.values()]
    cip_cols = ["cip_code", "cip_display", "cip_description", "cip_version"]
    cred_cols = ["credential_level_id", "credential_description"]
    program_cols = ["unit_id", "cip_code", "credential_level_id", "release_id", *PROGRAM_COLUMNS.values()]

    counts = {
        "institutions": write_rows(output_dir / "institutions.csv", inst_cols, institutions),
        "institution_snapshots": write_rows(output_dir / "institution_snapshots.csv", snap_cols, snapshots),
        "cip_codes": write_rows(output_dir / "cip_codes.csv", cip_cols, cip_codes.values()),
        "credential_levels": write_rows(output_dir / "credential_levels.csv", cred_cols, credentials.values()),
        "program_snapshots": write_rows(output_dir / "program_snapshots.csv", program_cols, programs),
    }

    script = [
        "USE new_england_college_data;",
        "SET SESSION sql_mode = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';",
        "SET FOREIGN_KEY_CHECKS = 0;",
        f"""INSERT INTO source_release
(release_id, release_label, release_date, institution_academic_year,
 program_academic_year, source_name, source_url)
VALUES ('{args.release_id}', '{args.release_label}', '{args.release_date}',
        '{args.institution_year}', '{args.program_year}',
        'U.S. Department of Education College Scorecard',
        'https://collegescorecard.ed.gov/data/')
ON DUPLICATE KEY UPDATE
  release_label = VALUES(release_label), release_date = VALUES(release_date),
  institution_academic_year = VALUES(institution_academic_year),
  program_academic_year = VALUES(program_academic_year);""",
        load_statement(output_dir / "institutions.csv", "institution", inst_cols, {"unit_id", "institution_name", "state_code"}),
        load_statement(output_dir / "cip_codes.csv", "cip_code", cip_cols, {"cip_code", "cip_display", "cip_description"}),
        load_statement(output_dir / "credential_levels.csv", "credential_level", cred_cols, {"credential_level_id", "credential_description"}),
        load_statement(output_dir / "institution_snapshots.csv", "institution_snapshot", snap_cols, {"unit_id", "release_id"}),
        load_statement(output_dir / "program_snapshots.csv", "program_snapshot", program_cols, {"unit_id", "cip_code", "credential_level_id", "release_id"}),
        "SET FOREIGN_KEY_CHECKS = 1;",
        f"-- Generated rows: {counts}",
    ]
    (output_dir / "02_load_generated.sql").write_text("\n\n".join(script) + "\n", encoding="utf-8")
    print(f"Created load files in {output_dir.resolve()}")
    for name, count in counts.items():
        print(f"  {name}: {count:,}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--release-id", default="scorecard_2026-06-10_most_recent")
    parser.add_argument("--release-label", default="College Scorecard Most Recent — June 10, 2026")
    parser.add_argument("--release-date", default="2026-06-10")
    parser.add_argument("--institution-year", default="2025-26")
    parser.add_argument("--program-year", default="2023-24")
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
