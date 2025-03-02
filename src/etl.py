#!/usr/bin/env python3
"""
ETL script that recursively processes all XML files under /home/chinmay/edi/data,
parses clinical study information, and inserts the records into PostgreSQL.
Includes error handling and rollback for each file.
"""

import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime
import psycopg2

def parse_date(raw_date):
    """
    Given a raw download_date string like:
    "ClinicalTrials.gov processed this data on February 28, 2025",
    extract and return a datetime.date object.
    Returns None if parsing fails.
    """
    # Use regex to extract the date part after the word "on"
    match = re.search(r'on\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})', raw_date)
    if match:
        date_str = match.group(1)
        try:
            parsed_date = datetime.strptime(date_str, '%B %d, %Y').date()
            return parsed_date
        except Exception as e:
            return None
    else:
        return None

def parse_clinical_study(xml_file):
    """
    Parse a clinical study XML file and extract key fields.
    Returns three dictionaries: study, sponsor, and intervention.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    study = {}
    sponsor = {}
    intervention = {}

    # --- Extract study fields ---
    # nct_id from <id_info>
    id_info = root.find('id_info')
    if id_info is not None:
        nct_id_elem = id_info.find('nct_id')
        if nct_id_elem is not None and nct_id_elem.text:
            study['nct_id'] = nct_id_elem.text.strip()

    # title from <brief_title>
    brief_title_elem = root.find('brief_title')
    if brief_title_elem is not None and brief_title_elem.text:
        study['title'] = brief_title_elem.text.strip()

    # brief_summary from <brief_summary>/<textblock>
    brief_summary_elem = root.find('brief_summary')
    if brief_summary_elem is not None:
        textblock_elem = brief_summary_elem.find('textblock')
        if textblock_elem is not None and textblock_elem.text:
            study['brief_summary'] = textblock_elem.text.strip()
        else:
            study['brief_summary'] = None
    else:
        study['brief_summary'] = None

    # overall_status from <overall_status>
    overall_status_elem = root.find('overall_status')
    if overall_status_elem is not None and overall_status_elem.text:
        study['overall_status'] = overall_status_elem.text.strip()

    # study_type from <study_type>
    study_type_elem = root.find('study_type')
    if study_type_elem is not None and study_type_elem.text:
        study['study_type'] = study_type_elem.text.strip()

    # updated_date from <required_header>/<download_date>
    required_header = root.find('required_header')
    if required_header is not None:
        download_date_elem = required_header.find('download_date')
        if download_date_elem is not None and download_date_elem.text:
            raw_date = download_date_elem.text.strip()
            study['download_date'] = parse_date(raw_date)
        else:
            study['download_date'] = None
    else:
        study['download_date'] = None

    # --- Extract sponsor fields ---
    sponsors_elem = root.find('sponsors')
    if sponsors_elem is not None:
        lead_sponsor = sponsors_elem.find('lead_sponsor')
        if lead_sponsor is not None:
            agency_elem = lead_sponsor.find('agency')
            if agency_elem is not None and agency_elem.text:
                sponsor['sponsor_name'] = agency_elem.text.strip()
            agency_class_elem = lead_sponsor.find('agency_class')
            if agency_class_elem is not None and agency_class_elem.text:
                sponsor['sponsor_type'] = agency_class_elem.text.strip()

    # --- Extract intervention fields ---
    intervention_elem = root.find('intervention')
    if intervention_elem is not None:
        intervention_type_elem = intervention_elem.find('intervention_type')
        if intervention_type_elem is not None and intervention_type_elem.text:
            intervention['intervention_type'] = intervention_type_elem.text.strip()
        intervention_name_elem = intervention_elem.find('intervention_name')
        if intervention_name_elem is not None and intervention_name_elem.text:
            intervention['intervention_name'] = intervention_name_elem.text.strip()

    return study, sponsor, intervention

def insert_into_db(study, sponsor, intervention, conn):
    """
    Insert the parsed data into the database in its own mini-transaction.
    Rolls back on error to ensure subsequent files can be processed.
    """
    try:
        with conn.cursor() as cur:
            # Insert into studies table (including brief_summary and download_date as date)
            cur.execute(
                """
                INSERT INTO studies (
                    nct_id,
                    title,
                    brief_summary,
                    overall_status,
                    study_type,
                    updated_date
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    study.get('nct_id'),
                    study.get('title'),
                    study.get('brief_summary'),
                    study.get('overall_status'),
                    study.get('study_type'),
                    study.get('download_date')
                )
            )
            study_id = cur.fetchone()[0]

        if sponsor.get('sponsor_name'):
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO sponsors (study_id, sponsor_name, sponsor_type)
                    VALUES (%s, %s, %s);
                    """,
                    (study_id, sponsor['sponsor_name'], sponsor.get('sponsor_type'))
                )

        if intervention.get('intervention_name'):
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO interventions (study_id, intervention_type, name)
                    VALUES (%s, %s, %s);
                    """,
                    (
                        study_id,
                        intervention.get('intervention_type'),
                        intervention.get('intervention_name')
                    )
                )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

def process_xml_files(data_dir, conn):
    """
    Recursively process all XML files under data_dir and its subdirectories.
    Performs basic validation for required fields and logs errors.
    """
    for root_dir, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".xml"):
                filepath = os.path.join(root_dir, file)
                try:
                    study, sponsor, intervention = parse_clinical_study(filepath)

                    # Basic validation: Ensure nct_id and title are present.
                    if not study.get('nct_id'):
                        print(f"Skipping {filepath}: Missing nct_id")
                        continue
                    if not study.get('title'):
                        print(f"Skipping {filepath}: Missing title")
                        continue

                    insert_into_db(study, sponsor, intervention, conn)
                    print(f"Processed {filepath}")

                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    conn = psycopg2.connect(
        host="localhost",
        database="edi_clinicaltrials",
        user="ediuser",
        password="12345"
    )

    data_dir = "/home/chinmay/edi/data"
    process_xml_files(data_dir, conn)
    conn.close()

