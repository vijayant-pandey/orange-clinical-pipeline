
-- A) Quick sanity + exploring data (basic filters)
-- Q1. Count by Phase (basic GROUP BY)
SELECT trial_phase, COUNT(*) AS cnt
FROM clinical_trials
GROUP BY trial_phase
ORDER BY cnt DESC;


-- Q2. Filter: Phase III + High Dose + Severe adverse events (classic interview filter)
SELECT trial_record_id, patient_id, age, sex, site_name, drug_code, trial_phase,
       study_arm, adverse_event, adverse_event_severity, outcome
FROM clinical_trials
WHERE trial_phase = 'Phase III'
  AND study_arm = 'High Dose'
  AND adverse_event_severity = 'Severe'
ORDER BY enrollment_date DESC
LIMIT 50;


-- Q3. Patients older than 60 with high BP (range filtering)
SELECT patient_id, age, systolic_bp, diastolic_bp, trial_phase, drug_code, outcome
FROM clinical_trials
WHERE age >= 60
  AND systolic_bp >= 160
ORDER BY systolic_bp DESC, age DESC
LIMIT 50;

-- Q4. Find missing follow-up marker (NULL handling)
SELECT trial_record_id, patient_id, trial_phase, drug_code, baseline_marker, followup_marker
FROM clinical_trials
WHERE followup_marker IS NULL
ORDER BY enrollment_date DESC
LIMIT 50;

-- B) Clinical “effectiveness” style analytics
-- Q5. Success rate by drug (important KPI)
SELECT drug_code,
       COUNT(*) AS total,
       SUM(success_flag) AS successes,
       ROUND(100.0 * SUM(success_flag) / COUNT(*), 2) AS success_rate_pct
FROM clinical_trials
GROUP BY drug_code
ORDER BY success_rate_pct DESC, total DESC;


-- Q6. Success rate by phase + drug (more granular)
SELECT trial_phase, drug_code,
       COUNT(*) AS total,
       SUM(success_flag) AS successes,
       ROUND(100.0 * SUM(success_flag) / COUNT(*), 2) AS success_rate_pct
FROM clinical_trials
GROUP BY trial_phase, drug_code
ORDER BY trial_phase, success_rate_pct DESC;



-- Q7. Marker improvement (baseline - followup) by study arm (shows treatment effect)
SELECT study_arm,
       COUNT(*) AS total,
       ROUND(AVG(baseline_marker), 2) AS avg_baseline,
       ROUND(AVG(followup_marker), 2) AS avg_followup,
       ROUND(AVG(baseline_marker - followup_marker), 2) AS avg_improvement
FROM clinical_trials
WHERE followup_marker IS NOT NULL
GROUP BY study_arm
ORDER BY avg_improvement DESC;


-- Q8. Outcome distribution by drug (Improved/No Change/Worsened)
SELECT drug_code, outcome, COUNT(*) AS cnt
FROM clinical_trials
GROUP BY drug_code, outcome
ORDER BY drug_code, cnt DESC;


-- C) Safety analytics (adverse events)
-- Q9. Severe adverse events by drug (safety risk)
SELECT drug_code,
       COUNT(*) AS severe_events
FROM clinical_trials
WHERE adverse_event_severity = 'Severe'
GROUP BY drug_code
ORDER BY severe_events DESC;


-- Q10. Adverse event breakdown by phase (safety vs phase)
SELECT trial_phase, adverse_event_severity, COUNT(*) AS cnt
FROM clinical_trials
GROUP BY trial_phase, adverse_event_severity
ORDER BY trial_phase, cnt DESC;


-- Q11. Top 5 sites with most severe events (operations insight)
SELECT site_name, COUNT(*) AS severe_cnt
FROM clinical_trials
WHERE adverse_event_severity = 'Severe'
GROUP BY site_name
ORDER BY severe_cnt DESC
LIMIT 5;

-- D) Time-based analytics (very interview-friendly)
-- Q12. Monthly enrollment trend (time series)
SELECT DATE_FORMAT(enrollment_date, '%Y-%m') AS month,
       COUNT(*) AS enrollments
FROM clinical_trials
GROUP BY month
ORDER BY month;


-- Q13. Monthly success rate (trend KPI)
SELECT DATE_FORMAT(enrollment_date, '%Y-%m') AS month,
       COUNT(*) AS total,
       SUM(success_flag) AS successes,
       ROUND(100.0 * SUM(success_flag) / COUNT(*), 2) AS success_rate_pct
FROM clinical_trials
GROUP BY month
ORDER BY month;



-- E) “Advanced SQL” (CTEs + window functions) — MySQL 8+ (XAMPP usually supports it)
-- Q14. Rank drugs by success rate (window function)

WITH drug_stats AS (
  SELECT drug_code,
         COUNT(*) AS total,
         SUM(success_flag) AS successes,
         ROUND(100.0 * SUM(success_flag) / COUNT(*), 2) AS success_rate_pct
  FROM clinical_trials
  GROUP BY drug_code
)
SELECT *,
       DENSE_RANK() OVER (ORDER BY success_rate_pct DESC) AS success_rank
FROM drug_stats
ORDER BY success_rank;


-- Q15. Find top 3 highest baseline_marker per drug (window function)
WITH ranked AS (
  SELECT drug_code, patient_id, baseline_marker,
         ROW_NUMBER() OVER (PARTITION BY drug_code ORDER BY baseline_marker DESC) AS rn
  FROM clinical_trials
)
SELECT drug_code, patient_id, baseline_marker
FROM ranked
WHERE rn <= 3
ORDER BY drug_code, baseline_marker DESC;



-- Q16. Compare each site to overall success rate (great “business SQL”)
WITH overall AS (
  SELECT ROUND(100.0 * SUM(success_flag) / COUNT(*), 2) AS overall_success_rate
  FROM clinical_trials
),
site_stats AS (
  SELECT site_name,
         COUNT(*) AS total,
         ROUND(100.0 * SUM(success_flag) / COUNT(*), 2) AS site_success_rate
  FROM clinical_trials
  GROUP BY site_name
)
SELECT s.site_name, s.total, s.site_success_rate, o.overall_success_rate,
       ROUND(s.site_success_rate - o.overall_success_rate, 2) AS diff_vs_overall
FROM site_stats s
CROSS JOIN overall o
ORDER BY diff_vs_overall DESC;



-- F) “Data cleaning checks” (you can mention in interview)
-- Q17. Find weird ages (should be 18–85)
SELECT COUNT(*) AS bad_age_rows
FROM clinical_trials
WHERE age < 18 OR age > 85;


-- Q18. Find impossible BP values (basic sanity)
SELECT COUNT(*) AS bad_bp_rows
FROM clinical_trials
WHERE systolic_bp < 80 OR systolic_bp > 220
   OR diastolic_bp < 40 OR diastolic_bp > 140;
