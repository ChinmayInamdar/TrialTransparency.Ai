#!/usr/bin/env python3
"""
Draft report script that retrieves all clinical trial records from the database,
generates a comprehensive, structured clinical trial report for each using a Hugging Face
text-generation model (GPT-2), and saves each report as a text file in a 'reports' folder.
"""

import os
import psycopg2
from transformers import pipeline

def get_all_trial_ids(conn):
    """Retrieve a list of all nct_ids from the studies table."""
    with conn.cursor() as cur:
        cur.execute("SELECT nct_id FROM studies;")
        trial_ids = [row[0] for row in cur.fetchall()]
    return trial_ids

def get_trial_summary(conn, nct_id):
    """
    Retrieve the clinical trial title and brief_summary for the given nct_id.
    Returns a dictionary with 'title' and 'brief_summary', or None if not found.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT title, brief_summary
            FROM studies
            WHERE nct_id = %s;
            """,
            (nct_id,)
        )
        result = cur.fetchone()
    if result:
        return {"title": result[0], "brief_summary": result[1]}
    else:
        return None

def generate_report(trial_data, generator):
    """
    Generate a draft clinical trial report using the provided trial data and text-generation model.
    This version uses an updated prompt that instructs the model to create a complete, structured report
    with the following sections:
      1. Objectives
      2. Methods
      3. Results
      4. Conclusions
      5. Acknowledgments
      6. References
    The function calculates the remaining token budget so that the total tokens do not exceed GPT-2's max context of 1024.
    """
    prompt = (
        f"Clinical Trial Title: {trial_data.get('title', '')}\n\n"
        f"Brief Summary: {trial_data.get('brief_summary', '')}\n\n"
        "Draft a comprehensive clinical trial report that includes the following sections:\n"
        "1. Objectives\n"
        "2. Methods\n"
        "3. Results\n"
        "4. Conclusions\n"
        "5. Acknowledgments\n"
        "6. References\n\n"
        "Ensure that each section is clearly labeled and contains detailed, structured information."
    )
    
    # Get the tokenizer to determine prompt token length
    tokenizer = generator.tokenizer
    tokens = tokenizer(prompt, return_tensors="pt", truncation=True)
    input_length = tokens.input_ids.shape[-1]
    
    max_context = 1024  # GPT-2 maximum context length
    # Calculate available tokens for generation
    max_new = max_context - input_length
    # Use a lower cap if available tokens exceed a safe generation length (e.g., 800 tokens)
    if max_new > 800:
        max_new = 800
    # Fallback: ensure at least some tokens are generated
    if max_new <= 0:
        max_new = 50

    report = generator(
        prompt,
        max_new_tokens=max_new,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        truncation=True
    )
    return report[0]['generated_text']

def save_report(nct_id, report_text, reports_dir):
    """
    Save the generated report to a text file in the specified reports directory.
    The file will be named as 'report_<nct_id>.txt'.
    """
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    filename = os.path.join(reports_dir, f"report_{nct_id}.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report_text)

if __name__ == "__main__":
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        database="edi_clinicaltrials",
        user="ediuser",
        password="12345"
    )
    
    # Initialize the text-generation pipeline with GPT-2
    generator = pipeline('text-generation', model='gpt2')
    
    # Retrieve all trial nct_ids from the database
    trial_ids = get_all_trial_ids(conn)
    print(f"Found {len(trial_ids)} trials in the database.")
    
    # Define the directory to store generated reports
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports")
    
    # Generate and save a report for each trial
    for nct_id in trial_ids:
        trial_data = get_trial_summary(conn, nct_id)
        if trial_data:
            report_text = generate_report(trial_data, generator)
            save_report(nct_id, report_text, reports_dir)
            print(f"Generated report for {nct_id}")
        else:
            print(f"No data found for trial with nct_id: {nct_id}")
    
    conn.close()

