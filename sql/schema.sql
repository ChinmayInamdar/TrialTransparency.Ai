-- Create table for clinical studies
CREATE TABLE studies (
    id SERIAL PRIMARY KEY,
    nct_id VARCHAR(20) UNIQUE NOT NULL,
    title TEXT,
    status VARCHAR(50),
    study_type VARCHAR(50),
    start_date DATE,
    completion_date DATE,
    updated_date DATE
);

-- Create table for interventions related to studies
CREATE TABLE interventions (
    id SERIAL PRIMARY KEY,
    study_id INTEGER REFERENCES studies(id) ON DELETE CASCADE,
    intervention_type VARCHAR(50),
    name TEXT
);

-- Create table for study outcomes
CREATE TABLE outcomes (
    id SERIAL PRIMARY KEY,
    study_id INTEGER REFERENCES studies(id) ON DELETE CASCADE,
    outcome_type VARCHAR(50),
    description TEXT,
    measure TEXT
);

-- Create table for study sponsors
CREATE TABLE sponsors (
    id SERIAL PRIMARY KEY,
    study_id INTEGER REFERENCES studies(id) ON DELETE CASCADE,
    sponsor_name TEXT,
    sponsor_type VARCHAR(50)
);
