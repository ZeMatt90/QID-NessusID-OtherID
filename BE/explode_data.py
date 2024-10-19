import pandas as pd
chunk_size = 10000  # Imposta un valore appropriato
df_list = []

# Carica i dati
df = pd.read_csv('data/dictionary.csv')  # CSV contenente CVE, NessusID, QualysID come liste

# Esplodi le liste in righe separate
dfQ_exploded = df.copy()
dfN_exploded = df.copy()
dfN_exploded['doc_id'] = dfN_exploded['doc_id'].str.split(',')
dfQ_exploded['QID'] = dfQ_exploded['QID'].str.split(',')

df_exploded = df_exploded.explode('doc_id').explode('QID')

# Rimuovi spazi bianchi e valori NaN
dfN_exploded['doc_id'] = dfN_exploded['doc_id'].str.strip().fillna('No doc_id')
dfQ_exploded['QID'] = dfQ_exploded['QID'].str.strip().fillna('No QID')

# Creazione delle colonne di verifica
dfN_exploded['Covered_by_Nessus'] = dfN_exploded['doc_id'] != 'No doc_id'
dfQ_exploded['Covered_by_Qualys'] = dfQ_exploded['QID'] != 'No QID'

# Creazione della colonna di combinazione per analisi
def coverage_status(row):
    if row['Covered_by_Nessus'] and row['Covered_by_Qualys']:
        return 'Both'
    elif row['Covered_by_Nessus']:
        return 'Nessus Only'
    elif row['Covered_by_Qualys']:
        return 'Qualys Only'
    else:
        return 'Neither'

df_exploded['Coverage_Status'] = df_exploded.apply(coverage_status, axis=1)



# Calcola il numero di CVE per ogni categoria di copertura
coverage_summary = df_exploded['Coverage_Status'].value_counts()

# Calcola statistiche addizionali
total_cve = df['CVE'].nunique()
cve_covered_by_both = coverage_summary.get('Both', 0)
cve_covered_by_nessus_only = coverage_summary.get('Nessus Only', 0)
cve_covered_by_qualys_only = coverage_summary.get('Qualys Only', 0)
cve_covered_by_neither = coverage_summary.get('Neither', 0)




import streamlit as st

def show_analysis_page(df_exploded, coverage_summary):
    st.title("CVE Coverage Analysis")

    # Mostra i dati filtrati
    search_input = st.sidebar.text_input("Search CVE", '')
    filtered_data = df_exploded[df_exploded['CVE'].str.contains(search_input, na=False)]
    st.dataframe(filtered_data)

    # Visualizza il riepilogo della copertura
    st.subheader("CVE Coverage Summary")
    st.bar_chart(coverage_summary)

    # Dettagli statistici
    st.subheader("Statistics")
    st.write(f"Total CVE: {total_cve}")
    st.write(f"CVE covered by both Nessus and Qualys: {cve_covered_by_both} ({cve_covered_by_both/total_cve:.2%})")
    st.write(f"CVE covered by Nessus only: {cve_covered_by_nessus_only} ({cve_covered_by_nessus_only/total_cve:.2%})")
    st.write(f"CVE covered by Qualys only: {cve_covered_by_qualys_only} ({cve_covered_by_qualys_only/total_cve:.2%})")
    st.write(f"CVE covered by neither: {cve_covered_by_neither} ({cve_covered_by_neither/total_cve:.2%})")

# Esegui l'app Streamlit
if __name__ == "__main__":
    show_analysis_page(df_exploded, coverage_summary)
