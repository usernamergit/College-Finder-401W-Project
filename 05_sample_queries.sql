USE new_england_college_data;

-- Find currently operating bachelor's-oriented colleges in Rhode Island.
SELECT institution_name, city, undergraduate_enrollment, admission_rate,
       average_net_price, completion_rate_150
FROM v_current_institution
WHERE state_code = 'RI'
  AND currently_operating = 1
  AND predominant_degree = 3
ORDER BY institution_name;

-- Compare bachelor's programs matching “Computer Science” across New England.
SELECT institution_name, state_code, cip_display, cip_description,
       awards_year_2, median_earnings_1yr, median_earnings_4yr, median_debt
FROM v_current_program
WHERE credential_level_id = 3
  AND cip_description LIKE '%Computer Science%'
ORDER BY median_earnings_1yr DESC, awards_year_2 DESC;

-- Affordable public institutions with completion context.
SELECT institution_name, state_code, undergraduate_enrollment,
       in_state_tuition, average_net_price, completion_rate_150
FROM v_current_institution
WHERE control_type = 1
ORDER BY average_net_price, completion_rate_150 DESC;

-- Programs with the largest second-year award counts in each state.
WITH ranked AS (
  SELECT p.*,
         ROW_NUMBER() OVER (
           PARTITION BY state_code
           ORDER BY awards_year_2 DESC
         ) AS state_rank
  FROM v_current_program p
  WHERE awards_year_2 IS NOT NULL
)
SELECT state_code, institution_name, cip_description,
       credential_description, awards_year_2
FROM ranked
WHERE state_rank <= 10
ORDER BY state_code, state_rank;

-- This becomes useful after at least two releases have been imported.
SELECT institution_name, cip_description, credential_description,
       release_date, current_awards, previous_release_awards, awards_change
FROM v_program_release_change x
JOIN institution i ON i.unit_id = x.unit_id
JOIN cip_code c ON c.cip_code = x.cip_code
JOIN credential_level cl ON cl.credential_level_id = x.credential_level_id
WHERE previous_release_awards IS NOT NULL
ORDER BY ABS(awards_change) DESC;

