import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_FILE = "data.csv"
PASS_FILE = "password.txt"

# إنشاء كلمة المرور لأول مرة
if not os.path.exists(PASS_FILE):
    with open(PASS_FILE, "w", encoding="utf-8") as f:
        f.write("1234")

def get_password():
    with open(PASS_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(
            columns=["التاريخ", "القسم", "النوع", "المبلغ"]
        )
    return df

st.set_page_config(
    page_title="Smart Manager",
    page_icon="📊",
    layout="wide"
)

# نظام تسجيل الدخول
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Smart Manager")

    password = st.text_input(
        "كلمة المرور",
        type="password"
    )

    if st.button("دخول"):

        if password == get_password():
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة")

    st.stop()

df = load_data()

if not df.empty:
    df["التاريخ"] = pd.to_datetime(df["التاريخ"])

# القائمة الجانبية
with st.sidebar:

    st.header("⚙️ الإعدادات")

    new_pass = st.text_input(
        "تغيير كلمة المرور",
        type="password"
    )

    if st.button("حفظ كلمة المرور"):

        if new_pass != "":
            with open(PASS_FILE, "w", encoding="utf-8") as f:
                f.write(new_pass)

            st.success("تم تغيير كلمة المرور")

    st.divider()

    if st.button("تسجيل خروج"):
        st.session_state.logged_in = False
        st.rerun()

st.title("🚀 نظام الإدارة الذكي")
# ==========================
# إضافة حركة مالية
# ==========================

with st.expander("➕ إضافة حركة مالية", expanded=True):

    with st.form("add_form"):

        date = st.date_input("التاريخ")

        section = st.selectbox(
            "القسم",
            [
                "مبيعات",
                "رواتب",
                "مشتريات",
                "إيجار",
                "كهرباء",
                "مياه",
                "مصاريف أخرى"
            ]
        )

        trans_type = st.selectbox(
            "النوع",
            [
                "دخل",
                "مصروف"
            ]
        )

        amount = st.number_input(
            "المبلغ",
            min_value=0.0,
            step=1.0
        )

        save = st.form_submit_button("💾 حفظ")

        if save:

            new_row = pd.DataFrame(
                [[date, section, trans_type, amount]],
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

            df.to_csv(
                DATA_FILE,
                index=False
            )

            st.success("✅ تم حفظ الحركة المالية")

            st.rerun()

# ==========================
# التقرير الشهري
# ==========================

st.subheader("📊 التقرير الشهري")

c1, c2 = st.columns(2)

year = c1.selectbox(
    "السنة",
    [2026, 2027, 2028]
)

month = c2.selectbox(
    "الشهر",
    list(range(1, 13))
)

if df.empty:

    filtered = pd.DataFrame(
        columns=df.columns
    )

else:

    filtered = df[
        (df["التاريخ"].dt.year == year)
        &
        (df["التاريخ"].dt.month == month)
    ]# ==========================
# لوحة الإحصائيات
# ==========================

if filtered.empty:

    st.info("لا توجد بيانات لهذا الشهر.")

else:

    total_income = filtered[
        filtered["النوع"] == "دخل"
    ]["المبلغ"].sum()

    total_expense = filtered[
        filtered["النوع"] == "مصروف"
    ]["المبلغ"].sum()

    net_profit = total_income - total_expense

    st.subheader("📊 لوحة الإحصائيات")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💰 إجمالي الدخل",
        f"{total_income:,.2f} ريال"
    )

    c2.metric(
        "💸 إجمالي المصروف",
        f"{total_expense:,.2f} ريال"
    )

    c3.metric(
        "📈 صافي الربح",
        f"{net_profit:,.2f} ريال"
    )

    st.divider()

    # رسم بالأعمدة
    st.subheader("📊 الدخل والمصروف")

    chart_data = (
        filtered.groupby("النوع")["المبلغ"]
        .sum()
    )

    st.bar_chart(chart_data)

    st.divider()

    # مخطط دائري
    st.subheader("🥧 توزيع العمليات")

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.pie(
        chart_data.values,
        labels=chart_data.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)

    st.divider()

    # جدول العمليات
    st.subheader("📋 جميع العمليات")

    st.dataframe(
        filtered,
        use_container_width=True
    )

    st.download_button(
        "📥 تحميل التقرير CSV",
        filtered.to_csv(index=False).encode("utf-8-sig"),
        "report.csv",
        "text/csv"
    )

st.divider()

st.caption("🚀 تم التطوير بواسطة Zeko Momen")
