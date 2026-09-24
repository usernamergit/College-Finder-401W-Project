USE new_england_college_data;

SELECT 'institutions' AS check_name, COUNT(*) AS actual_count, 300 AS expected_count
FROM institution;

SELECT state_code, COUNT(*) AS institutions
FROM institution
GROUP BY state_code
ORDER BY state_code;

SELECT 'orphan institution snapshots' AS check_name, COUNT(*) AS issue_count
FROM institution_snapshot s
LEFT JOIN institution i ON i.unit_id = s.unit_id
WHERE i.unit_id IS NULL;

SELECT 'orphan program institutions' AS check_name, COUNT(*) AS issue_count
FROM program_snapshot p
LEFT JOIN institution i ON i.unit_id = p.unit_id
WHERE i.unit_id IS NULL;

SELECT 'invalid rates' AS check_name, COUNT(*) AS issue_count
FROM institution_snapshot
WHERE admission_rate NOT BETWEEN 0 AND 1
   OR full_time_retention_4yr NOT BETWEEN 0 AND 1
   OR full_time_retention_lt4yr NOT BETWEEN 0 AND 1
   OR completion_rate_150_4yr NOT BETWEEN 0 AND 1
   OR completion_rate_150_lt4yr NOT BETWEEN 0 AND 1
   OR pell_recipient_rate NOT BETWEEN 0 AND 1
   OR federal_loan_rate NOT BETWEEN 0 AND 1;

SELECT 'program rows' AS check_name, COUNT(*) AS actual_count
FROM program_snapshot;

SELECT 'duplicate program keys' AS check_name, COUNT(*) AS issue_count
FROM (
  SELECT unit_id, cip_code, credential_level_id, release_id
  FROM program_snapshot
  GROUP BY unit_id, cip_code, credential_level_id, release_id
  HAVING COUNT(*) > 1
) d;

