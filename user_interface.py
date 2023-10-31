import streamlit as st
import pandas as pd

class UserInterface:
    def __init__(self, df):
        self.df = df

    def show_arcadia_page(self):
        st.title("Arcadia Page")
        st.write(' A Tiny Example of Data from Dummy Things')
        
        colonna_selezionata = st.sidebar.selectbox("Seleziona una tipologia", self.df.columns)
        filtro_opzioni = self.df[colonna_selezionata].unique()
        categoria_selezionata = st.sidebar.selectbox("Seleziona un filtro", filtro_opzioni)
        data_filtrati = self.df[self.df[colonna_selezionata] == categoria_selezionata]

        tab1, tab2,tab3 = st.tabs(["🗃 Data 🧬","📈📉Chart","📊 Grafico🔬"])
        #*************tab 1********************
        tab1.subheader("A tab with a data")
        tab1.dataframe(data_filtrati)

        #*************tab 2********************
        tab2.subheader("A tab with the chart")
        x_variable = st.sidebar.selectbox('Seleziona variabile X', self.df.columns)
        y_variable = st.sidebar.selectbox('Seleziona variabile Y', self.df.columns)
        # Grafico personalizzato
        tab2.line_chart(self.df[[x_variable, y_variable]])
        #*************tab 3********************
        tab3.line_chart(data_filtrati)
        tab3.write(f"Numero di righe per la categoria '{categoria_selezionata}': {len(data_filtrati)}")
        tab3.write(categoria_selezionata)
        tab3.scatter_chart(data_filtrati)
        st.sidebar.header('Personalizza il grafico')




    def show_qualys_page(self):
        st.title("Qualys Page")
        st.write(' A Tiny Example of Data from Dummy Things')
        
        colonna_selezionata = st.sidebar.selectbox("Seleziona una tipologia", self.df.columns)
        filtro_opzioni = self.df[colonna_selezionata].unique()
        categoria_selezionata = st.sidebar.selectbox("Seleziona un filtro", filtro_opzioni)
        data_filtrati = self.df[self.df[colonna_selezionata] == categoria_selezionata]

        tab1, tab2,tab3 = st.tabs(["🗃 Data 🧬","📈📉Chart","📊 Grafico🔬"])
        #*************tab 1********************
        tab1.subheader("A tab with a data")
        tab1.dataframe(data_filtrati)

        #*************tab 2********************
        tab2.subheader("A tab with the chart")
        x_variable = st.sidebar.selectbox('Seleziona variabile X', self.df.columns)
        y_variable = st.sidebar.selectbox('Seleziona variabile Y', self.df.columns)
        # Grafico personalizzato
        tab2.line_chart(self.df[[x_variable, y_variable]])
        #*************tab 3********************
        tab3.line_chart(data_filtrati)
        tab3.write(f"Numero di righe per la categoria '{categoria_selezionata}': {len(data_filtrati)}")
        tab3.write(categoria_selezionata)
        tab3.scatter_chart(data_filtrati)
        st.sidebar.header('Personalizza il grafico')

        # Aggiungi il contenuto specifico della scheda Qualys qui

    def show_nessus_page(self):
        st.title("Nessus Page")
        st.write(' A Tiny Example of Data from Dummy Things')
        
        colonna_selezionata = st.sidebar.selectbox("Seleziona una tipologia", self.df.columns)
        filtro_opzioni = self.df[colonna_selezionata].unique()
        categoria_selezionata = st.sidebar.selectbox("Seleziona un filtro", filtro_opzioni)
        data_filtrati = self.df[self.df[colonna_selezionata] == categoria_selezionata]

        tab1, tab2,tab3 = st.tabs(["🗃 Data 🧬","📈📉Chart","📊 Grafico🔬"])
        #*************tab 1********************
        tab1.subheader("A tab with a data")
        tab1.dataframe(data_filtrati)

        #*************tab 2********************
        tab2.subheader("A tab with the chart")
        x_variable = st.sidebar.selectbox('Seleziona variabile X', self.df.columns)
        y_variable = st.sidebar.selectbox('Seleziona variabile Y', self.df.columns)
        # Grafico personalizzato
        tab2.line_chart(self.df[[x_variable, y_variable]])
        #*************tab 3********************
        tab3.line_chart(data_filtrati)
        tab3.write(f"Numero di righe per la categoria '{categoria_selezionata}': {len(data_filtrati)}")
        tab3.write(categoria_selezionata)
        tab3.scatter_chart(data_filtrati)
        st.sidebar.header('Personalizza il grafico')

        # Aggiungi il contenuto specifico della scheda Nessus qui

def main():
    st.title("🌟  Arcadia Streamlit 🌟")
    st.write(' A Tiny Example of Data from Dummy Things')

    #TODO: usare usecols  per caricare meno dati
    # ed implementare la tipizzazione per i NULL
    #df['empty'] = df['empty'].astype(str)  # Specifica 'empty' come una colonna di tipo stringa
    
    dfa = pd.read_excel("./data/arcadia-light.xlsx")
    dfq = pd.read_excel("./data/qualys-light.xlsx")
    dfn = pd.read_excel("./data/nessus-light.xlsx")

    tab = st.sidebar.selectbox("Scegli una archivio dati", ["Arcadia", "Qualys", "Nessus"])

    arcadia_interface = UserInterface(dfa)
    qualys_interface = UserInterface(dfq)
    nessus_interface = UserInterface(dfn)

    if tab == "Arcadia":
        arcadia_interface.show_arcadia_page()
    elif tab == "Qualys":
        qualys_interface.show_qualys_page()
    elif tab == "Nessus":
        nessus_interface.show_nessus_page()

if __name__ == '__main__':
    main()
