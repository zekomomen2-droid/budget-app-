import streamlit as st
import pandas as pd
import os
from datetime import datetime

# إعداد واجهة البرنامج لتكون عريضة ومنظمة مثل جداول المحاسبة
st.set_page_config(page_title="نظام المحاسبة وإدارة الميزانية الذكي", layout="wide")

st.title("📊 نظام المحاسبة وإدارة الميزانية الذكي")
st.markdown("نظام سحابي مرن لتسجيل الإيرادات والمصروفات اليومية بدقة إكسل.")

# اسم ملف قاعدة البيانات المحلية لحفظ البيانات بشكل دائم
FILE_NAME = "accounting_ledger.csv"

# دالة تحميل البيانات المحفوظة سابقاً
def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    else:
        return pd.DataFrame(columns=["التاريخ", "البيان / الوصف", "التصنيف", "الوارد (دخل)", "المنصرف (مصروف)"])

# دالة حفظ البيانات الجديدة
def save_data(df):
    df.to_csv(FILE_NAME, index=False)

# تحميل البيانات في ذاكرة التطبيق
df = load_data()

# --- 1. لوحة المؤشرات المالية السريعة (Dashboard) ---
if not df.empty:
    total_income = df["الوارد (دخل)"].sum()
    total_expenses = df["المنصرف (مصروف)"].sum()
else:
    total_income = 0
    total_expenses = 0

balance = total_income - total_expenses

# تصميم بطاقات العرض العلوية
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🟢 إجمالي الإيرادات (الوارد)", value=f"{total_income:,} ريال")
with col2:
    st.metric(label="🔴 إجمالي المصروفات (المنصرف)", value=f"{total_expenses:,} ريال")
with col3:
    st.metric(label="💰 صافي الرصيد الحالي", value=f"{balance:,} ريال")

st.markdown("---")

# --- 2. نموذج إدخال المعاملات اليومية ---
st.subheader("📝 تسجيل قيد محاسبي جديد")

with st.form("accounting_form", clear_on_submit=True):
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        date_input = st.date_input("التاريخ", datetime.now())
    with c2:
        description = st.text_input("البيان / الوصف", placeholder="مثال: شراء فطور، مقاضي محل..")
    with c3:
        category = st.selectbox("التصنيف", ["دخل يومي", "مقاضي", "فطور", "غداء", "دخان", "مواصلات", "أخرى"])
    with c4:
        income_val = st.number_input("الوارد (الدخل)", min_value=0, step=5)
    with c5:
        expense_val = st.number_input("المنصرف (المصروف)", min_value=0, step=5)
        
    submit_btn = st.form_submit_button("إضافة العملية إلى الدفتر المحاسبي 💾")

# معالجة الضغط على زر الحفظ
if submit_btn:
    if description.strip() == "":
        st.error("عذراً، يجب كتابة وصف أو بيان للعملية قبل الحفظ!")
    elif income_val == 0 and expense_val == 0:
        st.error("يجب إدخال مبلغ في خانة الدخل أو خانة المصروف!")
    else:
        # تجهيز السطر الجديد
        new_row = {
            "التاريخ": str(date_input),
            "البيان / الوصف": description,
            "التصنيف": category,
            "الوارد (دخل)": income_val,
            "المنصرف (مصروف)": expense_val
        }
        # إضافة السطر الجديد وحفظ الملف
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("تم ترحيل العملية وحفظها في الدفتر بنجاح!")
        st.rerun()

st.markdown("---")

# --- 3. عرض دفتر القيود اليومية والرسم البياني ---
st.subheader("📋 دفتر القيود اليومي (جداول البيانات)")

if not df.empty:
    # حساب الرصيد التراكمي خطوة بخطوة مثل دفاتر المحاسبة الفندقية والتجارية
    df["الرصيد المتبقي"] = df["الوارد (دخل)"].cumsum() - df["المنصرف (مصروف)"].cumsum()
    
    # عرض الجدول بشكل تفاعلي شبيه بإكسل
    st.dataframe(df, use_container_width=True)
    
    # رسم بياني سريع لتوزيع المصاريف لحاملي الأجهزة الذكية
    st.markdown("### 📊 تحليل سريع للمصروفات حسب التصنيف")
    expenses_only = df[df["المنصرف (مصروف)"] > 0]
    if not expenses_only.empty:
        chart_data = expenses_only.groupby("التصنيف")["المنصرف (مصروف)"].sum()
        st.bar_chart(chart_data)
    else:
        st.info("لا توجد مصروفات مرصودة لعرض رسم بياني لها بعد.")
        
    # خيار لمسح البيانات وتصفير النظام
    st.markdown("##")
    if st.button("🔴 تصفير الدفتر والميزانية بالكامل"):
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
        st.rerun()
else:
    st.info("الدفتر فارغ حالياً. قم بتسجيل العمليات اليومية من النموذج أعلاه للبدء.")
