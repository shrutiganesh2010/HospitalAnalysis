import pandas as pd

df = pd.read_csv(r"C:\Users\Shru\Downloads\HospitalAnalysis\data\hospital_cleaned.csv", encoding='utf-8-sig')

df['AdmissionDate'] = pd.to_datetime(df['AdmissionDate'])
df['DischargeDate']  = pd.to_datetime(df['DischargeDate'])

df.to_excel(r"C:\Users\Shru\Downloads\HospitalAnalysis\data\hospital_cleaned.xlsx", index=False, sheet_name="HospitalData")

print(f"Saved! Rows: {len(df)} | Columns: {len(df.columns)}")
print("File: data/hospital_cleaned.xlsx")
