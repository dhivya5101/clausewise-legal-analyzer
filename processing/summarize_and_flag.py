import pandas as pd

def analyze_clauses(clauses):
    """
    Label, summarize, and flag risks for each clause.
    Returns: List of dictionaries with clause details.
    """
    clause_types = {
        "Termination": ["terminate", "cancellation", "end"],
        "Exclusivity": ["exclusive", "sole", "not engage others"],
        "Auto-Renewal": ["auto-renew", "automatic renewal"],
        "Liability": ["liable", "indemnify", "damages"],
        "Definitions": ["definition", "defined as", "means"]
    }
    
    risk_keywords = ["auto-renew", "exclusive", "not engage others", "indemnify"]
    
    results = []
    
    for idx, clause in enumerate(clauses, 1):
        clause_text = clause[:200] + "..." if len(clause) > 200 else clause
        clause_type = "Other"
        summary = "No summary available"
        risk_flag = "❌"

        for c_type, keywords in clause_types.items():
            if any(keyword.lower() in clause.lower() for keyword in keywords):
                clause_type = c_type
                break

        if clause_type == "Termination":
            summary = "Allows ending the agreement with notice."
        elif clause_type == "Exclusivity":
            summary = "Restricts working with other parties."
        elif clause_type == "Auto-Renewal":
            summary = "Agreement renews unless canceled."
        elif clause_type == "Liability":
            summary = "Outlines responsibility for damages."
        elif clause_type == "Definitions":
            summary = "Defines key terms used in the agreement."
        else:
            summary = "General clause, review for specifics."

        if any(keyword.lower() in clause.lower() for keyword in risk_keywords):
            risk_flag = "⚠️"
        
        results.append({
            "Clause Type": clause_type,
            "Original Text (Excerpt)": clause_text,
            "Summary": summary,
            "Risk?": risk_flag
        })
    
    return results

def save_to_csv(results, output_path):
    """
    Save analysis results to CSV.
    """
    if not results:
        print("No results to save.")
        return
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Results saved to {output_path}")

def save_to_markdown(results, output_path):
    """
    Save analysis results to Markdown.
    """
    if not results:
        print("No results to save.")
        return

    headers = list(results[0].keys())
    md_content = "| " + " | ".join(headers) + " |\n"
    md_content += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for result in results:
        row = [str(result[header]) for header in headers]
        md_content += "| " + " | ".join(row) + " |\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Results saved to {output_path}")