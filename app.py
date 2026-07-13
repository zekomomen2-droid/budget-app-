import streamlit as st
import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="نظام إدارة اللاونج المحاسبي", layout="wide")

# نظام الدخول
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if not st.session_state.password_correct:
        st.title("🔐 دخول الإدارة")
        user = st.text_input("اسم المستخدم")
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if user == "admin" and pwd == "1234":
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
        return False
    return True

if not check_password():
    st.stop()

# دالة الـ PDF
def create_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="تقرير أداء اللاونج (غرفة الشيشة - البار - المطبخ)", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"التاريخ: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(35, 10, "التاريخ", border=1)
    pdf.cell(40, 10, "القسم", border=1)
    pdf.cell(35, 10, "النوع", border=1)
    pdf.cell(30, 10, "المبلغ", border=1)
    pdf.ln()
    pdf.set_font("Arial", size=10)
    for index, row in df.iterrows():
        pdf.cell(35, 10, str(row['التاريخ']), border=1)
        pdf.cell(40, 10, str(row['القسم/التصنيف']), border=1)
        pdf.cell(35, 10, str(row['النوع']), border=1)
        pdf.cell(30, 10, str(row['المبلغ']), border=1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1')

# الواجهة
st.title("☕ نظام إدارة اللاونج")
st.sidebar.button("تسجيل الخروج", on_click=lambda: st.session_state.update({"password_correct": False}))

FILE_NAME = "lounge_ledger.csv"
df = pd.read_csv(FILE_NAME) if os.path.exists(FILE_NAME) else pd.DataFrame(columns=["التاريخ", "القسم/التصنيف", "النوع", "الوصف", "المبلغ"])

col1, col2, col3 = st.columns(3)
total_sales = df[df["النوع"] == "مبيعات (دخل)"]["المبلغ"].sum()
total_costs = df[df["النوع"] == "مشتريات (صرف)"]["المبلغ"].sum()
col1.metric("إجمالي المبيعات", f"{total_sales:,} ريال")
col2.metric("إجمالي المصاريف", f"{total_costs:,} ريال")
col3.metric("صافي الربح", f"{total_sales - total_costs:,} ريال")

if not df.empty:
    pdf_file = create_pdf(df)
    st.download_button(label="📥 تحميل التقرير PDF", data=pdf_file, file_name="Lounge_Report.pdf", mime="application/pdf")

# النموذج
with st.form("lounge_form", clear_on_submit=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        date = st.date_input("التاريخ", datetime.now())
        entry_type = st.radio("نوع الحركة", ["مبيعات (دخل)", "مشتريات (صرف)"])
    with c2:
        category = st.selectbox("القسم", ["غرفة الشيشة", "البار", "المطبخ", "مصاريف إدارية/أخرى"])
        description = st.text_input("وصف العملية")
    with c3:
        amount = st.number_input("المبلغ (ريال)", min_value=0.0, step=1.0)
    submitted = st.form_submit_button("إضافة العملية 💾")

if submitted:
    new_data = pd.DataFrame([{"التاريخ": str(date), "القسم/التصنيف": category, "النوع": entry_type, "الوصف": description, "المبلغ": amount}])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    st.success("تم الحفظ!")
    st.rerun()

st.subheader("📋 سجل الحركة اليومية")
st.dataframe(df, use_container_width=True)
