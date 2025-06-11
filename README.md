
# 📘 ClauseWise – Legal Document Analyzer

ClauseWise is an AI-powered tool to analyze legal documents like NDAs or contracts by extracting clauses, summarizing them in plain English, and flagging risky terms using LLMs and NLP.

---

## 🚀 Features

- Upload `.pdf` or `.docx` files
- Extract clauses using NLP/regex
- Identify clause type (e.g., Termination, Non-Compete)
- Generate plain English summaries with LLM
- Detect red flags (e.g., exclusivity, auto-renewal)
- Export to CSV, Markdown, or PDF
- Streamlit UI for live interaction

---

## 🛠️ How to Run

streamlit run app/viewer.py
https://drive.google.com/file/d/1zZvmVz4FMVoeiOlqCJ80eAliMh1s3aKK/view?usp=drive_link

## 📁 Folder Structure

```
ClauseWise-LegalAnalyzer/
├── contracts/
│   └── sample_nda.pdf
├── processing/
│   ├── extract_text.py
│   ├── detect_clauses.py
│   └── summarize_and_flag.py
├── outputs/
│   ├── clause_analysis.csv
│   ├── clause_analysis.md
│   └── clause_analysis.pdf
├── app/
│   └── viewer.py
├── notebooks/
│   └── 01_pipeline_overview.ipynb
├── README.md
└── requirements.txt
```

---

## 📄 Sample Output

- `clause_analysis.csv` – Structured output table
- `clause_analysis.md` – Markdown report
- `clause_analysis.pdf` – Printable version (optional)

---

## 🤖 Tech Stack

- Python, Streamlit, pandas
- PyMuPDF or pdfplumber
- Regex + spaCy for clause detection
- OpenAI/Gemini/LLAMA for summaries
