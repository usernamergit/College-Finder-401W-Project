USE new_england_college_data;

SET SESSION sql_mode = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

SET FOREIGN_KEY_CHECKS = 0;

INSERT INTO source_release
(release_id, release_label, release_date, institution_academic_year,
 program_academic_year, source_name, source_url)
VALUES ('scorecard_2026-06-10_most_recent', 'College Scorecard Most Recent — June 10, 2026', '2026-06-10',
        '2025-26', '2023-24',
        'U.S. Department of Education College Scorecard',
        'https://collegescorecard.ed.gov/data/')
ON DUPLICATE KEY UPDATE
  release_label = VALUES(release_label), release_date = VALUES(release_date),
  institution_academic_year = VALUES(institution_academic_year),
  program_academic_year = VALUES(program_academic_year);

LOAD DATA LOCAL INFILE 'generated/institutions.csv'
REPLACE INTO TABLE institution
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@unit_id, @ope_id, @ope_id6, @institution_name, @city, @state_code, @zip_code, @accrediting_agency, @institution_url, @net_price_calculator_url, @latitude, @longitude)
SET
  unit_id = @unit_id,
  ope_id = NULLIF(@ope_id, ''),
  ope_id6 = NULLIF(@ope_id6, ''),
  institution_name = @institution_name,
  city = NULLIF(@city, ''),
  state_code = @state_code,
  zip_code = NULLIF(@zip_code, ''),
  accrediting_agency = NULLIF(@accrediting_agency, ''),
  institution_url = NULLIF(@institution_url, ''),
  net_price_calculator_url = NULLIF(@net_price_calculator_url, ''),
  latitude = NULLIF(@latitude, ''),
  longitude = NULLIF(@longitude, '');


LOAD DATA LOCAL INFILE 'generated/cip_codes.csv'
REPLACE INTO TABLE cip_code
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


LOAD DATA LOCAL INFILE 'generated/credential_levels.csv'
REPLACE INTO TABLE credential_level
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@credential_level_id, @credential_description)
SET
  credential_level_id = @credential_level_id,
  credential_description = @credential_description;


LOAD DATA LOCAL INFILE 'generated/institution_snapshots.csv'
REPLACE INTO TABLE institution_snapshot
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@unit_id, @release_id, @main_campus, @branch_count, @predominant_degree, @highest_degree, @control_type, @region_code, @locale_code, @currently_operating, @distance_only, @undergraduate_enrollment, @admission_rate, @average_sat, @act_composite_midpoint, @in_state_tuition, @out_of_state_tuition, @average_net_price_public, @average_net_price_private, @average_cost_of_attendance, @full_time_retention_4yr, @full_time_retention_lt4yr, @completion_rate_150_4yr, @completion_rate_150_lt4yr, @pell_recipient_rate, @federal_loan_rate, @median_debt_at_repayment, @median_earnings_1yr, @median_earnings_4yr, @median_earnings_5yr)
SET
  unit_id = @unit_id,
  release_id = @release_id,
  main_campus = NULLIF(@main_campus, ''),
  branch_count = NULLIF(@branch_count, ''),
  predominant_degree = NULLIF(@predominant_degree, ''),
  highest_degree = NULLIF(@highest_degree, ''),
  control_type = NULLIF(@control_type, ''),
  region_code = NULLIF(@region_code, ''),
  locale_code = NULLIF(@locale_code, ''),
  currently_operating = NULLIF(@currently_operating, ''),
  distance_only = NULLIF(@distance_only, ''),
  undergraduate_enrollment = NULLIF(@undergraduate_enrollment, ''),
  admission_rate = NULLIF(@admission_rate, ''),
  average_sat = NULLIF(@average_sat, ''),
  act_composite_midpoint = NULLIF(@act_composite_midpoint, ''),
  in_state_tuition = NULLIF(@in_state_tuition, ''),
  out_of_state_tuition = NULLIF(@out_of_state_tuition, ''),
  average_net_price_public = NULLIF(@average_net_price_public, ''),
  average_net_price_private = NULLIF(@average_net_price_private, ''),
  average_cost_of_attendance = NULLIF(@average_cost_of_attendance, ''),
  full_time_retention_4yr = NULLIF(@full_time_retention_4yr, ''),
  full_time_retention_lt4yr = NULLIF(@full_time_retention_lt4yr, ''),
  completion_rate_150_4yr = NULLIF(@completion_rate_150_4yr, ''),
  completion_rate_150_lt4yr = NULLIF(@completion_rate_150_lt4yr, ''),
  pell_recipient_rate = NULLIF(@pell_recipient_rate, ''),
  federal_loan_rate = NULLIF(@federal_loan_rate, ''),
  median_debt_at_repayment = NULLIF(@median_debt_at_repayment, ''),
  median_earnings_1yr = NULLIF(@median_earnings_1yr, ''),
  median_earnings_4yr = NULLIF(@median_earnings_4yr, ''),
  median_earnings_5yr = NULLIF(@median_earnings_5yr, '');


LOAD DATA LOCAL INFILE 'generated/program_snapshots.csv'
REPLACE INTO TABLE program_snapshot
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


SET FOREIGN_KEY_CHECKS = 1;

-- Generated rows: {'institutions': 300, 'institution_snapshots': 300, 'cip_codes': 365, 'credential_levels': 9, 'program_snapshots': 14562}
