USE new_england_college_data;

SET SESSION sql_mode = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

INSERT INTO source_release
(release_id, release_label, release_date, institution_academic_year,
 program_academic_year, source_name, source_url)
VALUES ('scorecard_field_2015_16', 'College Scorecard Field of Study 2015-16',
        '2016-06-30', NULL, '2015-16',
        'U.S. Department of Education College Scorecard',
        'https://collegescorecard.ed.gov/data/')
ON DUPLICATE KEY UPDATE
  release_label = VALUES(release_label),
  release_date = VALUES(release_date),
  program_academic_year = VALUES(program_academic_year);

LOAD DATA LOCAL INFILE 'generated_field_2015_16/cip_codes.csv'
IGNORE INTO TABLE cip_code
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@cip_code, @cip_display, @cip_description, @cip_version)
SET
  cip_code = @cip_code,
  cip_display = @cip_display,
  cip_description = @cip_description,
  cip_version = NULLIF(@cip_version, '');


LOAD DATA LOCAL INFILE 'generated_field_2015_16/credential_levels.csv'
IGNORE INTO TABLE credential_level
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@credential_level_id, @credential_description)
SET
  credential_level_id = @credential_level_id,
  credential_description = @credential_description;


LOAD DATA LOCAL INFILE 'generated_field_2015_16/program_snapshots.csv'
IGNORE INTO TABLE program_snapshot
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@unit_id, @cip_code, @credential_level_id, @release_id, @awards_year_1, @awards_year_2, @borrower_count, @mean_debt, @median_debt, @earners_count_1yr, @median_earnings_1yr, @earners_count_4yr, @median_earnings_4yr, @earners_count_5yr, @median_earnings_5yr)
SET
  unit_id = @unit_id,
  cip_code = @cip_code,
  credential_level_id = @credential_level_id,
  release_id = @release_id,
  awards_year_1 = NULLIF(@awards_year_1, ''),
  awards_year_2 = NULLIF(@awards_year_2, ''),
  borrower_count = NULLIF(@borrower_count, ''),
  mean_debt = NULLIF(@mean_debt, ''),
  median_debt = NULLIF(@median_debt, ''),
  earners_count_1yr = NULLIF(@earners_count_1yr, ''),
  median_earnings_1yr = NULLIF(@median_earnings_1yr, ''),
  earners_count_4yr = NULLIF(@earners_count_4yr, ''),
  median_earnings_4yr = NULLIF(@median_earnings_4yr, ''),
  earners_count_5yr = NULLIF(@earners_count_5yr, ''),
  median_earnings_5yr = NULLIF(@median_earnings_5yr, '');


-- IGNORE prevents a rerun from replacing existing historical rows with blanks.

-- Generated rows: {'new_england_institution_ids': 300, 'cip_codes': 341, 'credential_levels': 8, 'program_snapshots': 12458}
