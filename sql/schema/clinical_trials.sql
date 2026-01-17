CREATE DATABASE IF NOT EXISTS orange_trials;
USE orange_trials;

DROP TABLE IF EXISTS clinical_trials;

CREATE TABLE clinical_trials (
    trial_record_id INT NOT NULL,
    patient_id VARCHAR(20) NOT NULL,
    age TINYINT NOT NULL,
    sex CHAR(1) NOT NULL,
    site_name VARCHAR(120) NOT NULL,
    trial_phase VARCHAR(20) NOT NULL,
    drug_code VARCHAR(20) NOT NULL,
    therapeutic_area VARCHAR(60) NOT NULL,
    study_arm VARCHAR(20) NOT NULL,
    enrollment_date DATE NOT NULL,
    visit_date DATE NOT NULL,
    baseline_marker DECIMAL(5,2) NOT NULL,
    followup_marker DECIMAL(5,2) NULL,
    systolic_bp SMALLINT NOT NULL,
    diastolic_bp SMALLINT NOT NULL,
    heart_rate SMALLINT NOT NULL,
    adverse_event VARCHAR(40) NOT NULL,
    adverse_event_severity VARCHAR(20) NOT NULL,
    outcome VARCHAR(20) NOT NULL,
    success_flag TINYINT NOT NULL,
    PRIMARY KEY (trial_record_id),
    INDEX idx_phase (trial_phase),
    INDEX idx_drug (drug_code),
    INDEX idx_outcome (outcome)
);
