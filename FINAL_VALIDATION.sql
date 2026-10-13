USE new_england_college_data;

SELECT 'institutions' AS item, COUNT(*) AS row_count FROM institution
UNION ALL
SELECT 'institution snapshots', COUNT(*) FROM institution_snapshot
UNION ALL
SELECT 'program snapshots', COUNT(*) FROM program_snapshot
UNION ALL
SELECT 'source releases', COUNT(*) FROM source_release
UNION ALL
SELECT 'CIP codes', COUNT(*) FROM cip_code
UNION ALL
SELECT 'credential levels', COUNT(*) FROM credential_level;

SELECT
  sr.release_id,
  sr.institution_academic_year,
  sr.program_academic_year,
  COUNT(DISTINCT ins.unit_id) AS institution_snapshots,
  COUNT(DISTINCT CONCAT_WS('|', ps.unit_id, ps.cip_code, ps.credential_level_id)) AS program_snapshots
FROM source_release sr
LEFT JOIN institution_snapshot ins ON ins.release_id = sr.release_id
LEFT JOIN program_snapshot ps ON ps.release_id = sr.release_id
GROUP BY sr.release_id, sr.institution_academic_year, sr.program_academic_year
ORDER BY sr.release_date, sr.release_id;

SELECT ps.release_id, COUNT(*) AS orphaned_program_rows
FROM program_snapshot ps
LEFT JOIN institution i ON i.unit_id = ps.unit_id
WHERE i.unit_id IS NULL
GROUP BY ps.release_id;

