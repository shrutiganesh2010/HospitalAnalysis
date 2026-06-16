from sqlalchemy import create_engine
import pandas as pd

df = pd.read_csv(r"C:\Users\Shru\Downloads\HospitalAnalysis\data\hospital_cleaned.csv")

df.columns = df.columns.str.lower().str.replace(' ', '_')
# Step 1: Connect to PostgreSQL
# Replace placeholders with your actual details
username = "postgres"      # default user
password = "password" # the password you set during installation
host = "localhost"         # if running locally
port = "5432"              # default PostgreSQL port
database = "hospital_db"    # the database you created in pgAdmin

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Step 2: Load DataFrame into PostgreSQL
table_name = "hospital_patients"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")
