import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="نظام إدارة اللاونج المحاسبي", layout="wide")

st.title("☕ نظام إدارة ميزانية اللاونج")
st.subheader("إدارة الشيشة، القهوة، الحلى، والأكل")

FILE_NAME = "lounge_ledger.csv"

def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    else:
        return pd.DataFrame(columns=["التاريخ", "القسم/التصنيف", "النوع", "الوصف", "المبلغ"])

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

df = load_data()

# --- لوحة المؤشرات ---
col1, col2, col3 = st.columns(3)
total_sales = df[df["النوع"] == "مبيعات (دخل)"]["المبلغ"].sum()
total_costs = df[df["النوع"] == "مشتريات (صرف)"]["المبلغ"].sum()
net_profit = total_sales - total_costs

col1.metric("💰 إجمالي المبيعات", f"{total_sales:,} ريال")
col2.metric("💸 إجمالي المصاريف", f"{total_costs:,} ريال")
col3.metric("📈 صافي الربح", f"{net_profit:,} ريال")

st.markdown("---")

# --- نموذج الإدخال ---
with st.form("lounge_form", clear_on_submit=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        date = st.date_input("التاريخ", datetime.now())
        entry_type = st.radio("نوع الحركة", ["مبيعات (دخل)", "مشتريات (صرف)"])
    with c2:
        category = st.selectbox("القسم/التصنيف", ["شيشة", "قهوة", "حلى", "أكل", "فواتير عامة"])
        description = st.text_input("وصف الفاتورة/العملية")
    with c3:
        amount = st.number_input("المبلغ (ريال)", min_value=0.0, step=1.0)
    
    submitted = st.form_submit_button("إضافة العملية 💾")

if submitted:
    new_data = pd.DataFrame([{"التاريخ": str(date), "القسم/التصنيف": category, "النوع": entry_type, "الوصف": description, "المبلغ": amount}])
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)
    st.success("تم الحفظ!")
    st.rerun()

# --- عرض البيانات ---
st.subheader("📋 سجل الحركة اليومية")
st.dataframe(df, use_container_width=True)

# --- تحليل ذكي ---
st.subheader("📊 تحليل الأداء حسب القسم")
if not df.empty:
    pivot = df.groupby(["القسم/التصنيف", "النوع"])["المبلغ"].sum().unstack().fillna(0)
    st.bar_chart(pivot)

if st.button("🔴 تصفير البيانات"):
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)
    st.rerun()
