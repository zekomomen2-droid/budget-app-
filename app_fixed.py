import streamlit as st
import pandas as pd
import os
import plotly.express as px

DATA_FILE = "data.csv"
PASS_FILE = "password.txt"

# إعداد الملفات
if not os.path.exists(PASS_FILE):
    with open(PASS_FILE, "w") as f: f.write("1234")

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # التأكد من وجود عمود الملاحظات
        if "ملاحظات" not in df.columns:
            df["ملاحظات"] = ""
        return df
    return pd.DataFrame(columns=["التاريخ", "القسم", "النوع", "المبلغ", "ملاحظات"])

st.set_page_config(page_title="Smart Manager Pro", layout="centered")

st.title("🚀 نظام الإدارة الذكي - نسخة الأعمال")

# --- نظام الدخول ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    user_pass = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        with open(PASS_FILE, "r") as f: real_pass = f.read()
        if user_pass == real_pass:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة")
else:
    df = load_data()
    
    # --- إضافة الحركات ---
    with st.expander("➕ إضافة حركة مالية جديدة"):
        with st.form("add"):
            date = st.date_input("التاريخ")
            section = st.selectbox("التصنيف", ["مبيعات عامة", "رواتب", "مشتريات", "إيجار/كهرباء", "أخرى"])
            trans_type = st.selectbox("النوع", ["دخل", "مصروف"])
            amount = st.number_input("المبلغ", min_value=1)
            notes = st.text_input("ملاحظات (اختياري)") # إضافة حقل الملاحظات
            
            if st.form_submit_button("حفظ الحركة"):
                new_data = pd.DataFrame([[date, section, trans_type, amount, notes]], 
                                        columns=["التاريخ", "القسم", "النوع", "المبلغ", "ملاحظات"])
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("تم الحفظ بنجاح!")
                st.rerun()

    # --- التقرير ---
    st.subheader("📊 تقرير الجرد والتحليل")
    col_y, col_m = st.columns(2)
    year = col_y.selectbox("السنة", [2026, 2027])
    month = col_m.selectbox("الشهر", range(1, 13))
    
    df["التاريخ"] = pd.to_datetime(df["التاريخ"])
    filtered = df[(df["التاريخ"].dt.year == year) & (df["التاريخ"].dt.month == month)]

    if not filtered.empty:
        inc = filtered[filtered["النوع"] == "دخل"]["المبلغ"].sum()
        exp = filtered[filtered["النوع"] == "مصروف"]["المبلغ"].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("الدخل", f"{inc} ريال")
        c2.metric("المصروف", f"{exp} ريال")
        c3.metric("صافي الربح", f"{inc - exp} ريال")
        
        # الرسم البياني
        fig = px.pie(filtered, values='المبلغ', names='النوع', title="توزيع الدخل مقابل المصروفات")
        st.plotly_chart(fig)
        
        st.dataframe(filtered)
        
        # تحميل التقرير
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 تحميل التقرير بصيغة CSV", data=csv, file_name=f"report_{year}_{month}.csv", mime="text/csv")
    else:
        st.info("لا توجد بيانات لهذا الشهر.")
    
    st.sidebar.button("تسجيل خروج", on_click=lambda: st.session_state.update({"logged_in": False}) or st.rerun())
