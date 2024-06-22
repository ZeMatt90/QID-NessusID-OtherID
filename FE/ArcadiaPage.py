import streamlit as st
import pandas as pd
import plotly.express as px

def run_update():
    with open("./plugin/nessus/update.py", 'r') as f:
        code = f.read()
        exec(code)

def show_page(df):
    st.title("Arcadia Page")

    if st.button("Update"):
        run_update()

    search_input = st.sidebar.text_input("Cerca una CVE", '')
    data_filtrati = df[df['CVE'].str.contains(search_input)]

    st.dataframe(data_filtrati)

    st.subheader("Conteggio delle occorrenze QID per ogni CVE")
    conteggio_qid_per_cve = df['QID'].apply(len)
    st.bar_chart(conteggio_qid_per_cve.value_counts())

    st.subheader("Conteggio delle occorrenze Nessus per ogni CVE")
    conteggio_qid_per_cve = df['doc_id'].apply(len)
    st.bar_chart(conteggio_qid_per_cve.value_counts())
