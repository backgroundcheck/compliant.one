# app.py
import streamlit as st
import pandas as pd
from fuzzywuzzy import process
from fpdf import FPDF
import datetime

# === PAGE CONFIG ===
st.set_page_config(page_title="Compliant.one", layout="wide")

# === APP HEADER ===
st.title("🛡️ Compliant.one")
st.subheader("Threat & Compliance Intelligence Screening")

st.markdown("""
This is the MVP version of Compliant.one.  
It screens individuals or organizations against:
- Sanctions lists
- PEP watchlists
- Adverse media mentions

Enter a name to start.
""")

# === LOAD MOCK DATA ===
try:
    df = pd.read_csv("data/entities.csv")
except FileNotFoundError:
    df = pd.DataFrame({
        "Entity": ["Ali Raza Khan", "PakSecure Technologies", "Nexus Capital"],
        "Type": ["Individual", "Organization", "Organization"],
        "Risk_Level": ["High", "Medium", "Low"],
        "Flags": ["Sanctions Match, Adverse Media", "Dark Web Mention", ""],
        "Last_Seen": ["2024-12-01", "2025-02-10", "2025-06-01"]
    })

# === SEARCH INTERFACE ===
entity = st.text_input("🔍 Search for an entity:")

if entity:
    st.markdown("---")
    st.markdown(f"### Results for: **{entity}**")
    match, score = process.extractOne(entity, df["Entity"])

    if score > 70:
        result = df[df["Entity"] == match].iloc[0]
        st.warning(f"⚠️ **Match found**: {match} (score {score})")
        st.markdown(f"- **Type**: {result['Type']}")
        st.markdown(f"- **Risk Level**: {result['Risk_Level']}")
        st.markdown(f"- **Flags**: {result['Flags']}")
        st.markdown(f"- **Last Seen**: {result['Last_Seen']}")

        # === GENERATE PDF ===
        if st.button("📄 Generate PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, f"Compliant.one Report - {match}", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.cell(200, 10, f"Generated: {datetime.datetime.now()}", ln=True)
            pdf.ln(10)
            pdf.multi_cell(0, 10, f"""
Entity: {match}
Type: {result['Type']}
Risk Level: {result['Risk_Level']}
Flags: {result['Flags']}
Last Seen: {result['Last_Seen']}
""")
            report_name = f"reports/{match.replace(' ','_')}_report.pdf"
            pdf.output(report_name)
            st.success(f"✅ Report saved as {report_name}")

    else:
        st.success("✅ No matching records found in the database.")

st.markdown("---")
st.caption("Compliant.one MVP © 2025 | AI-Powered RegTech Platform")
