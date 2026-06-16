# HospitalAnalysis
End-to-end analytics project analysing 10,000 hospital patient records across 8 departments to uncover revenue drivers, readmission risks, and operational performance gaps.

•	Generated a realistic 10,000-row dataset using Python (Faker, Pandas) with 17 fields — patient demographics, diagnosis, billing, insurance type, and discharge outcome
•	Performed full EDA using Pandas: null checks, duplicate detection, IQR-based outlier analysis, and 18 business summary tables across departments, diagnoses, age groups, and payment trends
•	Loaded data into PostgreSQL via SQLAlchemy and wrote 15 business SQL queries — revenue by department, readmission rates, top diagnoses by cost, age-group billing, and weekday vs weekend admissions
•	Built a 3-page interactive Power BI dashboard (Executive Overview, Patient Analytics, Financial Analysis) with 6 DAX KPI measures, dynamic slicers, and drill-through filters
•	Key findings: Oncology generated 29% of total hospital revenue (Rs 38.3 Cr); Cardiology had the highest 30-day readmission rate at 18.2%; overall hospital readmission rate 13.1% flagged for clinical review
