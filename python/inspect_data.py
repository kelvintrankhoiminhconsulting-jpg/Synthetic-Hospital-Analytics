# Step 1: Initial Data Inspection / Understanding the Dataset.
# ✅ Identified the files
# ✅ Checked row and column counts
# ✅ Looked at column names
# ✅ Opened the data dictionary
# ✅ Identified what the fields mean
# ✅ Identified primary keys and foreign keys
# ✅ Determined the likely grain of each table
# ✅ Mapped how the tables relate
#=====================================================================================

# ===========================================================
# 1. IMPORT LIBRARIES
# ===========================================================

from pathlib import Path
import pandas as pd

# Always work relative to this script's location
data_folder = Path(__file__).resolve().parent

# Verify the environment
print("Pandas Version:", pd.__version__)
print("Working folder:", data_folder)

#=============END OF IMPORT LIBRARIES=========================

# ===========================================================
# 2. LOAD DATA
# ===========================================================

# Folder where this script is located
data_folder = Path(__file__).resolve().parent

patients = pd.read_csv(data_folder / "patients.csv")
encounters = pd.read_csv(data_folder / "encounters.csv")
procedures = pd.read_csv(data_folder / "procedures.csv")
organizations = pd.read_csv(data_folder / "organizations.csv")
payers = pd.read_csv(data_folder / "payers.csv")
data_dictionary = pd.read_csv(data_folder / "data_dictionary.csv")

print("\nAll tables loaded successfully.")

#===========END OF LOAD DATA=========================

# ===========================================================
# 3. TABLE INVENTORY
# ===========================================================

tables = {
    "Patients": patients,
    "Encounters": encounters,
    "Procedures": procedures,
    "Organizations": organizations,
    "Payers": payers,
    "Data Dictionary": data_dictionary
}

print("\n" + "=" * 70)
print("TABLE INVENTORY")
print("=" * 70)

for name, df in tables.items():
    print(f"\n{name}")
    print("-" * 40)
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")

#==================END OF TABLE INVENTORY=================

# =================================================================
# 4. COLUMN INVENTORY----LETS YOU SEE EVERY COLUMN IN EVERY TABLE
# ==================================================================

print("\n" + "=" * 70)
print("COLUMN INVENTORY")
print("=" * 70)

for name, df in tables.items():
    print(f"\n{name}")
    print("-" * 40)
    print(df.columns.tolist())

#==================END OF COLUMN INVENTORY=================

# ===========================================================
# 5. DATA TYPES----THIS IS HOW PANDA SEES EVERY COLUMN
# ===========================================================

# This helps identify:

# dates stored as text

# numeric fields stored as strings

# categorical columns

# ===========================================================

print("\n" + "=" * 70)
print("DATA TYPES")
print("=" * 70)

for name, df in tables.items():
    print(f"\n{name}")
    print("-" * 40)
    print(df.dtypes)

#==================END OF DATA TYPES=================

# ===========================================================
# 6. MISSING VALUES--ONE OF RIST DATA QUALITY CHECKS
# ===========================================================
# Instead of printing every column, this only shows columns that actually contain missing values.
#==========================================================

print("\n" + "=" * 70)
print("MISSING VALUES")
print("=" * 70)

for name, df in tables.items():
    print(f"\n{name}")
    print("-" * 40)

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print("No missing values.")
    else:
        print(missing)

#==================END OF MISSING VALUES=================

# =====================================================================
# 7. DUPLICATE ROW CHECK -----CHECKS WHETHER ENTIRE ROWS ARE DUPLICATED
# =====================================================================
#==This checks for complete duplicate rows only.

print("\n" + "=" * 70)
print("DUPLICATE ROW CHECK")
print("=" * 70)

for name, df in tables.items():
    print(f"{name}: {df.duplicated().sum():,} duplicate rows")

#==================END OF DUPLICATE ROW CHECK=================

# ======================================================================
# 8. UNIQUE VALUE COUNTS--Useful for identifying candidate primary keys.
# =======================================================================

print("\n" + "=" * 70)
print("UNIQUE VALUE COUNTS")
print("=" * 70)

for name, df in tables.items():
    print(f"\n{name}")
    print("-" * 40)

    for column in df.columns:
        unique_count = df[column].nunique(dropna=False)
        print(f"{column}: {unique_count:,}")

#==================END OF UNIQUE VALUE COUNTS=================

# ================================================================================
# 9. PRIMARY KEY VALIDATION---This checks whether an Id column is truly unique.
# ================================================================================
#==Notice something important:

# We're checking whether "Id" exists first.

# That prevents another KeyError.

print("\n" + "=" * 70)
print("PRIMARY KEY VALIDATION")
print("=" * 70)

for name, df in tables.items():

    if "Id" in df.columns:
        unique = df["Id"].nunique()
        rows = len(df)

        print(f"\n{name}")
        print("-" * 40)
        print(f"Rows: {rows:,}")
        print(f"Unique Id values: {unique:,}")

        if unique == rows:
            print("Primary key appears unique.")
        else:
            print("Duplicate Id values found.")

#==================END OF PRIMARY KEY VALIDATION=================

# ===========================================================
# 10. NUMERIC SUMMARY----This profiles all numeric columns.
# ===========================================================
# This gives:

# count

# mean

# standard deviation

# minimum

# quartiles

# maximum

print("\n" + "=" * 70)
print("NUMERIC SUMMARY")
print("=" * 70)

for name, df in tables.items():

    numeric = df.select_dtypes(include="number")

    if not numeric.empty:
        print(f"\n{name}")
        print("-" * 40)
        print(numeric.describe())

#==================END OF NUMERIC SUMMARY=================

# ===========================================================
# 3.1 PATIENTS TABLE OVERVIEW
# ===========================================================

print("\n" + "=" * 70)
print("PATIENTS TABLE OVERVIEW")
print("=" * 70)

print("Shape:", patients.shape)
print("\nFirst 5 Rows:")
print(patients.head())
#==================END OF PATIENTS TABLE OVERVIEW=================

# ===========================================================
# 3.2 PATIENTS COLUMN NAMES
# ===========================================================

print("\nColumn Names:")
print(patients.columns.tolist())
#==================END OF PATIENTS COLUMN NAMES=================

# ===========================================================
# 3.3 PATIENTS DATA TYPES
# ===========================================================

print("\nPatients Data Types")
print("-" * 40)
patients.info()
#==================END OF PATIENTS DATA TYPES=================

# ===========================================================
# 3.4 PATIENT ID VALIDATION
# ===========================================================

id_column = next((col for col in patients.columns if col.lower() == "id"), None)

if id_column:
    print(f"\nID Column Found: {id_column}")
    print(f"Rows: {len(patients):,}")
    print(f"Unique IDs: {patients[id_column].nunique():,}")

    if len(patients) == patients[id_column].nunique():
        print("Patient ID is unique.")
    else:
        print("Duplicate Patient IDs found.")
else:
    print("No ID column found.")

#==================END OF PATIENT ID VALIDATION=================    

# ===========================================================
# 4.1 PATIENTS MISSING VALUES
# ===========================================================

print("\n" + "=" * 70)
print("PATIENTS MISSING VALUES")
print("=" * 70)

missing = patients.isnull().sum()
missing = missing[missing > 0]

if missing.empty:
    print("No missing values found.")
else:
    print(missing)

#==================END OF PATIENTS MISSING VALUES=================

# ===========================================================
# 4.2 PATIENTS DUPLICATE ROWS
# ===========================================================

print("\n" + "=" * 70)
print("PATIENTS DUPLICATE ROWS")
print("=" * 70)

duplicates = patients.duplicated().sum()

print(f"Duplicate Rows: {duplicates:,}")

#==================END OF PATIENTS DUPLICATE ROWS=================

# ===========================================================
# 4.3 DUPLICATE PATIENT IDs
# ===========================================================

print("\n" + "=" * 70)
print("DUPLICATE PATIENT IDs")
print("=" * 70)

id_column = next((col for col in patients.columns if col.lower() == "id"), None)

if id_column:
    duplicate_ids = patients[patients.duplicated(subset=id_column, keep=False)]

    if duplicate_ids.empty:
        print("No duplicate patient IDs found.")
    else:
        print(duplicate_ids[[id_column]].sort_values(by=id_column))

#==================END OF DUPLICATE PATIENT IDs=================

# ===========================================================
# 4.4 CATEGORICAL VALUE CHECK
# ===========================================================

print("\n" + "=" * 70)
print("PATIENTS CATEGORICAL VALUES")
print("=" * 70)

categorical_columns = [
    "GENDER",
    "RACE",
    "ETHNICITY",
    "MARITAL"
]

for col in categorical_columns:
    if col in patients.columns:
        print(f"\n{col}")
        print("-" * 40)
        print(patients[col].value_counts(dropna=False))

#==================END OF CATEGORICAL VALUE CHECK=================

# ===========================================================
# 4.5 DATE FIELD INSPECTION
# ===========================================================

print("\n" + "=" * 70)
print("PATIENTS DATE FIELDS")
print("=" * 70)

date_columns = [
    col for col in patients.columns
    if "DATE" in col.upper()
]

print("Date Columns:", date_columns)

for col in date_columns:
    print(f"\nSample values from {col}")
    print(patients[col].head())

#==================END OF DATE FIELD INSPECTION=================

# ===========================================================
# 5.1 ENCOUNTERS TABLE OVERVIEW
# ===========================================================

print("\n" + "=" * 70)
print("ENCOUNTERS TABLE OVERVIEW")
print("=" * 70)

print("Shape:", encounters.shape)

print("\nFirst 5 Rows:")
print(encounters.head())

#==================END OF ENCOUNTERS TABLE OVERVIEW=================

# ===========================================================
# 5.2 ENCOUNTERS COLUMN INVENTORY
# ===========================================================

print("\nEncounter Columns")
print("-" * 40)

print(encounters.columns.tolist())

#==================END OF ENCOUNTERS COLUMN INVENTORY=================

# ===========================================================
# 5.3 ENCOUNTER PRIMARY KEY VALIDATION
# ===========================================================

print("\n" + "=" * 70)
print("ENCOUNTER PRIMARY KEY")
print("=" * 70)

print("Rows:", len(encounters))
print("Unique Encounter IDs:", encounters["Id"].nunique())

if len(encounters) == encounters["Id"].nunique():
    print("Encounter ID is unique.")
else:
    print("Duplicate Encounter IDs found.")

#==================END OF ENCOUNTER PRIMARY KEY VALIDATION=================

# ===========================================================
# 5.4 ENCOUNTERS -> PATIENTS RELATIONSHIP
# ===========================================================

print("\n" + "=" * 70)
print("ENCOUNTERS -> PATIENTS RELATIONSHIP")
print("=" * 70)

patient_id_col = next((col for col in patients.columns if col.lower() == "id"), None)

matching_patients = encounters["PATIENT"].isin(patients[patient_id_col])

print("Matching Patient IDs:", matching_patients.sum())
print("Total Encounter Records:", len(encounters))
print(f"Match Rate: {matching_patients.mean()*100:.2f}%")

#==================END OF ENCOUNTERS -> PATIENTS RELATIONSHIP=================

# ===========================================================
# 5.5 ENCOUNTERS -> ORGANIZATIONS RELATIONSHIP
# ===========================================================

print("\n" + "=" * 70)
print("ENCOUNTERS -> ORGANIZATIONS RELATIONSHIP")
print("=" * 70)

matching_orgs = encounters["ORGANIZATION"].isin(organizations["Id"])

print("Matching Organizations:", matching_orgs.sum())
print("Total Encounter Records:", len(encounters))
print(f"Match Rate: {matching_orgs.mean()*100:.2f}%")

#==================END OF ENCOUNTERS -> ORGANIZATIONS RELATIONSHIP=================

# ===========================================================
# 5.6 ENCOUNTERS -> PAYERS RELATIONSHIP
# ===========================================================

print("\n" + "=" * 70)
print("ENCOUNTERS -> PAYERS RELATIONSHIP")
print("=" * 70)

matching_payers = encounters["PAYER"].isin(payers["Id"])

print("Matching Payers:", matching_payers.sum())
print("Total Encounter Records:", len(encounters))
print(f"Match Rate: {matching_payers.mean()*100:.2f}%")

#==================END OF ENCOUNTERS -> PAYERS RELATIONSHIP=================

# ===========================================================
# 6.1 PROCEDURES TABLE OVERVIEW
# ===========================================================

print("\n" + "=" * 70)
print("PROCEDURES TABLE OVERVIEW")
print("=" * 70)

print("Shape:", procedures.shape)

print("\nFirst 5 Rows:")
print(procedures.head())

#==================END OF PROCEDURES TABLE OVERVIEW=================

# ===========================================================
# 6.2 PROCEDURES COLUMN INVENTORY
# ===========================================================

print("\nProcedure Columns")
print("-" * 40)
print(procedures.columns.tolist())

#==================END OF PROCEDURES COLUMN INVENTORY=================

# ===========================================================
# 6.3 PROCEDURES -> PATIENTS
# ===========================================================

print("\n" + "=" * 70)
print("PROCEDURES -> PATIENTS")
print("=" * 70)

patient_id_col = next((col for col in patients.columns if col.lower() == "id"), None)

matching_patients = procedures["PATIENT"].isin(patients[patient_id_col])

print("Matching Patient IDs:", matching_patients.sum())
print("Total Procedure Records:", len(procedures))
print(f"Match Rate: {matching_patients.mean()*100:.2f}%")

#==================END OF PROCEDURES -> PATIENTS=================

# ===========================================================
# 6.4 PROCEDURES -> ENCOUNTERS
# ===========================================================

print("\n" + "=" * 70)
print("PROCEDURES -> ENCOUNTERS")
print("=" * 70)

matching_encounters = procedures["ENCOUNTER"].isin(encounters["Id"])

print("Matching Encounter IDs:", matching_encounters.sum())
print("Total Procedure Records:", len(procedures))
print(f"Match Rate: {matching_encounters.mean()*100:.2f}%")

#==================END OF PROCEDURES -> ENCOUNTERS=================

# ===========================================================
# 6.5 PROCEDURES PER ENCOUNTER
# ===========================================================

print("\n" + "=" * 70)
print("PROCEDURES PER ENCOUNTER")
print("=" * 70)

procedures_per_encounter = procedures.groupby("ENCOUNTER").size()

print(procedures_per_encounter.describe())

print("\nTop 10 Encounters with the Most Procedures")
print(procedures_per_encounter.sort_values(ascending=False).head(10))

#==================END OF PROCEDURES PER ENCOUNTER=================


# ===========================================================
# 7. RELATIONSHIP NOTES
# ===========================================================

"""
RELATIONSHIP SUMMARY

Patients (Id)
    1 -> Many Encounters (PATIENT)

Organizations (Id)
    1 -> Many Encounters (ORGANIZATION)

Payers (Id)
    1 -> Many Encounters (PAYER)

Encounters (Id)
    1 -> Many Procedures (ENCOUNTER)

Validation Results
- All foreign keys matched 100%.
- Encounter IDs are unique.
- Patient IDs are unique.
- One encounter can contain multiple procedures.
"""

# ===========================================================
# PHASE 2 - CREATE CLEAN COPIES
# ===========================================================

patients_clean = patients.copy()
encounters_clean = encounters.copy()
procedures_clean = procedures.copy()
organizations_clean = organizations.copy()
payers_clean = payers.copy()

print("\nClean copies created successfully.")

#==================END OF PHASE 2 - CREATE CLEAN COPIES=================

# ===========================================================
# DATA CLEANING LOG
# ===========================================================

cleaning_log = []

print("\nData Cleaning Log Initialized.")

#==================END OF DATA CLEANING LOG=================

# ===========================================================
# STANDARDIZE PATIENT DATE COLUMNS
# ===========================================================

patient_date_columns = [
    col for col in patients_clean.columns
    if "DATE" in col.upper()
]

for col in patient_date_columns:
    patients_clean[col] = pd.to_datetime(
        patients_clean[col],
        errors="coerce"
    )

print("Patient date columns converted:", patient_date_columns)

#==================END OF STANDARDIZE PATIENT DATE COLUMNS=================
#=====EXAMPLE OF CLEANING LOG===================
cleaning_log.append({
    "Table": "Patients",
    "Issue": "Missing DEATHDATE",
    "Action": "Retained NULL values because they likely represent living patients."
})

# ===========================================================
# CLEAN ORGANIZATION TEXT FIELDS
# ===========================================================

text_columns = organizations_clean.select_dtypes(include=["object", "string"]).columns

for col in text_columns:
    organizations_clean[col] = organizations_clean[col].str.strip()

#==================END OF CLEAN ORGANIZATION TEXT FIELDS=================

# ===========================================================
# VALIDATE CLEAN PATIENT IDs
# ===========================================================

id_column = next((c for c in patients_clean.columns if c.lower() == "id"), None)

print("Rows:", len(patients_clean))
print("Unique IDs:", patients_clean[id_column].nunique())

#==================END OF VALIDATE CLEAN PATIENT IDs=================

#===========================================================
#PREVIEW BEFORE EXPORT TO POWER BI
#===========================================================

print(patients_clean.head())
print(encounters_clean.head())

#==================END OF PREVIEW BEFORE EXPORT TO POWER BI=================

# ===========================================================
# 8.3 STANDARDIZE TEXT FIELDS
# ===========================================================

clean_tables = {
    "Patients": patients_clean,
    "Encounters": encounters_clean,
    "Procedures": procedures_clean,
    "Organizations": organizations_clean,
    "Payers": payers_clean
}

for table_name, df in clean_tables.items():

    text_columns = df.select_dtypes(include=["object", "string"]).columns

    for col in text_columns:
        df[col] = df[col].str.strip()

print("Text fields standardized across all tables.")

#==================END OF STANDARDIZE TEXT FIELDS=================

# ===========================================================
# 8.4 CATEGORICAL CONSISTENCY CHECK
# ===========================================================

categorical_columns = [
    "GENDER",
    "RACE",
    "ETHNICITY",
    "MARITAL"
]

for col in categorical_columns:

    if col in patients_clean.columns:

        print("\n" + "=" * 40)
        print(col)
        print("=" * 40)

        print(patients_clean[col].value_counts(dropna=False))

#==================END OF CATEGORICAL CONSISTENCY CHECK=================
# ===========================================================
# 8.5 INVALID DATE CHECK
# ===========================================================

for col in patient_date_columns:

    invalid_dates = patients_clean[col].isna().sum()

    print(f"{col}: {invalid_dates:,} missing/invalid values")

#==================END OF INVALID DATE CHECK=================

# ===========================================================
# 9.1 PATIENT DATE VALIDATION
# ===========================================================

print("\n" + "=" * 70)
print("PATIENT DATE VALIDATION")
print("=" * 70)

invalid_patient_dates = patients_clean[
    (patients_clean["DEATHDATE"].notna()) &
    (patients_clean["DEATHDATE"] < patients_clean["BIRTHDATE"])
]

print(f"Invalid Patient Date Records: {len(invalid_patient_dates):,}")

if not invalid_patient_dates.empty:
    print(invalid_patient_dates[["BIRTHDATE", "DEATHDATE"]].head())

#==================END OF PATIENT DATE VALIDATION=================

    # ===========================================================
# 9.2 ENCOUNTER DATE VALIDATION
# ===========================================================

print("\n" + "=" * 70)
print("ENCOUNTER DATE VALIDATION")
print("=" * 70)

invalid_encounters = encounters_clean[
    encounters_clean["STOP"] < encounters_clean["START"]
]

print(f"Encounters Ending Before They Started: {len(invalid_encounters):,}")

if not invalid_encounters.empty:
    print(invalid_encounters[["START", "STOP"]].head())

#==================END OF ENCOUNTER DATE VALIDATION=================

# ===========================================================
# 9.3 FINANCIAL VALIDATION
# ===========================================================

print("\n" + "=" * 70)
print("FINANCIAL VALIDATION")
print("=" * 70)

cost_columns = [
    "BASE_ENCOUNTER_COST",
    "TOTAL_CLAIM_COST",
    "PAYER_COVERAGE"
]

for col in cost_columns:

    negative = (encounters_clean[col] < 0).sum()

    print(f"{col}: {negative:,} negative values")

#==================END OF FINANCIAL VALIDATION=================

# ===========================================================
# 9.4 PAYER COVERAGE VALIDATION
# ===========================================================

print("\n" + "=" * 70)
print("PAYER COVERAGE VALIDATION")
print("=" * 70)

coverage_errors = encounters_clean[
    encounters_clean["PAYER_COVERAGE"] >
    encounters_clean["TOTAL_CLAIM_COST"]
]

print(f"Coverage Greater Than Total Claim: {len(coverage_errors):,}")

if not coverage_errors.empty:
    print(coverage_errors[
        ["PAYER_COVERAGE", "TOTAL_CLAIM_COST"]
    ].head())

#==================END OF PAYER COVERAGE VALIDATION=================

# ===========================================================
# 9.5 PROCEDURE DATE VALIDATION
# ===========================================================

# ===========================================================
# CONVERT PROCEDURE DATES
# ===========================================================

procedures_clean["START"] = pd.to_datetime(
    procedures_clean["START"],
    errors="coerce"
)

procedures_clean["STOP"] = pd.to_datetime(
    procedures_clean["STOP"],
    errors="coerce"
)

#==================END OF PROCEDURE DATE VALIDATION==========
# ===========================================================
# PROCEDURES -> ENCOUNTERS DATE VALIDATION
# ===========================================================

procedure_dates = procedures_clean.merge(
    encounters_clean[["Id", "START", "STOP"]],
    left_on="ENCOUNTER",
    right_on="Id",
    how="left",
    suffixes=("_PROC", "_ENC")
)

outside_encounter = procedure_dates[
    (procedure_dates["START_PROC"] < procedure_dates["START_ENC"]) |
    (procedure_dates["STOP_PROC"] > procedure_dates["STOP_ENC"])
]

print("\n" + "=" * 70)
print("PROCEDURE DATE VALIDATION")
print("=" * 70)

print(f"Procedures Outside Encounter Window: {len(outside_encounter):,}")

if not outside_encounter.empty:
    print(outside_encounter[
        ["ENCOUNTER", "START_PROC", "STOP_PROC", "START_ENC", "STOP_ENC"]
    ].head())

#==================END OF PROCEDURES -> ENCOUNTERS DATE VALIDATION=================
cleaning_log.append({
    "Table": "Encounters",
    "Issue": "Negative costs",
    "Action": "Investigate before cleaning."
})
#==================END OF CLEANING LOG ENTRY=================
# ===========================================================
# 10.1 DATA QUALITY REPORT
# ===========================================================

print("\n" + "=" * 70)
print("DATA QUALITY REPORT")
print("=" * 70)

quality_report = []

for name, df in clean_tables.items():

    # Find an ID column if one exists
    id_col = next((c for c in df.columns if c.lower() == "id"), None)

    quality_report.append({
        "Table": name,
        "Rows": len(df),
        "Columns": df.shape[1],
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Primary Key Unique":
            id_col is not None and df[id_col].nunique() == len(df)
    })

quality_report = pd.DataFrame(quality_report)

print(quality_report)

#==================END OF DATA QUALITY REPORT=================
# ===========================================================
# 10.2 TABLES NEEDING REVIEW
# ===========================================================

print("\n" + "=" * 70)
print("TABLES NEEDING REVIEW")
print("=" * 70)

needs_review = quality_report[
    (quality_report["Missing Values"] > 0) |
    (quality_report["Duplicate Rows"] > 0) |
    (quality_report["Primary Key Unique"] == False)
]

if needs_review.empty:
    print("All tables passed the validation checks.")
else:
    print(needs_review)

#==================END OF TABLES NEEDING REVIEW=================
# ===========================================================
# 10.3 SAVE DATA QUALITY REPORT
# ===========================================================

processed_folder = data_folder / "processed"
processed_folder.mkdir(exist_ok=True)

quality_report.to_csv(
    processed_folder / "data_quality_report.csv",
    index=False
)

print("Data Quality Report saved.")

#==================END OF SAVE DATA QUALITY REPORT=================
# ===========================================================
# 10.4 EXPORT CLEANED TABLES
# ===========================================================

patients_clean.to_csv(processed_folder / "patients_clean.csv", index=False)
encounters_clean.to_csv(processed_folder / "encounters_clean.csv", index=False)
procedures_clean.to_csv(processed_folder / "procedures_clean.csv", index=False)
organizations_clean.to_csv(processed_folder / "organizations_clean.csv", index=False)
payers_clean.to_csv(processed_folder / "payers_clean.csv", index=False)

print("Cleaned tables exported successfully.")

#==================END OF EXPORT CLEANED TABLES=================


    




















