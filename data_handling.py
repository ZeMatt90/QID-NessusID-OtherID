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
        self.qualysdata = pd.read_excel("./data/qualys-light2.xlsx")
        self.nessusdata = pd.read_excel("./data/nessus-light.xlsx")
        self.arcadiadata = pd.read_excel("./data/arcadia-light.xlsx")

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



# stringa = "CVE-2022-3602,CVE-2022-3786"
# stringa1 = ""
# stringa2 = "Open Secure Sockets Layer (OpenSSL) Less Than 3.0.7 Buffer Overflow Vulnerability"
#
# distanza = Levenshtein.distance(stringa1, stringa2)
#
# print(f"Distanza di Levenshtein tra '{stringa1}' e '{stringa2}': {distanza}")
#
#
# percorso_corrente = os.path.abspath(os.getcwd())
#
# # Costruisci il percorso completo al file Excel
# percorso_excel = os.path.join(percorso_corrente, "qualys", "qualys-light2.xlsx")
#
# # Leggi il file Excel
# df = pd.read_excel(percorso_excel)
#
# #df = pd.read_excel("./qualys/qualys-light2.xlsx")
#
# documento1 = [
#     '39',
#     'Open Secure Sockets Layer (OpenSSL) Less Than 3.0.7 Buffer Overflow Vulnerability',
#     'Remote Discovery, Multiple Authentication Types Discovery, Patch Available',
#     'General remote services',
#     'CVE-2022-3602, CVE-2022-3786',
#     'OpenSSL 3.0.7', '10.00',
#     '7.50',
#     '11/07/2022 at 02:33:47 PM (GMT+0100)',
#     '10/31/2022 at 12:40:23 PM (GMT+0100)',
#     'Security Patch Installation',
#     '#NAME?']
#
# # Creazione del vettore TF-IDF per i documenti
# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(documento1)
#
# # Calcola la similarità coseno tra i documenti
# similarità = cosine_similarity(X)
#
# # Stampa la matrice di similarità
# print("***************Matrice di similarità documento:")
# print(similarità)
#
#
# correlazioni = df.corr()
# print("****************Matrice di correlazione df:")
# print(correlazioni)
#


# Crea un vettore TF-IDF per ciascun documento
#vectorizer = TfidfVectorizer()
#X = vectorizer.fit_transform([documento1, documento2])

# Calcola la similarità coseno tra i due documenti
#similarità = cosine_similarity(X[0], X[1])

# Stampa la similarità coseno
#print("Similarità coseno tra documento1 e documento2:", similarità[0][0])
