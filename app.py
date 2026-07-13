import streamlit as st
import pandas as pd
import os

DATA_FILE = "data.csv"
PASS_FILE = "password.txt"

# إعداد كلمة المرور الافتراضية
if not os.path.exists(PASS_FILE):
    with open(PASS_FILE, "w") as f: f.write("1234")

def get_password():
    with open(PASS_FILE, "r") as f: return f.read()

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["التاريخ", "القسم", "النوع", "المبلغ"])

st.set_page_config(page_title="نظام الإدارة - Zeko Momen")

# --- نظام الدخول ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 دخول الإدارة")
    user_pass = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if user_pass == get_password():
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("كلمة المرور خطأ")
else:
    st.title("☕ نظام إدارة اللاونج المتكامل")
    df = load_data()
    df["التاريخ"] = pd.to_datetime(df["التاريخ"])

    # القائمة الجانبية للإعدادات
    with st.sidebar:
        st.header("⚙️ الإعدادات")
        new_pass = st.text_input("تغيير كلمة المرور", type="password")
        if st.button("حفظ كلمة المرور الجديدة"):
            with open(PASS_FILE, "w") as f: f.write(new_pass)
            st.success("تم التحديث!")
        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.rerun()

    # --- إضافة الحركات ---
    with st.expander("➕ إضافة حركة"):
        with st.form("add"):
            date = st.date_input("التاريخ")
            section = st.selectbox("القسم", ["الشيشة", "البار", "المطبخ"])
            trans_type = st.selectbox("النوع", ["دخل", "مصروف"])
            amount = st.number_input("المبلغ", min_value=0)
            if st.form_submit_button("حفظ"):
                if trans_type == "مصروف" and amount > 5000:
                    st.warning("⚠️ تنبيه: المبلغ يتجاوز الحد المسموح!")
                new_data = pd.DataFrame([[date, section, trans_type, amount]], columns=df.columns)
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.rerun()

    # --- الجرد الشهري ---
    st.subheader("📊 الجرد الشهري")
    col_y, col_m = st.columns(2)
    year = col_y.selectbox("السنة", [2026, 2027])
    month = col_m.selectbox("الشهر", range(1, 13))
    
    filtered = df[(df["التاريخ"].dt.year == year) & (df["التاريخ"].dt.month == month)]

    if not filtered.empty:
        inc = filtered[filtered["النوع"] == "دخل"]["المبلغ"].sum()
        exp = filtered[filtered["النوع"] == "مصروف"]["المبلغ"].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("الدخل", inc)
        c2.metric("المصروف", exp)
        c3.metric("الصافي", inc - exp)
        
        if exp > 5000: st.error("🚨 إجمالي المصروفات تجاوز 5000!")
        
        st.dataframe(filtered)
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 تحميل التقرير", data=csv, file_name="report.csv", mime="text/csv")
    
    st.write("---")
    st.write("تطوير: **زكريا (Zeko Momen)** 🚀")
