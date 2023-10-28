import streamlit as st
import pandas as pd

class UserInterface:
    def __init__(self, df):
        self.df = df
        self.setup_ui()

    def setup_ui(self):
        st.title('Arcadia Streamlit')
        st.write('A Tiny Example of Data from Dummy Things')
        self.select_category()

    def select_category(self):
        colonna_selezionata = st.sidebar.selectbox("Seleziona una tipologia", self.df.columns)
        filtro_opzioni = self.df[colonna_selezionata].unique()
        categoria_selezionata = st.sidebar.selectbox("Seleziona un filtro", filtro_opzioni)
        data_filtrati = self.df[self.df[colonna_selezionata] == categoria_selezionata]
        st.write(f"Numero di righe per la categoria '{categoria_selezionata}': {len(data_filtrati)}")
        st.write(categoria_selezionata)
        st.dataframe(data_filtrati)

def main():
    st.title('Arcadia Streamlit')
    st.write('A Tiny Example of Data from Dummy Things')

    df = pd.read_excel("./data/arcadia-light.xlsx")

    user_interface = UserInterface(df)

    

if __name__ == '__main__':
    main()










