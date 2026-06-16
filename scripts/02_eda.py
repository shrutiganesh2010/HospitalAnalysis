import pandas as pd
import os

df = pd.read_csv(r"C:\Users\Shru\Downloads\HospitalAnalysis\data\hospital_patients.csv")
print(df)

# How many rows and columns do we have?
print("\n---DATASET SHAPE---")
print(f"ROWS :{df.shape[0]}")
print(f"COLUMNS :{df.shape[1]}")


# What are the column names?
print("\n---COLUMN NAMES---")
print(df.columns.tolist())

#What does the first 5 rows look like?
print("\n---FIRST FIVE ROWS---")
print(df.head())

# What data type is each column?
print("\n---DATA TYPES")
print(df.dtypes)

# Are there any missing values?
print("\n--- MISSING VALUES PER COLUMN ---")
print(df.isnull().sum())
print(f"\nTotal missing values :{df.isnull().sum().sum()}")

# Are there any duplicate rows?
print(f"duplicate rows :{df.duplicated().sum()}")

# Dates were read as text — convert them to proper date format
df['AdmissionDate'] = pd.to_datetime(df['AdmissionDate'])
df['DischargeDate']  = pd.to_datetime(df['DischargeDate'])

# Extract useful parts from the date for analysis

df['AdmissionMonth'] = df['AdmissionDate'].dt.month_name()
df['AdmissionYear']  = df['AdmissionDate'].dt.year
df['MonthNum']       = df['AdmissionDate'].dt.month
print("\n--- DATE COLUMNS FIXED ---")
print(df[['AdmissionDate', 'DischargeDate','MonthNum', 'AdmissionMonth', 'AdmissionYear']].head())

# What is the min, max, average of numeric columns?
print("\n--- STATISTICS FOR KEY NUMERIC COLUMNS ---")
print(df[['Age', 'LengthOfStay', 'BillAmount']].describe().round(2))

# IQR = Interquartile Range = difference between 75th and 25th percentile
# Any value below Q1 - 1.5*IQR or above Q3 + 1.5*IQR is an outlier
print("\n--- OUTLIER DETECTION ---")

for col in['Age','LengthOfStay', 'BillAmount']:
    Q1 = df[col].quantile(0.25)
    Q3  = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_limit  = Q1 - 1.5 * IQR
    upper_limit  = Q3 + 1.5 * IQR
    outlier_rows = df[(df[col] < lower_limit) | (df[col] > upper_limit)]
    print(f"{col}: {len(outlier_rows)} outliers found (allowed range: {lower_limit:.1f} to {upper_limit:.1f})")    
    
# These are the headline numbers that go on the Power BI dashboard
print("\n--- KEY PERFORMANCE INDICATORS ---")

total_patients   = len(df)
total_revenue    = df['BillAmount'].sum()
avg_bill         = df['BillAmount'].mean()
avg_los          = df['LengthOfStay'].mean()
readmit_count    = (df['ReadmissionWithin30Days'] == 'Yes').sum()
readmit_rate     = (readmit_count / total_patients) * 100

print(f"Total Patients       : {total_patients:,}")
print(f"Total Revenue        : Rs {total_revenue:,.0f}")
print(f"Average Bill Amount  : Rs {avg_bill:,.0f}")
print(f"Average Length Stay  : {avg_los:.1f} days")
print(f"Readmission Count    : {readmit_count:,}")
print(f"Readmission Rate     : {readmit_rate:.1f}%")

# DEPARTMENT EARNS THE MOST?
print("\n--- REVENUE BY DEPARTMENT ---")

dept_revenue = df.groupby('Department')['BillAmount'].sum()
dept_revenue = dept_revenue.sort_values(ascending=False)
dept_revenue = dept_revenue.reset_index()
dept_revenue.columns = ['Department', 'Total_Revenue']
dept_revenue['Total_Revenue'] = dept_revenue['Total_Revenue'].round(0)

print(dept_revenue.to_string(index=False))

# PPD
print("\n--- PATIENT PER DEPARTMENT ---")

ppd = df.groupby('Department')['PatientID'].count()
ppd = ppd.sort_values(ascending=False)
ppd = ppd.reset_index()
ppd.columns = ['Department', 'Patient_Count']

print(ppd.to_string(index=False))

# PATIENTS PER DEPARTMENT? 
print("\n--- PATIENT COUNT BY DEPARTMENT ---")

dept_patients = df['Department'].value_counts().reset_index()
dept_patients.columns = ['Department', 'Patient_Count']

print(dept_patients.to_string(index=False))

# AVERAGE BILL AND STAY PER DEPARTMENT 
print("\n--- AVG BILL & LENGTH OF STAY BY DEPARTMENT ---")

dept_avg = df.groupby('Department')[['BillAmount', 'LengthOfStay']].mean().round(2)
dept_avg = dept_avg.sort_values('BillAmount', ascending=False)
dept_avg.columns = ['Avg_Bill_Rs', 'Avg_LOS_Days']

print(dept_avg.to_string())

# DMC
print("\n--- DMC ---")

dmc = df.groupby('Diagnosis')['PatientID'].count()
dmc = dmc.sort_values(ascending=False)
dmc = dmc.reset_index().head(10)
dmc.columns = ['Diagnosis', 'Patient_Count']

print(dmc.to_string(index=False))

# DIAGNOSES ARE MOST COMMON?
print("\n--- TOP 10 DIAGNOSES BY PATIENT COUNT ---")

top_diagnoses = df['Diagnosis'].value_counts().head(10).reset_index()
top_diagnoses.columns = ['Diagnosis', 'Patient_Count']

print(top_diagnoses.to_string(index=False))

# DIAGNOSES COST THE MOST?
print("\n--- TOP 10 DIAGNOSES BY AVERAGE BILL ---")

diag_bill = df.groupby('Diagnosis')['BillAmount'].mean()
diag_bill = diag_bill.sort_values(ascending=False).head(10).round(0)
diag_bill = diag_bill.reset_index()
diag_bill.columns = ['Diagnosis', 'Avg_Bill_Rs']

print(diag_bill.to_string(index=False))

# GENDER BREAKDOWN
print("\n--- GENDER BREAKDOWN ---")

gender_count = df['Gender'].value_counts().reset_index()
gender_count.columns = ['Gender', 'Count']

# % of each gender?
gender_count['Percentage'] = ((gender_count['Count'] / total_patients) * 100).round(1)

print(gender_count.to_string(index=False))

# INSURANCE TYPE ANALYSIS 
print("\n--- REVENUE BY INSURANCE TYPE ---")

insurance = df.groupby('InsuranceType')['BillAmount'].agg(['count', 'sum', 'mean'])
insurance = insurance.sort_values('sum', ascending=False).round(0)
insurance.columns = ['Patient_Count', 'Total_Revenue', 'Avg_Bill']

print(insurance.to_string())


# ADMISSION TYPE BREAKDOWN 
print("\n--- ADMISSION TYPE BREAKDOWN ---")

admission = df['AdmissionType'].value_counts().reset_index()
admission.columns = ['Admission_Type', 'Count']
admission['Percentage'] = ((admission['Count'] / total_patients) * 100).round(1)

print(admission.to_string(index=False))

# READMISSION RATE BY DEPARTMENT 
# Departments which has the most patients coming back within 30 days?
print("\n--- READMISSION RATE BY DEPARTMENT ---")

# Count of total patients per department
total_per_dept = df.groupby('Department')['PatientID'].count()

# Count of readmitted patients per department
readmit_per_dept = df[df['ReadmissionWithin30Days'] == 'Yes'].groupby('Department')['PatientID'].count()

# Rate calculated  
readmit_rate_dept = (readmit_per_dept / total_per_dept * 100).round(1)
readmit_rate_dept = readmit_rate_dept.sort_values(ascending=False).reset_index()
readmit_rate_dept.columns = ['Department', 'Readmission_Rate_%']

print(readmit_rate_dept.to_string(index=False))

# PAYMENT STATUS BREAKDOWN 
print("\n--- PAYMENT STATUS BREAKDOWN ---")

payment = df.groupby('PaymentStatus')['BillAmount'].agg(['count', 'sum']).round(0)
payment = payment.sort_values('sum', ascending=False)
payment.columns = ['Patient_Count', 'Total_Billed_Rs']

print(payment.to_string())

# MONTHLY ADMISSIONS TREND
print("\n--- MONTHLY ADMISSIONS TREND (last 12 months) ---")

monthly = df.groupby(['AdmissionYear', 'MonthNum', 'AdmissionMonth'])['PatientID'].count()
monthly = monthly.reset_index()
monthly = monthly.sort_values(['AdmissionYear', 'MonthNum'])
monthly.columns = ['Year', 'MonthNum', 'Month', 'Admissions']
monthly = monthly.drop(columns='MonthNum')
monthly = monthly.tail(12)

print(monthly.to_string(index=False))

# DISCHARGE STATUS BREAKDOWN 
print("\n--- DISCHARGE STATUS BREAKDOWN ---")

discharge = df['DischargeStatus'].value_counts().reset_index()
discharge.columns = ['Discharge_Status', 'Count']
discharge['Percentage'] = ((discharge['Count'] / total_patients) * 100).round(1)

print(discharge.to_string(index=False))

# SAVING CLEANED DATA
df.to_csv(r"C:\Users\Shru\Downloads\HospitalAnalysis\data\hospital_cleaned.csv",index=False,encoding='utf-8-sig')

 
