import streamlit as st
import os
import sys
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io
import tempfile

app_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(app_dir)

processing_dir = os.path.join(base_dir, 'processing')
sys.path.append(processing_dir)
st.write(f"Debug: Added {processing_dir} to sys.path") 

if not os.path.exists(os.path.join(processing_dir, 'extract_text.py')):
    st.error("Error: extract_text.py not found in processing directory.")
if not os.path.exists(os.path.join(processing_dir, 'detect_clauses.py')):
    st.error("Error: detect_clauses.py not found in processing directory.")
if not os.path.exists(os.path.join(processing_dir, 'summarize_and_flag.py')):
    st.error("Error: summarize_and_flag.py not found in processing directory.")

from extract_text import extract_text
from detect_clauses import detect_clauses
from summarize_and_flag import analyze_clauses, save_to_csv, save_to_markdown

st.title("ClauseWise - Legal Document Analyzer")
st.write(f"Current Date and Time: 07:17 PM IST, Friday, May 30, 2025")

uploaded_files = st.file_uploader("Upload one or more .pdf or .docx files", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    all_results = []

    with tempfile.TemporaryDirectory() as temp_contracts_dir, tempfile.TemporaryDirectory() as temp_outputs_dir:
        for idx, uploaded_file in enumerate(uploaded_files):
            st.write(f"### Processing File {idx + 1}: {uploaded_file.name}")
            file_path = os.path.join(temp_contracts_dir, uploaded_file.name)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            text = extract_text(file_path)
            if not text:
                st.error(f"No text extracted from {uploaded_file.name}. Ensure the file is text-based.")
                continue
            
            clauses = detect_clauses(text)
            if not clauses:
                st.error(f"No clauses detected in {uploaded_file.name}. Ensure the document has numbered sections (e.g., '1.', '2.1').")
                continue
            
            results = analyze_clauses(clauses)
            for result in results:
                result["Source File"] = uploaded_file.name
            all_results.extend(results)

            st.write(f"#### Analysis for {uploaded_file.name}")
            st.dataframe(results)

        if all_results:
            csv_path = os.path.join(temp_outputs_dir, "clause_analysis.csv")
            md_path = os.path.join(temp_outputs_dir, "clause_analysis.md")

            combined_results = pd.DataFrame(all_results)
            cols = ["Source File"] + [col for col in combined_results.columns if col != "Source File"]
            combined_results = combined_results[cols]

            save_to_csv(combined_results.to_dict('records'), csv_path)
            save_to_markdown(combined_results.to_dict('records'), md_path)

            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            elements = []

            styles = getSampleStyleSheet()
            elements.append(Paragraph("ClauseWise Analysis Report", styles['Title']))
            elements.append(Paragraph("Generated on: 09:11 PM IST, Thursday, May 22, 2025", styles['Normal']))
            elements.append(Spacer(1, 12))

            data = [cols]
            for _, row in combined_results.iterrows():
                data.append([str(row[col]) for col in cols])

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('WORDWRAP', (0, 0), (-1, -1), True),
            ]))
            elements.append(table)

            doc.build(elements)
            pdf_buffer.seek(0)

            st.write("### Download Analysis Report")
            st.download_button(
                label="Download Analysis as PDF (Auto-triggered)",
                data=pdf_buffer,
                file_name="clause_analysis_report.pdf",
                mime="application/pdf",
                key="auto_download_pdf",
                on_click=lambda: st.session_state.update({"download_triggered": True})
            )

            with open(csv_path, "rb") as f:
                st.download_button("Download Combined CSV", f, "clause_analysis.csv")
            with open(md_path, "rb") as f:
                st.download_button("Download Combined Markdown", f, "clause_analysis.md")
else:
    st.info("Please upload one or more files to analyze.")