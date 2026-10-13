-- Run from the folder containing this file with the MySQL command-line client.
-- This file creates the schema, imports every validated release, and creates views.

SOURCE sql/01_schema.sql

-- Load matched institution/program releases in chronological order.
SOURCE generated_merged_2016_17/02_load_merged_institution.sql
SOURCE generated_field_2016_17/02_load_field_of_study.sql
SOURCE generated_merged_2017_18/02_load_merged_institution.sql
SOURCE generated_field_2017_18/02_load_field_of_study.sql
SOURCE generated_merged_2018_19/02_load_merged_institution.sql
SOURCE generated_field_2018_19/02_load_field_of_study.sql
SOURCE generated_merged_2019_20/02_load_merged_institution.sql
SOURCE generated_field_2019_20/02_load_field_of_study.sql
SOURCE generated_merged_2020_21/02_load_merged_institution.sql
SOURCE generated_field_2020_21/02_load_field_of_study.sql
SOURCE generated_merged_2021_22/02_load_merged_institution.sql
SOURCE generated_field_2021_22/02_load_field_of_study.sql
SOURCE generated_merged_2022_23/02_load_merged_institution.sql
SOURCE generated_field_2022_23/02_load_field_of_study.sql

-- Later institution releases (no matching historical field file was provided).
SOURCE generated_merged_2023_24/02_load_merged_institution.sql
SOURCE generated_merged_2024_25/02_load_merged_institution.sql
SOURCE generated_merged_2025_26/02_load_merged_institution.sql

-- The current Scorecard release contains the latest supplied program outcomes.
SOURCE generated_current_program_2023_24/02_load_current_program.sql

-- 2015-16 program data has no matching MERGED file; load it after institutions exist.
SOURCE generated_field_2015_16/02_load_field_of_study.sql

SOURCE sql/03_views.sql
SOURCE FINAL_VALIDATION.sql

