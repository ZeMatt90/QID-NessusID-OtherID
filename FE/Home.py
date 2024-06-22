import streamlit as st
import pandas as pd

# Importa le pagine
import ArcadiaPage
import QualysPage
import NessusPage

def main():
    st.title("🌟 Arcadia Streamlit 🌟")

    data_files = {
        "Arcadia": "../BE/data/dictionary.csv",
        "Qualys": "../BE/data/qualys-kb.csv",
        "Nessus": "../BE/data/nessus-kb.csv"
    }

    tab = st.sidebar.selectbox("Scegli un archivio dati", list(data_files.keys()))

    df = pd.read_csv(data_files[tab])
    
    if tab == "Arcadia":
        ArcadiaPage.show_page(df)
    elif tab == "Qualys":
        QualysPage.show_page(df)
    elif tab == "Nessus":
        NessusPage.show_page(df)

if __name__ == '__main__':
    main()
