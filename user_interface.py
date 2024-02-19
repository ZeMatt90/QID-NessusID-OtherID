# pylint: disable=import-error

import streamlit as st
import pandas as pd
import plotly.express as px 

#from transformers import pipeline

# Carica il modello di linguaggio pre-addestrato
#chatbot = pipeline("conversational")



class UserInterface:
    def __init__(self, df):
        self.df = df
    # Funzione per eseguire la chat con l'IA
    # def chat_with_ai(self):
    #     user_input = st.text_input("Tu:")
    #     if user_input:
    #         # Genera una risposta dall'IA
    #         bot_response = chatbot(user_input)[0]['generated_text']
    #         # Visualizza la risposta dell'IA
    #         st.text_area("AI:", bot_response, height=100)


    def show_data_page(self, title):
        st.title(title)
        #st.write('A Tiny Example of Data')
        if title == "Arcadia Page":
                    cve_selezionata = st.sidebar.selectbox("Seleziona una CVE", self.df['CVE'].unique())
                    #data_filtrati = self.df[self.df['CVE'] == cve_selezionata]
                    #data_filtrati = self.df['CVE'] == cve_selezionata
                    data_filtrati = self.df

                    st.subheader(f"Dati relativi alla CVE: {cve_selezionata}")
                    st.dataframe(data_filtrati)

                    st.subheader("Correlazione tra QID e DOC_ID")
                    correlazione_chart_data = data_filtrati.groupby(['QID', 'doc_id']).size().reset_index(name='count')
                    fig = px.pie(correlazione_chart_data['count'], labels=correlazione_chart_data['QID'].astype(str) + '-' + correlazione_chart_data['doc_id'].astype(str))
                    st.plotly_chart(fig)


#'info': ""
                     # Aggiungi l'opzione per modificare la colonna CVE
                    nuova_cve = st.text_input("Modifica la CVE", cve_selezionata)
                    if st.button("Salva modifiche"):
                        self.df.loc[self.df['info'] == cve_selezionata, 'Solution'] = nuova_cve

        else:
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
    
    #st.snow()
    st.title("🌟  Arcadia Streamlit 🌟")
    #st.write('A Tiny Example of Data from Dummy Things')

    data_files = {
        "Arcadia": "./data/dictionary-light.csv",
        "Qualys": "./data/qualys-kb.csv",
        "Nessus": "./data/nessus-kb.csv"
    }

    tab = st.sidebar.selectbox("Scegli un archivio dati", list(data_files.keys()))

    df = pd.read_csv(data_files[tab]) # type: ignore
    user_interface = UserInterface(df)

    if tab == "Arcadia":
        user_interface.show_arcadia_page()
    elif tab == "Qualys":
        user_interface.show_qualys_page()
    elif tab == "Nessus":
        user_interface.show_nessus_page()

if __name__ == '__main__':
    main()
