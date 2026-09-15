# Synthetic Hospital Analytics

## Project Overview

This project analyzes a synthetic hospital and patient records dataset using Python, pandas, Power BI, and DAX.

The goal of the project was to practice an end-to-end data analytics workflow, including data inspection, data quality validation, data cleaning, relational data modeling, and interactive dashboard development.

## Tools Used

- Python
- pandas
- Power BI
- DAX
- GitHub

## Dataset

The dataset contains five related tables. The original source data is synthetic and was processed locally using Python and pandas. Cleaned datasets used for the Power BI analysis are included in this repository.

- **Patients** - patient demographic and geographic information
- **Encounters** - patient healthcare encounters and associated costs
- **Procedures** - procedures performed during encounters
- **Organizations** - healthcare organization information
- **Payers** - insurance payer information

The data is synthetic and is used for learning and portfolio development.

## Data Preparation with Python

Python and pandas were used to inspect and prepare the data before loading it into Power BI.

The data preparation workflow included:

1. Loading the CSV files
2. Inspecting table and column structure
3. Reviewing data types
4. Checking missing values
5. Checking duplicate records
6. Validating primary keys
7. Validating foreign-key relationships
8. Checking table relationships and cardinality
9. Standardizing text fields
10. Converting date fields
11. Validating business rules
12. Exporting cleaned datasets for Power BI

### Data Quality Checks

Examples of validation performed include:

- Primary key uniqueness
- Foreign-key match rates
- Duplicate record detection
- Birth date occurring before death date
- Encounter start occurring before encounter end
- Negative financial values
- Payer coverage compared with total claim cost
- Procedures occurring within the associated encounter period

## Power BI Dashboard

The cleaned datasets were imported into Power BI and connected using relational data modeling.

### Dashboard Preview

![Hospital Analytics Dashboard](screenshots/dashboard.png)

### Key Performance Indicators

The dashboard includes the following KPIs:

- Total Patients
- Total Encounters
- Total Procedures
- Average Encounter Cost
- Total Claim Cost

### Dashboard Visualizations

The dashboard includes:

- Patient encounters by patient
- Patient gender distribution
- Encounters over time
- Top procedures
- Claim cost analysis

### Interactive Filters

Users can filter the dashboard by:

- Month
- Encounter Class
- Payer
- Gender

These filters dynamically update the dashboard's KPIs and visualizations.

## Data Model

The Power BI model uses the following relationships:

```text
Patients
    |
    | 1 : *
    v
Encounters
    |
    | 1 : *
    v
Procedures

Organizations
    |
    | 1 : *
    v
Encounters

Payers
    |
    | 1 : *
    v
Encounters
