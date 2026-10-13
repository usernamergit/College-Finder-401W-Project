#!/usr/bin/env python3
"""Build New England institution load files from a MERGEDYYYY_YY_PP.csv file.

College Scorecard MERGED files contain one row per institution. They can update
the institution and institution_snapshot tables, but they do not contain the
row-per-program fields required by program_snapshot.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


NEW_ENGLAND = {"CT", "ME", "MA", "NH", "RI", "VT"}
NULL_MARKERS = {"", "NA", "NULL", "PrivacySuppressed", "PS"}

INSTITUTION_COLUMNS = {
    "UNITID": "unit_id",
    "OPEID": "ope_id",
    "OPEID6": "ope_id6",
    "INSTNM": "institution_name",
    "CITY": "city",
    "STABBR": "state_code",
    "ZIP": "zip_code",
    "ACCREDAGENCY": "accrediting_agency",
    "INSTURL": "institution_url",
    "NPCURL": "net_price_calculator_url",
    "LATITUDE": "latitude",
    "LONGITUDE": "longitude",
}

SNAPSHOT_COLUMNS = {
    "MAIN": "main_campus",
    "NUMBRANCH": "branch_count",
    "PREDDEG": "predominant_degree",
    "HIGHDEG": "highest_degree",
    "CONTROL": "control_type",
    "REGION": "region_code",
    "LOCALE": "locale_code",
    "CURROPER": "currently_operating",
    "DISTANCEONLY": "distance_only",
    "UGDS": "undergraduate_enrollment",
    "ADM_RATE": "admission_rate",
    "SAT_AVG": "average_sat",
    "ACTCMMID": "act_composite_midpoint",
    "TUITIONFEE_IN": "in_state_tuition",
    "TUITIONFEE_OUT": "out_of_state_tuition",
    "NPT4_PUB": "average_net_price_public",
    "NPT4_PRIV": "average_net_price_private",
    "COSTT4_A": "average_cost_of_attendance",
    "RET_FT4": "full_time_retention_4yr",
    "RET_FTL4": "full_time_retention_lt4yr",
    "C150_4": "completion_rate_150_4yr",
    "C150_L4": "completion_rate_150_lt4yr",
    "PCTPELL": "pell_recipient_rate",
    "PCTFLOAN": "federal_loan_rate",
    "DEBT_MDN": "median_debt_at_repayment",
    "MD_EARN_WNE_1YR": "median_earnings_1yr",
    "MD_EARN_WNE_4YR": "median_earnings_4yr",
    "MD_EARN_WNE_5YR": "median_earnings_5yr",
}


def clean(value: str | None) -> str:
    value = "" if value is None else value.strip()
    return "" if value in NULL_MARKERS else value


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> int:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\r\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})
    return len(rows)


def sql_path(path: Path) -> str:
    return str(path).replace("\\", "/").replace("'", "''")


def load_statement(
    path: Path,
    table: str,
    columns: list[str],
    required_columns: set[str],
) -> str:
    variables = [f"@{column}" for column in columns]
    assignments = []
    for column in columns:
        if column in required_columns:
            assignments.append(f"  {column} = @{column}")
        else:
            assignments.append(f"  {column} = NULLIF(@{column}, '')")
    return f"""LOAD DATA LOCAL INFILE '{sql_path(path)}'
IGNORE INTO TABLE {table}
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 LINES
({', '.join(variables)})
SET
{',\n'.join(assignments)};
"""


def sql_quote(value: str) -> str:
    return value.replace("'", "''")


def build(args: argparse.Namespace) -> None:
    merged_path = Path(args.merged_file)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    institutions: dict[str, dict[str, str]] = {}
    snapshots: dict[str, dict[str, str]] = {}

    with merged_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = set(INSTITUTION_COLUMNS) | set(SNAPSHOT_COLUMNS)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(
                "Merged institution file is missing columns: "
                f"{sorted(missing)}"
            )

        for source in reader:
            if clean(source.get("STABBR")) not in NEW_ENGLAND:
                continue
            unit_id = clean(source.get("UNITID"))
            if not unit_id:
                continue

            institution = {
                target: clean(source.get(source_column))
                for source_column, target in INSTITUTION_COLUMNS.items()
            }
            snapshot = {"unit_id": unit_id, "release_id": args.release_id}
            snapshot.update(
                {
                    target: clean(source.get(source_column))
                    for source_column, target in SNAPSHOT_COLUMNS.items()
                }
            )
            institutions[unit_id] = institution
            snapshots[unit_id] = snapshot

    institution_columns = list(INSTITUTION_COLUMNS.values())
    snapshot_columns = ["unit_id", "release_id", *SNAPSHOT_COLUMNS.values()]

    institutions_path = output_dir / "institutions.csv"
    snapshots_path = output_dir / "institution_snapshots.csv"
    institution_count = write_rows(
        institutions_path,
        institution_columns,
        list(institutions.values()),
    )
    snapshot_count = write_rows(
        snapshots_path,
        snapshot_columns,
        list(snapshots.values()),
    )

    release_id = sql_quote(args.release_id)
    release_label = sql_quote(args.release_label)
    release_date = sql_quote(args.release_date)
    institution_year = sql_quote(args.institution_year)
    source_url = sql_quote(args.source_url)

    script = [
        "USE new_england_college_data;",
        "SET SESSION sql_mode = "
        "'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';",
        f"""INSERT INTO source_release
(release_id, release_label, release_date, institution_academic_year,
 source_name, source_url)
VALUES ('{release_id}', '{release_label}', '{release_date}',
        '{institution_year}',
        'U.S. Department of Education College Scorecard',
        '{source_url}')
ON DUPLICATE KEY UPDATE
  release_label = VALUES(release_label),
  release_date = VALUES(release_date),
  institution_academic_year = VALUES(institution_academic_year),
  source_name = VALUES(source_name),
  source_url = VALUES(source_url);""",
        load_statement(
            institutions_path,
            "institution",
            institution_columns,
            {"unit_id", "institution_name", "state_code"},
        ),
        load_statement(
            snapshots_path,
            "institution_snapshot",
            snapshot_columns,
            {"unit_id", "release_id"},
        ),
        f"-- Generated rows: institutions={institution_count}, "
        f"institution_snapshots={snapshot_count}",
        "-- IGNORE preserves any row already stored under the same primary key.",
        "-- This MERGED file contains no row-per-program records. "
        "program_snapshot is intentionally unchanged.",
    ]
    sql_file = output_dir / "02_load_merged_institution.sql"
    sql_file.write_text("\n\n".join(script) + "\n", encoding="utf-8")

    print(f"Created merged institution load files in {output_dir.resolve()}")
    print(f"  institutions: {institution_count:,}")
    print(f"  institution_snapshots: {snapshot_count:,}")
    print("  program_snapshots: 0 (not present in MERGED institution files)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a New England institution release from a College Scorecard MERGED file."
    )
    parser.add_argument("--merged-file", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--release-label", required=True)
    parser.add_argument("--release-date", required=True)
    parser.add_argument("--institution-year", required=True)
    parser.add_argument(
        "--source-url",
        default="https://collegescorecard.ed.gov/data/",
    )
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
