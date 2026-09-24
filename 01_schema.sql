CREATE DATABASE IF NOT EXISTS new_england_college_data
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE new_england_college_data;

CREATE TABLE IF NOT EXISTS source_release (
    release_id VARCHAR(80) PRIMARY KEY,
    release_label VARCHAR(160) NOT NULL,
    release_date DATE NOT NULL,
    institution_academic_year VARCHAR(9) NULL,
    program_academic_year VARCHAR(9) NULL,
    source_name VARCHAR(120) NOT NULL,
    source_url VARCHAR(500) NULL,
    imported_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS institution (
    unit_id INT PRIMARY KEY,
    ope_id VARCHAR(10) NULL,
    ope_id6 VARCHAR(10) NULL,
    institution_name VARCHAR(255) NOT NULL,
    city VARCHAR(120) NULL,
    state_code CHAR(2) NOT NULL,
    zip_code VARCHAR(20) NULL,
    accrediting_agency VARCHAR(500) NULL,
    institution_url VARCHAR(500) NULL,
    net_price_calculator_url VARCHAR(500) NULL,
    latitude DECIMAL(9,6) NULL,
    longitude DECIMAL(9,6) NULL,
    CONSTRAINT chk_institution_new_england
      CHECK (state_code IN ('CT','ME','MA','NH','RI','VT')),
    INDEX idx_institution_state_name (state_code, institution_name),
    INDEX idx_institution_ope6 (ope_id6)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS institution_snapshot (
    unit_id INT NOT NULL,
    release_id VARCHAR(80) NOT NULL,
    main_campus BOOLEAN NULL,
    branch_count SMALLINT UNSIGNED NULL,
    predominant_degree TINYINT UNSIGNED NULL,
    highest_degree TINYINT UNSIGNED NULL,
    control_type TINYINT UNSIGNED NULL,
    region_code TINYINT UNSIGNED NULL,
    locale_code SMALLINT UNSIGNED NULL,
    currently_operating BOOLEAN NULL,
    distance_only BOOLEAN NULL,
    undergraduate_enrollment INT UNSIGNED NULL,
    admission_rate DECIMAL(7,6) NULL,
    average_sat SMALLINT UNSIGNED NULL,
    act_composite_midpoint DECIMAL(5,2) NULL,
    in_state_tuition DECIMAL(12,2) NULL,
    out_of_state_tuition DECIMAL(12,2) NULL,
    average_net_price_public DECIMAL(12,2) NULL,
    average_net_price_private DECIMAL(12,2) NULL,
    average_cost_of_attendance DECIMAL(12,2) NULL,
    full_time_retention_4yr DECIMAL(7,6) NULL,
    full_time_retention_lt4yr DECIMAL(7,6) NULL,
    completion_rate_150_4yr DECIMAL(7,6) NULL,
    completion_rate_150_lt4yr DECIMAL(7,6) NULL,
    pell_recipient_rate DECIMAL(7,6) NULL,
    federal_loan_rate DECIMAL(7,6) NULL,
    median_debt_at_repayment DECIMAL(12,2) NULL,
    median_earnings_1yr DECIMAL(12,2) NULL,
    median_earnings_4yr DECIMAL(12,2) NULL,
    median_earnings_5yr DECIMAL(12,2) NULL,
    PRIMARY KEY (unit_id, release_id),
    CONSTRAINT fk_inst_snapshot_institution FOREIGN KEY (unit_id)
      REFERENCES institution(unit_id),
    CONSTRAINT fk_inst_snapshot_release FOREIGN KEY (release_id)
      REFERENCES source_release(release_id),
    INDEX idx_inst_snapshot_release (release_id),
    INDEX idx_inst_snapshot_control (control_type),
    INDEX idx_inst_snapshot_enrollment (undergraduate_enrollment)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS cip_code (
    cip_code VARCHAR(10) PRIMARY KEY,
    cip_display VARCHAR(12) NOT NULL,
    cip_description VARCHAR(500) NOT NULL,
    cip_version SMALLINT UNSIGNED NULL DEFAULT 2020,
    INDEX idx_cip_description (cip_description)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS credential_level (
    credential_level_id TINYINT UNSIGNED PRIMARY KEY,
    credential_description VARCHAR(160) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS program_snapshot (
    unit_id INT NOT NULL,
    cip_code VARCHAR(10) NOT NULL,
    credential_level_id TINYINT UNSIGNED NOT NULL,
    release_id VARCHAR(80) NOT NULL,
    awards_year_1 INT UNSIGNED NULL,
    awards_year_2 INT UNSIGNED NULL,
    borrower_count INT UNSIGNED NULL,
    mean_debt DECIMAL(12,2) NULL,
    median_debt DECIMAL(12,2) NULL,
    earners_count_1yr INT UNSIGNED NULL,
    median_earnings_1yr DECIMAL(12,2) NULL,
    earners_count_4yr INT UNSIGNED NULL,
    median_earnings_4yr DECIMAL(12,2) NULL,
    earners_count_5yr INT UNSIGNED NULL,
    median_earnings_5yr DECIMAL(12,2) NULL,
    PRIMARY KEY (unit_id, cip_code, credential_level_id, release_id),
    CONSTRAINT fk_program_institution FOREIGN KEY (unit_id)
      REFERENCES institution(unit_id),
    CONSTRAINT fk_program_cip FOREIGN KEY (cip_code)
      REFERENCES cip_code(cip_code),
    CONSTRAINT fk_program_credential FOREIGN KEY (credential_level_id)
      REFERENCES credential_level(credential_level_id),
    CONSTRAINT fk_program_release FOREIGN KEY (release_id)
      REFERENCES source_release(release_id),
    INDEX idx_program_release_cip (release_id, cip_code),
    INDEX idx_program_cip_credential (cip_code, credential_level_id),
    INDEX idx_program_earnings (median_earnings_1yr)
) ENGINE=InnoDB;

