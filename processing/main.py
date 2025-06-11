import os
from extract_text import extract_text
from detect_clauses import detect_clauses
from summarize_and_flag import analyze_clauses, save_to_csv, save_to_markdown

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTRACTS_DIR = os.path.join(BASE_DIR, "..", "contracts")
OUTPUTS_DIR = os.path.join(BASE_DIR, "..", "outputs")
SAMPLE_CONTRACT = os.path.join(CONTRACTS_DIR, "sample_nda.pdf")
OUTPUT_CSV = os.path.join(OUTPUTS_DIR, "clause_analysis.csv")
OUTPUT_MD = os.path.join(OUTPUTS_DIR, "clause_analysis.md")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(CONTRACTS_DIR, exist_ok=True)

def main():
    if not os.path.exists(SAMPLE_CONTRACT):
        print(f"Error: Sample contract not found at {SAMPLE_CONTRACT}")
        print("Please place a valid text-based PDF named 'sample_nda.pdf' in the contracts/ folder.")
        print("Create one with the provided NDA content or download from:")
        print("- PandaDoc: https://www.pandadoc.com/non-disclosure-agreement-template/")
        print("- LegalTemplates: https://legaltemplates.net/form/non-disclosure-agreement/")
        return

    print("Extracting text...")
    text = extract_text(SAMPLE_CONTRACT)
    if not text:
        print("No text extracted. Check if the PDF is text-based or try a .docx file.")
        return

    print("Detecting clauses...")
    clauses = detect_clauses(text)
    if not clauses:
        print("No clauses detected. Ensure the document has numbered sections (e.g., '1.', '2.1').")
        return
    print("Analyzing clauses...")
    results = analyze_clauses(clauses)

    print("Saving results...")
    save_to_csv(results, OUTPUT_CSV)
    save_to_markdown(results, OUTPUT_MD)

if __name__ == "__main__":
    main()