import pandas as pd
import random
from faker import Faker
from datetime import timedelta

fake = Faker('en_IN')
random.seed(42)
Faker.seed(42)

# ── CONFIG ──────────────────────────────────────────────
NUM_RECORDS = 10000
OUTPUT_PATH = r"data\hospital_patients.csv"   # change path if needed
# ────────────────────────────────────────────────────────

DEPARTMENTS = {
    "Cardiology":       ["Heart Attack", "Hypertension", "Arrhythmia", "Heart Failure", "Angina"],
    "Orthopedics":      ["Fracture", "Osteoarthritis", "Spinal Stenosis", "Ligament Tear", "Back Pain"],
    "Neurology":        ["Stroke", "Epilepsy", "Migraine", "Parkinson's Disease", "Brain Tumor"],
    "Gastroenterology": ["Appendicitis", "Gastritis", "Liver Cirrhosis", "Pancreatitis", "IBS"],
    "Pulmonology":      ["Pneumonia", "Asthma", "COPD", "Tuberculosis", "Bronchitis"],
    "Oncology":         ["Breast Cancer", "Lung Cancer", "Colon Cancer", "Leukemia", "Cervical Cancer"],
    "Nephrology":       ["Kidney Failure", "UTI", "Kidney Stones", "Chronic Kidney Disease", "Nephrotic Syndrome"],
    "General Surgery":  ["Hernia", "Gallstones", "Appendix Removal", "Wound Infection", "Abscess"],
}

DOCTORS = {
    "Cardiology":       ["Dr. Ramesh Iyer", "Dr. Priya Nair", "Dr. Suresh Menon"],
    "Orthopedics":      ["Dr. Anil Sharma", "Dr. Kavitha Rao", "Dr. Deepak Verma"],
    "Neurology":        ["Dr. Sunita Patel", "Dr. Arjun Mehta", "Dr. Lakshmi Devi"],
    "Gastroenterology": ["Dr. Mohan Kumar", "Dr. Sneha Pillai", "Dr. Rajiv Gupta"],
    "Pulmonology":      ["Dr. Vijay Nair", "Dr. Anitha Krishnan", "Dr. Balu Reddy"],
    "Oncology":         ["Dr. Meena Srinivas", "Dr. Harish Babu", "Dr. Pooja Tiwari"],
    "Nephrology":       ["Dr. Sanjay Das", "Dr. Rekha Mishra", "Dr. Ganesh Murthy"],
    "General Surgery":  ["Dr. Kiran Joshi", "Dr. Divya Nambiar", "Dr. Prasad Hegde"],
}

# Avg LOS and billing range per department (realistic Indian hospital rates ₹)
DEPT_CONFIG = {
    "Cardiology":       {"los_range": (3, 12),  "bill_range": (25000, 200000)},
    "Orthopedics":      {"los_range": (2, 10),  "bill_range": (20000, 180000)},
    "Neurology":        {"los_range": (4, 15),  "bill_range": (30000, 250000)},
    "Gastroenterology": {"los_range": (2, 8),   "bill_range": (10000, 120000)},
    "Pulmonology":      {"los_range": (3, 10),  "bill_range": (15000, 130000)},
    "Oncology":         {"los_range": (5, 20),  "bill_range": (50000, 500000)},
    "Nephrology":       {"los_range": (3, 12),  "bill_range": (20000, 180000)},
    "General Surgery":  {"los_range": (1, 7),   "bill_range": (8000, 100000)},
}

INSURANCE_TYPES   = ["Government", "Private", "Corporate", "Self-Pay", "ESI"]
ADMISSION_TYPES   = ["Emergency", "Elective", "Urgent"]
BLOOD_GROUPS      = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
DISCHARGE_STATUS  = ["Recovered", "Referred", "LAMA", "Deceased", "Transferred"]
PAYMENT_STATUS    = ["Paid", "Pending", "Partial", "Insurance Claimed"]

def generate_record(patient_id):
    dept       = random.choice(list(DEPARTMENTS.keys()))
    diagnosis  = random.choice(DEPARTMENTS[dept])
    doctor     = random.choice(DOCTORS[dept])
    config     = DEPT_CONFIG[dept]

    age        = int(random.gauss(45, 18))
    age        = max(1, min(95, age))
    gender     = random.choice(["Male", "Female"])
    blood      = random.choice(BLOOD_GROUPS)

    los        = random.randint(*config["los_range"])
    admit_date = fake.date_between(start_date="-2y", end_date="today")
    discharge_date = admit_date + timedelta(days=los)

    # Bill correlated with LOS + some department weight
    base_bill  = random.randint(*config["bill_range"])
    bill_amount= round(base_bill + (los * random.randint(1000, 4000)), 2)

    insurance  = random.choice(INSURANCE_TYPES)
    admission  = random.choice(ADMISSION_TYPES)

    # Readmission: higher chance for Oncology/Nephrology/Cardiology
    high_risk_depts    = ["Oncology", "Nephrology", "Cardiology", "Neurology"]
    readmit_prob       = 0.18 if dept in high_risk_depts else 0.08
    readmission        = "Yes" if random.random() < readmit_prob else "No"

    # Discharge status weighted
    discharge_wt = [0.70, 0.10, 0.08, 0.05, 0.07]
    discharge    = random.choices(DISCHARGE_STATUS, weights=discharge_wt, k=1)[0]

    # Payment status
    if insurance == "Self-Pay":
        pay_status = random.choices(PAYMENT_STATUS, weights=[0.40, 0.30, 0.30, 0.00], k=1)[0]
    else:
        pay_status = random.choices(PAYMENT_STATUS, weights=[0.20, 0.10, 0.10, 0.60], k=1)[0]

    return {
        "PatientID":              f"PID{patient_id:05d}",
        "PatientName":            fake.name(),
        "Age":                    age,
        "Gender":                 gender,
        "BloodGroup":             blood,
        "Department":             dept,
        "Diagnosis":              diagnosis,
        "DoctorName":             doctor,
        "AdmissionType":          admission,
        "AdmissionDate":          admit_date,
        "DischargeDate":          discharge_date,
        "LengthOfStay":           los,
        "BillAmount":             bill_amount,
        "InsuranceType":          insurance,
        "PaymentStatus":          pay_status,
        "DischargeStatus":        discharge,
        "ReadmissionWithin30Days":readmission,
    }

print("Generating 10,000 patient records...")
records = [generate_record(i+1) for i in range(NUM_RECORDS)]
df = pd.DataFrame(records)

df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8-sig')
print(f"Done! Dataset saved to: {OUTPUT_PATH}")
print(f"Shape: {df.shape}")
print(f"\nSample:\n{df.head(3).to_string()}")