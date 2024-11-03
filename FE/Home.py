# from turtle import home
import streamlit as st
import pandas as pd

# Importa le pagine
import ArcadiaPage
# import QualysPage
# import NessusPage
import HomePage

def main():
    st.title("🌟 Arcadia Streamlit 🌟")

    data_files = {
        "Home":"data/dictionary.csv",
        "Arcadia": "data/dictionary.csv"
        # "Qualys": "data/qualys-kb.csv",
        # "Nessus": "data/nessus-kb.csv"
    }

    tab = st.sidebar.selectbox("Scelta pagina", list(data_files.keys()))

    df = pd.read_csv(data_files[tab])
    
    if tab == "Home":
        HomePage.show_page(df)
    elif tab == "Arcadia":
        ArcadiaPage.show_page(df)
    # elif tab == "Qualys":
    #     QualysPage.show_page(df)
    # elif tab == "Nessus":
    #     NessusPage.show_page(df)

if __name__ == '__main__':
    main()
