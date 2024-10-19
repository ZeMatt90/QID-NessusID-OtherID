import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

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


    # Creazione della matrice di correlazione tra Nessus_ID e Qualys_ID
    correlation_matrix = pd.crosstab(df['Doc_id'], df['QID'])

    # Streamlit App
    st.title("Correlazione tra Nessus e Qualys tramite CVE comuni")

    st.write("Questa heatmap mostra la correlazione tra gli ID di Nessus e Qualys basata sulle CVE comuni.")

    # Creazione del grafico a heatmap
    plt.figure(figsize=(10, 7))
    sns.heatmap(correlation_matrix, annot=True, fmt="d", cmap="Blues", cbar=True)
    plt.title("Correlazione tra Nessus e Qualys")
    plt.xlabel("Qualys_ID")
    plt.ylabel("Nessus_ID")

    # Visualizzazione del grafico con Streamlit
    st.pyplot(plt)