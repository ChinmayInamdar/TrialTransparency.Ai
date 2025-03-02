#!/usr/bin/env python3
"""
Data validation script for clinical trials.
This script connects to the PostgreSQL database and performs checks on the studies,
sponsors, and interventions tables to ensure data integrity.
"""

import psycopg2

def validate_studies(conn):
    with conn.cursor() as cur:
        # Count studies with missing title
        cur.execute("SELECT COUNT(*) FROM studies WHERE title IS NULL OR title = ''")
        missing_titles = cur.fetchone()[0]
        print(f"Studies with missing title: {missing_titles}")

        # Count studies with missing nct_id
        cur.execute("SELECT COUNT(*) FROM studies WHERE nct_id IS NULL OR nct_id = ''")
        missing_nct = cur.fetchone()[0]
        print(f"Studies with missing nct_id: {missing_nct}")

        # Count studies with missing overall_status
        cur.execute("SELECT COUNT(*) FROM studies WHERE overall_status IS NULL OR overall_status = ''")
        missing_status = cur.fetchone()[0]
        print(f"Studies with missing overall_status: {missing_status}")

def validate_sponsors(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM sponsors WHERE sponsor_name IS NULL OR sponsor_name = ''")
        missing_sponsors = cur.fetchone()[0]
        print(f"Sponsors with missing sponsor_name: {missing_sponsors}")

def validate_interventions(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM interventions WHERE name IS NULL OR name = ''")
        missing_interventions = cur.fetchone()[0]
        print(f"Interventions with missing name: {missing_interventions}")

def run_validations():
    conn = psycopg2.connect(
        host="localhost",
        database="edi_clinicaltrials",
        user="ediuser",
        password="12345"
    )
    print("Running data validation checks...\n")
    validate_studies(conn)
    validate_sponsors(conn)
    validate_interventions(conn)
    conn.close()
    print("\nData validation complete.")

if __name__ == "__main__":
    run_validations()

