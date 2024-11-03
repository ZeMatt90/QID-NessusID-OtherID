# from turtle import home
import streamlit as st
import pandas as pd

# Importa le pagine
import ArcadiaPage
# import QualysPage
# import NessusPage
import HomePage

import os


def main():
    st.title("🌟 Arcadia Streamlit 🌟")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'data', 'dictionary.csv')

    data_files = {
        "Home":csv_path+"/data/dictionary.csv",
        "Arcadia": csv_path+"data/dictionary.csv"
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
