# TrialTransparency.Ai 🧪🔍  
*Hybrid Rules-Based + LLM-Powered Clinical Trial Data Validation Engine*

![Logo Placeholder](images/logo.png)

## 🚀 Overview

**TrialTransparency.Ai** is an open-source system purpose-built for scalable, explainable, and regulation-compliant **clinical trial data validation**. It leverages a hybrid architecture combining **deterministic rules-based checks** with **LLM-enhanced anomaly explanations**, significantly reducing the time, effort, and complexity involved in trial data cleaning.

- ✅ 94.7% Accuracy on structured anomaly detection  
- ⚡ 78.3% Reduction in validation processing time  
- 📊 Tailored, role-specific explanations via LLMs (Mixtral-8x7 B)  
- 🔒 Compliant with FDA 21 CFR Part 11, ICH GCP, GDPR

---

## 💡 Key Features

| Module | Description |
|--------|-------------|
| 🧩 **ETL + Preprocessing** | Efficiently loads XML from ClinicalTrials.gov using memory-optimized, schema-aware routines |
| ✅ **Rules-Based Validator** | Field-level, format, logical, and reference validation using 389+ deterministic rules |
| 🧠 **LLM Explainability Engine** | Uses Mixtral-8x7B-Instruct to generate natural-language, stakeholder-specific error justifications |
| 🧭 **Edge Case Handling** | Auto-escalation, severity scoring, outlier detection (Z-score, IQR), and human-in-the-loop handoffs |
| 🚀 **Performance Optimizations** | Chunked processing, caching, multithreading, and memory-aware design for large-scale datasets |

---

## 📊 Performance Highlights

### 🔎 Error Detection Accuracy
| Error Type               | F1 Score | vs Traditional (%) |
|--------------------------|----------|---------------------|
| Missing Fields           | 99.75%   | +2.4%               |
| Format Inconsistencies   | 98.5%    | +8.7%               |
| Logical Contradictions   | 93.4%    | +17.3%              |
| Cross-Record Issues      | 89.8%    | +21.8%              |
| Reference Mismatches     | 94.7%    | +15.2%              |

### ⚙️ Efficiency Benchmarks

| Task | Manual (min) | TrialTransparency.Ai (min) |
|------|--------------|----------------------------|
| Error Identification | 5.7 | 0.03 |
| Error Interpretation | 12.3 | 2.8 |
| Resolution Planning | 8.5 | 1.9 |
| Documentation | 7.2 | 1.6 |
| **Total** | **33.7** | **6.3** ⏱️ |

> 📈 ~78% faster resolution workflows with higher accuracy and transparency.

---

## 🏗️ Architecture

![System Diagram Placeholder](images/system_architecture.png)

1. **Data Ingestion** → XML parsing, dtype optimization, standardization  
2. **Validation Engine** → Rule-based logic covering structure, logic, cross-fields, and ontologies  
3. **Explainability Layer** → Generates explanations tailored to roles: Data Manager, Regulator, Clinician  
4. **Anomaly Handler** → Categorizes severity, detects outliers, escalates ambiguous cases  
5. **Performance Layer** → Chunked + parallel processing with intelligent caching

---

## ⚙️ Tech Stack

| Layer            | Tools |
|------------------|-------|
| Language & Parsing | Python, xml.etree.ElementTree, re |
| Data Storage     | PostgreSQL + psycopg2 |
| AI / NLP         | Hugging Face Transformers, Mixtral-8x7B |
| Scheduling       | Apache Airflow, Cron |
| Containers       | Docker |
| Interface        | REST APIs (planned) |## 🧪 Reproducing Results

Download clinical trial data XMLs from [ClinicalTrials.gov](https://clinicaltrials.gov)

1. Preprocess using `trial_loader.py`
2. Validate via `validator_core.py`
3. Generate explanations using `explanation_engine.py`
4. Review reports in `output/`

```bash
python3 trial_loader.py --input trials_raw.xml
python3 validator_core.py --input processed.csv
python3 explanation_engine.py --input validated.json
```

---

## 🔧 Installation

```bash
git clone https://github.com/yourusername/TrialTransparency.Ai.git
cd TrialTransparency.Ai
docker build -t trialtransparency .
docker run -p 8080:8080 trialtransparency
```
## 📌 Use Cases

- 🏥 **CROs and Sponsors** needing faster data cleaning  
- 📊 **Data Managers** resolving errors at scale  
- 🧾 **Regulatory Affairs** preparing audit-ready documentation  
- 🌍 **Global Trials** handling multi-country compliance  

---

## 🔮 Roadmap

- [ ] Real-time **eCRF integration**  
- [ ] **Lay Summary Generation** (patient-friendly output)  
- [ ] **Multilingual explanations**  
- [ ] **Cross-trial inconsistency detection**  

---

## 📷 Sample Screenshots / Visuals

> Replace below with actual images

![ETL Pipeline](images/pipeline_overview.png)  
*End-to-end ETL + Validation Pipeline*

![LLM Explanations](images/explanation_output.png)  
*Role-specific LLM-generated error messages*

---

## 👩‍⚕️ Authors

- **Arya Doshi**  
- **Chinmay Inamdar**  
- **Tanmay Gote**  
- **Swati Shilaskar**  

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 💬 Contact / Contributions

We welcome feedback, feature requests, and contributions.

- 📨 [arya.doshi22@vit.edu](mailto:arya.doshi22@vit.edu)  
- 🤝 Open issues or submit PRs on [GitHub](https://github.com/yourusername/TrialTransparency.Ai)


