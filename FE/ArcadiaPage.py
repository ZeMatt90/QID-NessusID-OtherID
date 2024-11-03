import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# def run_update():
#     with open("./plugin/nessus/update.py", 'r') as f:
#         code = f.read()
#         exec(code)

def show_page(df):
    st.title("Arcadia Page")

    # if st.button("Update"):
    #     run_update()

    search_input = st.sidebar.text_input("Cerca una CVE", '')
    data_filtrati = df[df['CVE'].str.contains(search_input)]

    st.dataframe(data_filtrati)

    # st.subheader("Conteggio delle occorrenze QID per ogni CVE")
    # conteggio_qid_per_cve = df['QID'].apply(len)
    # st.bar_chart(conteggio_qid_per_cve.value_counts())

    # st.subheader("Conteggio delle occorrenze Nessus per ogni CVE")
    # conteggio_qid_per_cve = df['doc_id'].apply(len)
    # st.bar_chart(conteggio_qid_per_cve.value_counts())


    # # Creazione della matrice di correlazione tra Nessus_ID e Qualys_ID
    # correlation_matrix = pd.crosstab(df['Doc_id'], df['QID'])

    # # Streamlit App
    # st.title("Correlazione tra Nessus e Qualys tramite CVE comuni")

    # st.write("Questa heatmap mostra la correlazione tra gli ID di Nessus e Qualys basata sulle CVE comuni.")

    # # Creazione del grafico a heatmap
    # plt.figure(figsize=(10, 7))
    # sns.heatmap(correlation_matrix, annot=True, fmt="d", cmap="Blues", cbar=True)
    # plt.title("Correlazione tra Nessus e Qualys")
    # plt.xlabel("Qualys_ID")
    # plt.ylabel("Nessus_ID")

    # # Visualizzazione del grafico con Streamlit
    # st.pyplot(plt)



    # Grafico 1: Numero di vulnerabilità per CVE
    st.subheader("Numero di vulnerabilità per CVE")
    cve_counts = df['CVE'].value_counts()
    
    # plt.figure(figsize=(10, 6))
    # plt.bar(cve_counts.index, cve_counts.values, color='steelblue')
    # plt.xlabel('CVE')
    # plt.ylabel('Numero di Vulnerabilità')
    # plt.title('Numero di Vulnerabilità per CVE')
    # st.pyplot(plt)

    # Grafico 2: Distribuzione dei QID per CVE
    st.subheader("Distribuzione dei QID per CVE")
    qid_lengths = df['QID'].apply(len)
    plt.figure(figsize=(10, 6))
    plt.bar(df['CVE'], qid_lengths, color='orange')
    plt.xlabel('CVE')
    plt.ylabel('Numero di QID associati')
    plt.title('Distribuzione dei QID per CVE')
    st.pyplot(plt)

    # Grafico 3: CVE con soluzioni Nessus
    st.subheader("CVE con soluzioni Nessus")
    has_solutions = df['Soluzioni_Nessus'].apply(lambda x: 1 if len(x) > 0 else 0).value_counts()
    labels = ['Con Soluzione', 'Senza Soluzione']
    plt.figure(figsize=(6, 6))
    plt.pie(has_solutions, labels=labels, autopct='%1.1f%%', colors=['green', 'red'])
    plt.title('Distribuzione di CVE con e senza Soluzioni Nessus')
    st.pyplot(plt)

    # Grafico 4: Conteggio CVE per Prodotti (Titoli Qualys)
    st.subheader("Conteggio CVE per Prodotti")
    prodotti_counts = df['Titoli_Qualys'].apply(len)
    plt.figure(figsize=(10, 6))
    plt.bar(df['CVE'], prodotti_counts, color='purple')
    plt.xlabel('CVE')
    plt.ylabel('Numero di Prodotti (Titoli Qualys)')
    plt.title('Conteggio CVE per Prodotti')
    st.pyplot(plt)

    # Grafico 5: CVE con Info Nessus aggiuntive
    st.subheader("CVE con Info Nessus aggiuntive")
    info_nessus_counts = df['Info_Nessus'].apply(lambda x: 1 if len(x) > 0 else 0).value_counts()
    labels_info = ['Con Info Nessus', 'Senza Info Nessus']
    plt.figure(figsize=(6, 6))
    plt.pie(info_nessus_counts, labels=labels_info, autopct='%1.1f%%', colors=['blue', 'gray'])
    plt.title('Distribuzione di CVE con e senza Info Nessus Aggiuntive')
    st.pyplot(plt)