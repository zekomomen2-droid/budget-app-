import streamlit as st
import pandas as pd
import os
import plotly.express as px  # مكتبة للرسوم البيانية

DATA_FILE = "data.csv"
PASS_FILE = "password.txt"

# إعداد كلمة المرور
if not os.path.exists(PASS_FILE):
    with open(PASS_FILE, "w") as f: f.write("1234")

def get_password():
    with open(PASS_FILE, "r") as f: return f.read()

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["التاريخ", "القسم", "النوع", "المبلغ"])

st.set_page_config(page_title="Smart Manager", layout="centered")

# --- نظام الدخول ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 دخول النظام")
    user_pass = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if user_pass == get_password():
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة")
else:
    st.title("🚀 نظام الإدارة الذكي")
    df = load_data()
    df["التاريخ"] = pd.to_datetime(df["التاريخ"], errors="coerce")
    df = df.dropna(subset=["التاريخ"])

    # القائمة الجانبية
    with st.sidebar:
        st.header("⚙️ الإعدادات")
        new_pass = st.text_input("تغيير كلمة المرور", type="password")
        if st.button("حفظ كلمة المرور"):
            with open(PASS_FILE, "w") as f: f.write(new_pass)
            st.success("تم التحديث!")
        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.rerun()

    # --- إضافة الحركات ---
    with st.expander("➕ إضافة حركة مالية"):
        with st.form("add"):
            date = st.date_input("التاريخ")
            section = st.selectbox("التصنيف", ["مبيعات عامة", "رواتب", "مشتريات/مواد خام", "إيجار/كهرباء", "أخرى"])
            trans_type = st.selectbox("النوع", ["دخل", "مصروف"])
            amount = st.number_input("المبلغ", min_value=1) # فرض قيمة أكبر من 0
            
            if st.form_submit_button("حفظ الحركة"):
                new_data = pd.DataFrame([[date, section, trans_type, amount]], columns=["التاريخ", "القسم", "النوع", "المبلغ"])
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.rerun()

    # --- الجرد الشهري ---
    st.subheader("📊 تقرير الجرد الشهري")
    col_y, col_m = st.columns(2)
    year = col_y.selectbox("السنة", [2026, 2027, 2028])
    month = col_m.selectbox("الشهر", range(1, 13))
    
    filtered = df[(df["التاريخ"].dt.year == year) & (df["التاريخ"].dt.month == month)]

    if not filtered.empty:
        inc = filtered[filtered["النوع"] == "دخل"]["المبلغ"].sum()
        exp = filtered[filtered["النوع"] == "مصروف"]["المبلغ"].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي الدخل", inc)
        c2.metric("إجمالي المصروف", exp)
        c3.metric("صافي الربح", inc - exp)
        
        # إضافة رسم بياني توضيحي
        fig = px.pie(filtered, values='المبلغ', names='النوع', title="توزيع الدخل والمصروفات")
        st.plotly_chart(fig)
        
        st.dataframe(filtered)
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 تحميل التقرير (Excel)", data=csv, file_name="report.csv", mime="text/csv")
    else:
        st.info("لا توجد بيانات لهذا الشهر.")
    
    st.write("تم التطوير بواسطة: **Zeko Momen** 🚀")
