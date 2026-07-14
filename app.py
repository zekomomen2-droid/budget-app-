import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================
# إعدادات التطبيق
# ==========================

st.set_page_config(
    page_title="Smart Manager",
    page_icon="💼",
    layout="wide"
)

DATA_FILE = "data.csv"
PASS_FILE = "password.txt"

# ==========================
# إنشاء الملفات تلقائياً
# ==========================

if not os.path.exists(PASS_FILE):
    with open(PASS_FILE, "w", encoding="utf-8") as f:
        f.write("1234")

if not os.path.exists(DATA_FILE):
    pd.DataFrame(
        columns=[
            "التاريخ",
            "القسم",
            "النوع",
            "المبلغ"
        ]
    ).to_csv(DATA_FILE, index=False)

# ==========================
# الدوال
# ==========================

def get_password():
    with open(PASS_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


def save_password(password):
    with open(PASS_FILE, "w", encoding="utf-8") as f:
        f.write(password)


def load_data():

    df = pd.read_csv(DATA_FILE)

    if not df.empty:
        df["التاريخ"] = pd.to_datetime(
            df["التاريخ"],
            errors="coerce"
        )

        df = df.dropna(subset=["التاريخ"])

    return df


def save_data(df):
    df.to_csv(DATA_FILE, index=False)
# ==========================
# نظام تسجيل الدخول
# ==========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Smart Manager")

    st.markdown("### تسجيل الدخول")

    password = st.text_input(
        "كلمة المرور",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:
        login = st.button(
            "🚀 دخول",
            use_container_width=True
        )

    with col2:
        st.button(
            "❌ خروج",
            disabled=True,
            use_container_width=True
        )

    if login:

        if password == get_password():

            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("❌ كلمة المرور غير صحيحة")

    st.stop()

# ==========================
# تحميل البيانات
# ==========================

df = load_data()

# ==========================
# القائمة الجانبية
# ==========================

with st.sidebar:

    st.title("⚙️ الإعدادات")

    st.write("---")

    new_password = st.text_input(
        "تغيير كلمة المرور",
        type="password"
    )

    if st.button(
        "💾 حفظ كلمة المرور",
        use_container_width=True
    ):

        if new_password.strip() == "":
            st.warning("اكتب كلمة مرور جديدة")
        else:
            save_password(new_password)
            st.success("✅ تم تغيير كلمة المرور")

    st.write("---")

    if st.button(
        "🚪 تسجيل خروج",
        use_container_width=True
    ):
        st.session_state.logged_in = False
        st.rerun()

# ==========================
# عنوان البرنامج
# ==========================

st.title("💼 Smart Manager")

st.caption("نظام إدارة الإيرادات والمصروفات")
# ==========================
# إضافة عملية مالية
# ==========================

st.write("---")
st.subheader("➕ إضافة عملية مالية")

with st.form("add_transaction"):

    col1, col2 = st.columns(2)

    with col1:
        trans_date = st.date_input("📅 التاريخ")

        section = st.selectbox(
            "📂 القسم",
            [
                "مبيعات",
                "مشتريات",
                "رواتب",
                "إيجار",
                "كهرباء",
                "مياه",
                "وقود",
                "صيانة",
                "مصروفات أخرى"
            ]
        )

    with col2:

        trans_type = st.selectbox(
            "💳 النوع",
            [
                "دخل",
                "مصروف"
            ]
        )

        amount = st.number_input(
            "💰 المبلغ",
            min_value=0.0,
            step=1.0,
            format="%.2f"
        )

    notes = st.text_input(
        "📝 ملاحظات (اختياري)"
    )

    save = st.form_submit_button(
        "💾 حفظ العملية",
        use_container_width=True
    )

    if save:

        new_row = pd.DataFrame(
            [[
                trans_date,
                section,
                trans_type,
                amount
            ]],
            columns=[
                "التاريخ",
                "القسم",
                "النوع",
                "المبلغ"
            ]
        )

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        save_data(df)

        st.success("✅ تم حفظ العملية بنجاح")

        st.rerun()
        # ==========================================
# لوحة الإحصائيات
# ==========================================

st.write("---")
st.subheader("📊 لوحة الإحصائيات")

if not df.empty:

    total_income = df[df["النوع"] == "دخل"]["المبلغ"].sum()

    total_expense = df[df["النوع"] == "مصروف"]["المبلغ"].sum()

    balance = total_income - total_expense

    total_transactions = len(df)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 إجمالي الدخل",
        f"{total_income:,.2f} ريال"
    )

    c2.metric(
        "💸 إجمالي المصروف",
        f"{total_expense:,.2f} ريال"
    )

    c3.metric(
        "💵 الرصيد",
        f"{balance:,.2f} ريال"
    )

    c4.metric(
        "🧾 عدد العمليات",
        total_transactions
        )
    # ==========================================
# الرسوم البيانية
# ==========================================

if not filtered.empty:

    st.write("---")
    st.subheader("📈 الرسوم البيانية")

    left, right = st.columns(2)

    # رسم أعمدة حسب النوع
    with left:

        chart = (
            filtered
            .groupby("النوع")["المبلغ"]
            .sum()
        )

        st.bar_chart(chart)

    # رسم دائري
    with right:

        fig, ax = plt.subplots(figsize=(5,5))

        ax.pie(
            chart.values,
            labels=chart.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.axis("equal")

        st.pyplot(fig)

    st.write("---")

    # ======================================
    # البحث
    # ======================================

    search = st.text_input(
        "🔍 ابحث عن قسم..."
    )

    display = filtered.copy()

    if search:

        display = display[
            display["القسم"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.subheader("📋 العمليات المالية")

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "📥 تحميل التقرير CSV",
        display.to_csv(index=False).encode("utf-8-sig"),
        "report.csv",
        "text/csv"
    )

else:

    st.info("لا توجد بيانات لعرض الرسوم البيانية.")
    # ==========================================
# ملخص حسب الأقسام
# ==========================================

st.write("---")
st.subheader("📂 ملخص الأقسام")

if not filtered.empty:

    summary = (
        filtered.groupby(["القسم", "النوع"])["المبلغ"]
        .sum()
        .unstack(fill_value=0)
    )

    if "دخل" not in summary.columns:
        summary["دخل"] = 0

    if "مصروف" not in summary.columns:
        summary["مصروف"] = 0

    summary["صافي الربح"] = (
        summary["دخل"] - summary["مصروف"]
    )

    st.dataframe(
        summary,
        use_container_width=True
    )

    st.write("---")

    best_income = summary["دخل"].idxmax()

    best_expense = summary["مصروف"].idxmax()

    col1, col2 = st.columns(2)

    col1.success(
        f"🏆 أعلى دخل: {best_income}"
    )

    col2.error(
        f"💸 أعلى مصروف: {best_expense}"
    )

else:

    st.info("لا توجد بيانات.")
    
# ==========================================
# تصدير Excel
# ==========================================

st.write("---")
st.subheader("📥 تصدير التقارير")

excel_data = display.copy()

excel_file = "report.xlsx"

try:

    excel_data.to_excel(
        excel_file,
        index=False
    )

    with open(excel_file, "rb") as f:

        st.download_button(
            "📊 تحميل التقرير Excel",
            f,
            file_name="report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

except Exception as e:

    st.error(e)

# ==========================================
# فلترة بالتاريخ
# ==========================================

st.write("---")
st.subheader("📅 فلترة حسب التاريخ")

col1, col2 = st.columns(2)

start_date = col1.date_input(
    "من تاريخ"
)

end_date = col2.date_input(
    "إلى تاريخ"
)

if not df.empty:

    result = df[
        (
            df["التاريخ"] >= pd.to_datetime(start_date)
        )
        &
        (
            df["التاريخ"] <= pd.to_datetime(end_date)
        )
    ]

    st.write("### النتائج")

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

# ==========================================
# معلومات سريعة
# ==========================================

st.write("---")

st.info(
    f"""
📊 عدد العمليات الكلي : {len(df)}

💰 إجمالي الدخل : {df[df['النوع']=='دخل']['المبلغ'].sum():,.2f}

💸 إجمالي المصروف : {df[df['النوع']=='مصروف']['المبلغ'].sum():,.2f}
"""
)# ==========================================
# تحسين الواجهة
# ==========================================

st.write("---")

st.markdown(
    """
    <style>

    .stMetric{
        background:#f8f9fa;
        border-radius:15px;
        padding:15px;
        border:1px solid #ddd;
        box-shadow:0 2px 10px rgba(0,0,0,.08);
    }

    .stButton>button{
        width:100%;
        border-radius:10px;
        height:45px;
        font-weight:bold;
    }

    .stDownloadButton>button{
        width:100%;
        border-radius:10px;
        height:45px;
    }

    footer{
        visibility:hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.write("")
st.write("")

st.success("✅ Smart Manager يعمل بنجاح")

st.caption(
    """
🚀 الإصدار 1.0

تم التطوير بواسطة **Zeko Momen**

شكراً لاستخدامك Smart Manager ❤️
"""
)
