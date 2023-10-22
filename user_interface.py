from main_module import st, pd, URLError

# Aggiungi un titolo all'app
st.title('Arcadia streamlight')

# Aggiungi un'introduzione
st.write('Tiny example of data from dummy things.')

# Carica il tuo DataFrame
df = pd.read_excel("qualys-kb.xlsx")

# Aggiungi una barra laterale per la selezione della categoria

# Prima barra laterale per selezionare una colonna
colonna_selezionata = st.sidebar.selectbox("Seleziona una tipologia", df.columns)

# Seconda barra laterale per la selezione della categoria
filtro_opzioni = df[colonna_selezionata].unique()
categoria_selezionata = st.sidebar.selectbox("Seleziona un filtro", filtro_opzioni)

# Filtra i dati in base alla categoria selezionata e alla colonna selezionata
data_filtrati = df[df[colonna_selezionata] == categoria_selezionata]

# Filtra i dati in base alla categoria selezionata e alla colonna selezionata
#data_filtrati = df[df["Category"] == categoria_selezionata][[colonna_selezionata]]

# Visualizza il numero di righe per la categoria selezionata
st.write(f"Numero di righe per la categoria '{categoria_selezionata}': {len(data_filtrati)}")

st.write(categoria_selezionata)
#st.write(data_subfiltrati.corr())
#st.line_chart(df)


# Calcola la correlazione tra le colonne
correlazione = data_filtrati.corr()

# Visualizza la matrice di correlazione utilizzando Streamlit
st.dataframe(correlazione)








"""


correlazione tra 2 dataframe

import Levenshtein

stringa1 = "gatto"
stringa2 = "cane"

distanza = Levenshtein.distance(stringa1, stringa2)

print(f"Distanza di Levenshtein tra '{stringa1}' e '{stringa2}': {distanza}")


"""
