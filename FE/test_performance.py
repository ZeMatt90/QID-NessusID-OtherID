import streamlit as st
import pandas as pd
import time

# Funzioni per caricare i dati e misurare il tempo
@st.cache.data
def load_file(file_path, file_type):
    start_time = time.time()
    if file_type == 'feather':
        df = pd.read_feather(file_path)
    elif file_type == 'hdf':
        df = pd.read_hdf(file_path)
    elif file_type == 'parquet':
        df = pd.read_parquet(file_path)
    elif file_type == 'csv':
        df = pd.read_csv(file_path)
    load_time = time.time() - start_time
    return df, load_time

# Funzione per eseguire una ricerca pesante
def heavy_search(df, column, value):
    start_time = time.time()
    result = df[df[column] == value]
    search_time = time.time() - start_time
    return result, search_time

# Percorsi dei file
feather_file = 'data/dictionary.feather'
hdf_file = 'data/dictionary.h5'
parquet_file = 'data/dictionary.parquet'
csv_file = 'data/dictionary.csv'

# Carica i dati e misura il tempo di caricamento
feather_df, feather_time = load_file(feather_file, 'feather')
hdf_df, hdf_time = load_file(hdf_file, 'hdf')
parquet_df, parquet_time = load_file(parquet_file, 'parquet')
csv_df, csv_time = load_file(csv_file, 'csv')

# Colonna e valore per la ricerca pesante (adattalo ai tuoi dati)
search_column = 'some_column'
search_value = 'some_value'

# Esegui la ricerca pesante e misura il tempo
feather_result, feather_search_time = heavy_search(feather_df, search_column, search_value)
hdf_result, hdf_search_time = heavy_search(hdf_df, search_column, search_value)
parquet_result, parquet_search_time = heavy_search(parquet_df, search_column, search_value)
csv_result, csv_search_time = heavy_search(csv_df, search_column, search_value)

# Titolo dell'applicazione
st.title("Confronto tra Formati di File: Feather, HDF5, Parquet e CSV")

# Mostra i tempi di caricamento
st.header("Tempi di Caricamento")
st.write(f"Tempo di caricamento Feather: {feather_time:.2f} secondi")
st.write(f"Tempo di caricamento HDF5: {hdf_time:.2f} secondi")
st.write(f"Tempo di caricamento Parquet: {parquet_time:.2f} secondi")
st.write(f"Tempo di caricamento CSV: {csv_time:.2f} secondi")

# Mostra i tempi di ricerca
st.header("Tempi di Ricerca Pesante")
st.write(f"Tempo di ricerca Feather: {feather_search_time:.2f} secondi")
st.write(f"Tempo di ricerca HDF5: {hdf_search_time:.2f} secondi")
st.write(f"Tempo di ricerca Parquet: {parquet_search_time:.2f} secondi")
st.write(f"Tempo di ricerca CSV: {csv_search_time:.2f} secondi")

# Mostra le prime righe dei DataFrame
st.header("Feather File")
st.write(feather_df.head())

st.header("HDF5 File")
st.write(hdf_df.head())

st.header("Parquet File")
st.write(parquet_df.head())

st.header("CSV File")
st.write(csv_df.head())

# Opzione per visualizzare statistiche descrittive
if st.checkbox("Visualizza statistiche descrittive per Feather", key="feather_stats"):
    st.subheader("Statistiche Descrittive Feather")
    st.write(feather_df.describe())
    
if st.checkbox("Visualizza statistiche descrittive per HDF5", key="hdf_stats"):
    st.subheader("Statistiche Descrittive HDF5")
    st.write(hdf_df.describe())
    
if st.checkbox("Visualizza statistiche descrittive per Parquet", key="parquet_stats"):
    st.subheader("Statistiche Descrittive Parquet")
    st.write(parquet_df.describe())

if st.checkbox("Visualizza statistiche descrittive per CSV", key="csv_stats"):
    st.subheader("Statistiche Descrittive CSV")
    st.write(csv_df.describe())
