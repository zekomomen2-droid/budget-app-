import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime

# إعدادات الصفحة
st.set_page_config(page_title="Lounge Budget App")
st.title("Lounge Management System")

# دالة إنشاء ملف الـ PDF
def create_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Lounge Daily Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
    pdf.ln(10)

    # رؤوس الجدول
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(35, 10, "Date", border=1)
    pdf.cell(40, 10, "Section", border=1)
    pdf.cell(35, 10, "Type", border=1)
    pdf.cell(30, 10, "Amount", border=1)
    pdf.ln()

    # بيانات الجدول
    pdf.set_font("Arial", size=10)
    for index, row in df.iterrows():
        pdf.cell(35, 10, str(row['Date']), border=1)
        pdf.cell(40, 10, str(row['Section']), border=1)
        pdf.cell(35, 10, str(row['Type']), border=1)
        pdf.cell(30, 10, str(row['Amount']), border=1)
        pdf.ln()
    
    return pdf.output(dest='S')

# واجهة التطبيق البسيطة
st.header("Enter Transaction")
date = st.date_input("Date")
section = st.selectbox("Section", ["Shisha", "Bar", "Kitchen"])
trans_type = st.selectbox("Type", ["Income", "Expense"])
amount = st.number_input("Amount", min_value=0)

if st.button("Save & Generate PDF"):
    # هنا يتم حفظ البيانات (مثال بسيط)
    new_data = pd.DataFrame({'Date': [date], 'Section': [section], 'Type': [trans_type], 'Amount': [amount]})
    
    # تحويل البيانات لـ PDF
    pdf_output = create_pdf(new_data)
    
    st.download_button(
        label="Download PDF Report",
        data=pdf_output,
        file_name="report.pdf",
        mime="application/pdf"
    )
    st.success("Report generated successfully!")

st.markdown("---")
st.write("Developed by: Zeko Momen 🚀")
