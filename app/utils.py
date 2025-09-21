import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from fpdf import FPDF
import tempfile
import base64

def render_xrd_chart():
    st.markdown("### 📊 Simulated XRD Plot")

    data = pd.DataFrame({
        "2θ (degrees)": [20, 30, 40, 50, 60, 70],
        "Intensity": [10, 80, 30, 100, 60, 20]
    })

    fig, ax = plt.subplots()
    ax.plot(data["2θ (degrees)"], data["Intensity"], marker='o', color='#0B5ED7')
    ax.set_xlabel("2θ (degrees)")
    ax.set_ylabel("Intensity")
    ax.set_title("Simulated XRD Pattern")
    st.pyplot(fig)

def generate_pdf_report(structure, recommendation):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="StructSentry Analysis Report", ln=1, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, txt="🔬 Structure Analysis")
    for k, v in structure.items():
        pdf.multi_cell(0, 10, f"{k.capitalize()}: {v}")

    pdf.ln(5)
    pdf.multi_cell(0, 10, txt="📦 Recommendation")
    pdf.multi_cell(0, 10, recommendation)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        tmp.seek(0)
        b64 = base64.b64encode(tmp.read()).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="structsentry_report.pdf">📥 Download PDF Report</a>'
        st.markdown(href, unsafe_allow_html=True)