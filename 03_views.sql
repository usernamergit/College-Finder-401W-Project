USE new_england_college_data;

CREATE OR REPLACE VIEW v_latest_release AS
SELECT release_id, release_date
FROM source_release
WHERE release_date = (SELECT MAX(release_date) FROM source_release);

CREATE OR REPLACE VIEW v_current_institution AS
SELECT
    i.*,
    s.release_id,
    s.main_campus,
    s.branch_count,
    s.predominant_degree,
    s.highest_degree,
    s.control_type,
    CASE s.control_type
      WHEN 1 THEN 'Public'
      WHEN 2 THEN 'Private nonprofit'
      WHEN 3 THEN 'Private for-profit'
      WHEN 4 THEN 'Foreign'
      ELSE 'Unknown'
    END AS control_description,
    s.currently_operating,
    s.distance_only,
    s.undergraduate_enrollment,
    s.admission_rate,
    s.average_sat,
    s.act_composite_midpoint,
    s.in_state_tuition,
    s.out_of_state_tuition,
    COALESCE(s.average_net_price_public, s.average_net_price_private) AS average_net_price,
    s.average_cost_of_attendance,
    COALESCE(s.full_time_retention_4yr, s.full_time_retention_lt4yr) AS full_time_retention_rate,
    COALESCE(s.completion_rate_150_4yr, s.completion_rate_150_lt4yr) AS completion_rate_150,
    s.pell_recipient_rate,
    s.federal_loan_rate,
    s.median_debt_at_repayment,
    s.median_earnings_1yr,
    s.median_earnings_4yr,
    s.median_earnings_5yr
FROM institution i
JOIN institution_snapshot s ON s.unit_id = i.unit_id
JOIN v_latest_release lr ON lr.release_id = s.release_id;

CREATE OR REPLACE VIEW v_current_program AS
SELECT
    i.unit_id,
    i.institution_name,
    i.city,
    i.state_code,
    c.cip_code,
    c.cip_display,
    c.cip_description,
    cl.credential_level_id,
    cl.credential_description,
    p.awards_year_1,
    p.awards_year_2,
    p.borrower_count,
    p.mean_debt,
    p.median_debt,
    p.earners_count_1yr,
    p.median_earnings_1yr,
    p.earners_count_4yr,
    p.median_earnings_4yr,
    p.earners_count_5yr,
    p.median_earnings_5yr,
    p.release_id
FROM program_snapshot p
JOIN institution i ON i.unit_id = p.unit_id
JOIN cip_code c ON c.cip_code = p.cip_code
JOIN credential_level cl ON cl.credential_level_id = p.credential_level_id
JOIN v_latest_release lr ON lr.release_id = p.release_id;

CREATE OR REPLACE VIEW v_program_release_change AS
SELECT
    p.unit_id,
    p.cip_code,
    p.credential_level_id,
    p.release_id,
    r.release_date,
    p.awards_year_2 AS current_awards,
    LAG(p.awards_year_2) OVER (
      PARTITION BY p.unit_id, p.cip_code, p.credential_level_id
      ORDER BY r.release_date
    ) AS previous_release_awards,
    p.awards_year_2 - LAG(p.awards_year_2) OVER (
      PARTITION BY p.unit_id, p.cip_code, p.credential_level_id
      ORDER BY r.release_date
    ) AS awards_change
FROM program_snapshot p
JOIN source_release r ON r.release_id = p.release_id;

