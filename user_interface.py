import streamlit as st
import pandas as pd

class UserInterface:
    def __init__(self, df):
        self.df = df

    def show_data_page(self, title):
        st.title(title)
        st.write('A Tiny Example of Data from Dummy Things')

        colonna_selezionata = st.sidebar.selectbox("Seleziona una tipologia", self.df.columns)
        filtro_opzioni = self.df[colonna_selezionata].unique()
        categoria_selezionata = st.sidebar.selectbox("Seleziona un filtro", filtro_opzioni)
        data_filtrati = self.df[self.df[colonna_selezionata] == categoria_selezionata]
        
        tab = st.selectbox("Scegli una scheda", ["🗃 Data 🧬", "📈📉 Chart", "📊 Grafico🔬"])

        if tab == "🗃 Data 🧬":
            st.subheader("A tab with data")
            st.dataframe(data_filtrati)
        elif tab == "📈📉 Chart":
            st.subheader("A tab with the chart")
            x_variable = st.sidebar.selectbox('Seleziona variabile X', self.df.columns)
            y_variable = st.sidebar.selectbox('Seleziona variabile Y', self.df.columns)
            st.line_chart(self.df[[x_variable, y_variable]], use_container_width=True)
        elif tab == "📊 Grafico🔬":
            st.subheader("A tab with chart and info")
            st.line_chart(data_filtrati)
            st.write(f"Numero di righe per la categoria '{categoria_selezionata}': {len(data_filtrati)}")
            st.write(categoria_selezionata)
            st.scatter_chart(data_filtrati)
            st.header('Personalizza il grafico')

    def show_arcadia_page(self):
        self.show_data_page("Arcadia Page")

    def show_qualys_page(self):
        self.show_data_page("Qualys Page")

    def show_nessus_page(self):
        self.show_data_page("Nessus Page")

def main():
    st.title("🌟  Arcadia Streamlit 🌟")
    st.write('A Tiny Example of Data from Dummy Things')

    data_files = {
        "Arcadia": "./data/arcadia-light.xlsx",
        "Qualys": "./data/qualys-light.xlsx",
        "Nessus": "./data/nessus-light.xlsx"
    }

    tab = st.sidebar.selectbox("Scegli una archivio dati", list(data_files.keys()))

    df = pd.read_excel(data_files[tab]) # type: ignore
    user_interface = UserInterface(df)

    if tab == "Arcadia":
        user_interface.show_arcadia_page()
    elif tab == "Qualys":
        user_interface.show_qualys_page()
    elif tab == "Nessus":
        user_interface.show_nessus_page()

if __name__ == '__main__':
    main()
