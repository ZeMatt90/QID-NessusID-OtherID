from main_module import Levenshtein, pd, cosine_similarity,TfidfVectorizer,distance

class DataHandler:
    __slots__ = ['qualysdata', 'nessusdata', 'arcadiadata']

    def __init__(self):
        # Inizializza i DataFrame
        self.qualysdata = pd.DataFrame()
        self.nessusdata = pd.DataFrame()
        self.arcadiadata = pd.DataFrame()

    def load_data(self):
        # Carica i dati dai file specificati
        self.qualysdata = pd.read_excel("./data/qualys-light0.xlsx")
        self.nessusdata = pd.read_excel("./data/nessus-light.xlsx")
        self.arcadiadata = pd.read_excel("./data/arcadia.xlsx")

    def process_data(self):
        # Esempio di logica di elaborazione dei dati
        # Unione dei DataFrame, calcoli, ecc.
        # Questa logica può essere personalizzata in base alle tue esigenze specifiche
        self.arcadiadata = pd.merge(self.qualysdata, self.nessusdata, on='CVE ID')
        pd.ExcelWriter("./data/arcadia-light.xlsx", self.arcadiadata) 

        
    def calculate_correlation(self, data):
        correlazione = data.corr()
        st.dataframe(correlazione)
        # Altre operazioni sui dati...

    def display_summary(self):
        # Esempio di visualizzazione di un riassunto dei dati
        print("Summary:")
        #print("Qualys Data Shape:", self.qualysdata.shape)
        styled_df = self.qualysdata.style.format({'QID': '{:.0f}', 'Titolo': '{:.2f}'}) \
        .set_properties(**{'text-align': 'center'}) 
        # Imposta il formato per le colonne specifiche
         # Allinea il testo al centro
          # Nascondi l'indice
        # Visualizza il DataFrame con la formattazione
        styled_df_html = styled_df.to_html()
        print(styled_df_html)
        #print("Qualys Data Shape:",styled_df)


        print("Nessus Data Shape:", self.nessusdata.shape)
        print("Arcadia Data Shape:", self.arcadiadata.shape)


    def _test_data(self):
        # Logica per mostrare i dati
        for row1 in self.qualysdata:
            for row2 in self.nessusdata:
                # Calcolo della distanza euclidea tra le due righe
                euclidean_distance = distance.euclidean(row1, row2)
                print(f"Distanza euclidea tra le righe: {euclidean_distance}")





def test_data(self):
    # Logica per mostrare i dati
    for row1 in self.qualysdata:
        for row2 in self.nessusdata:
            # Calcolo della distanza euclidea tra le due righe
            euclidean_distance = distance.euclidean(row1, row2)
            print(f"Distanza euclidea tra le righe: {euclidean_distance}")

def stampa_pubb(self):
    print("stampa pubb")
    _test_data(self)
def _stampa_priv():
    print("stampa priv")

