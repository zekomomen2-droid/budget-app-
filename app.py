import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام إدارة الميزانية - زكريا", layout="centered")

# --- دالة التحقق من الدخول ---
def login():
    st.title("🔐 دخول الإدارة")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    
    # يمكنك تغيير هذه القيم لاحقاً
    if st.button("دخول"):
        if username == "admin" and password == "1234":
            return True
        else:
            st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
    return False

# --- دالة إنشاء ملف الـ PDF ---
def create_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    
    # عنوان التقرير
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Lounge Daily Financial Report", ln=True, align='C')
    
    # التاريخ
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
    pdf.ln(10)

    # رؤوس الجدول (بالإنجليزية لتجنب أخطاء الترميز)
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

# --- البرنامج الرئيسي ---
if login():
    st.title("☕ نظام إدارة الميزانية")
    
    # مدخلات المستخدم
    date = st.date_input("التاريخ")
    section = st.selectbox("القسم", ["الشيشة", "البار", "المطبخ"])
    trans_type = st.selectbox("النوع", ["دخل", "مصروف"])
    amount = st.number_input("المبلغ", min_value=0)

    # زر الحفظ والتحميل
    if st.button("حفظ وتوليد التقرير"):
        new_data = pd.DataFrame({'Date': [date], 'Section': [section], 'Type': [trans_type], 'Amount': [amount]})
        
        # توليد الملف
        pdf_output = create_pdf(new_data)
        
        # زر التحميل
        st.download_button(
            label="📥 تحميل التقرير PDF",
            data=pdf_output,
            file_name="تقرير_الميزانية.pdf",
            mime="application/pdf"
        )
        st.success("تم تجهيز التقرير بنجاح!")

    # تذييل الصفحة
    st.markdown("---")
    st.write("تم التطوير بواسطة: **زكريا (Zeko Momen)** 🚀")
