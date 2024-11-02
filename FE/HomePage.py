import streamlit as st
import requests
import pandas as pd

def get_cve_description(cve_id):
    if not cve_id.startswith("CVE-") or len(cve_id.split("-")) != 3:
        st.write("Formato CVE non valido. Usa il formato CVE-YYYY-NNNN.")
        return None
    
    parts = cve_id.split("-")
    
    try:
        year = parts[1]
        
        cve_number = parts[2]

        # Controllo se `year` e `cve_number` sono numeri
        if not year.isdigit() or not cve_number.isdigit():
            st.write("Anno e numero CVE devono essere numerici. Usa il formato CVE-YYYY-NNNN.")
            return None

        base_num = cve_number[:-3] + "xxx"  
        url = f"https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/{year}/{base_num}/{cve_id}.json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            try:
                description = data["containers"]["cna"]["descriptions"][0]["value"]
                return description
            except KeyError:
                return "Descrizione non trovata nel file JSON."
        else:
            return "CVE non trovata, controllare l'esistenza della CVE https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/."
    
    except IndexError:
        st.write("Errore: l'ID CVE fornito non è completo. Usa il formato CVE-YYYY-NNNN.")
        return None


def show_page(df):
    st.title("home Page")
    
    search_input = st.sidebar.text_input("Inserisci l'ID CVE (es. CVE-1999-0001):", 'CVE-1999-0001')
    data_filtrati = df[df['CVE'].str.contains(search_input)]

    if search_input:
        description = get_cve_description(search_input)
        st.write("Descrizione CVE ufficiale per cve.org:", search_input)
        st.write(description)
        data_filtrati = df[df['CVE'].str.contains(search_input)]

    data_filtrati = data_filtrati.drop_duplicates(subset=['Vari titoli Qualys', 'possibili soluzioni Nessus', 'info aggiuntive Nessus'])


    # colonne_da_visualizzare = ['Vari titoli Qualys', 'possibili soluzioni Nessus', 'info aggiuntive Nessus']
    # data_filtrati = data_filtrati[colonne_da_visualizzare]

    # Visualizzazione del dataframe con le colonne selezionate
    # st.dataframe(data_filtrati)
    # Visualizza i dati di ciascuna colonna in sezioni separate
    if not data_filtrati.empty:
        st.write("Lista possibili informazioni correlate da Qualys:", data_filtrati['Vari titoli Qualys'].to_list())
        st.write("Lista possibili informazioni correlate da Nessus:", data_filtrati['possibili soluzioni Nessus'].to_list())
        st.write("Lista possibili informazioni aggiuntive correlate Nessu:", data_filtrati['info aggiuntive Nessus'].to_list())
    
        st.write("Informazioni aggiuntive eventuali:", data_filtrati['info'])
    # else:
    #     st.write("Nessun dato corrispondente trovato.")


