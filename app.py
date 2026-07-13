import streamlit as st
import pandas as pd
import os

# اسم ملف البيانات
DATA_FILE = "data.csv"

# دالة تحميل البيانات
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["التاريخ", "القسم", "النوع", "المبلغ"])

# دالة التحقق من كلمة المرور
def check_password():
    st.title("🔐 دخول الإدارة")
    password = st.text_input("يرجى إدخال كلمة المرور", type="password")
    if password == "1234":  # يمكنك تغيير 1234 لأي كلمة مرور تريدها
        return True
    elif password != "":
        st.error("كلمة المرور غير صحيحة")
    return False

# --- البرنامج الرئيسي ---
if check_password():
    st.title("☕ نظام إدارة اللاونج المتكامل")
    df = load_data()

    # --- 1. قسم الإضافة ---
    with st.expander("➕ إضافة حركة جديدة"):
        with st.form("add_form"):
            date = st.date_input("التاريخ")
            section = st.selectbox("القسم", ["الشيشة", "البار", "المطبخ"])
            trans_type = st.selectbox("النوع", ["دخل", "مصروف"])
            amount = st.number_input("المبلغ", min_value=0)
            if st.form_submit_button("حفظ الحركة"):
                new_data = pd.DataFrame([[date, section, trans_type, amount]], columns=df.columns)
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("تم الحفظ بنجاح!")
                st.rerun()

    # --- 2. قسم التصفية والحذف ---
    st.subheader("📋 سجل الحركات والتحكم")
    col1, col2 = st.columns([2, 1])
    
    # تصفية حسب التاريخ
    filter_date = col1.date_input("تصفية سجلات تاريخ معين", value=None)
    if filter_date:
        df = df[df["التاريخ"] == str(filter_date)]

    # حذف حركة
    del_idx = col2.number_input("رقم الصف للحذف", min_value=0, max_value=len(df)-1 if not df.empty else 0, step=1)
    if col2.button("حذف المحدد"):
        if not df.empty:
            df = df.drop(del_idx).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.rerun()

    # --- 3. عرض الملخص والبيانات ---
    if not df.empty:
        # تحويل عمود المبلغ لأرقام
        df["المبلغ"] = pd.to_numeric(df["المبلغ"])
        
        total_income = df[df["النوع"] == "دخل"]["المبلغ"].sum()
        total_expense = df[df["النوع"] == "مصروف"]["المبلغ"].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("الدخل", f"{total_income}")
        c2.metric("المصروف", f"{total_expense}")
        c3.metric("الصافي", f"{total_income - total_expense}")
        
        st.dataframe(df)

        # --- 4. تصدير البيانات (Excel) ---
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 تحميل التقرير كـ Excel", data=csv, file_name="تقرير_اللاونج.csv", mime="text/csv")
    else:
        st.info("لا توجد بيانات مسجلة حالياً.")

    st.markdown("---")
    st.write("تم التطوير بواسطة: **زكريا (Zeko Momen)** 🚀")
