import streamlit as st

st.title("💰 نظام إدارة الميزانية الشخصية")

income = st.number_input("أدخل دخلك الشهري:", min_value=0.0)
expense = st.number_input("أدخل مصروفاتك:", min_value=0.0)

if st.button("احسب الرصيد"):
    balance = income - expense
    st.write(f"### دخلك: {income} ريال")
    st.write(f"### مصروفاتك: {expense} ريال")
    st.write(f"### صافي الرصيد المتبقي: {balance} ريال")
