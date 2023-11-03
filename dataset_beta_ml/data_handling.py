from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os, sys, Levenshtein, time,random
import streamlit as st
from urllib.error import URLError
from scipy.spatial import distance

class DataHandler:
    __slots__ = ['qualysdata', 'nessusdata', 'arcadiadata']

    def __init__(self):
        # Inizializza i DataFrame
        self.qualysdata = pd.DataFrame()
        self.nessusdata = pd.DataFrame()
        self.arcadiadata = pd.DataFrame()

    def load_data(self):
        # Carica i dati dai file specificati
        self.qualysdata = pd.read_excel("./data/qualys-kb.xlsx")
        self.nessusdata = pd.read_excel("./data/nessus-light.xlsx")
        self.arcadiadata = pd.read_excel("./data/arcadia.xlsx")

    def process_data(self):
        # Esempio di logica di elaborazione dei dati
        # Unione dei DataFrame, calcoli, ecc.
        # Questa logica può essere personalizzata in base alle tue esigenze specifiche
        self.arcadiadata = pd.merge(self.qualysdata, self.nessusdata, on='CVE ID')
        pd.ExcelWriter("./data/arcadia-light.xlsx", self.arcadiadata) 

    def display_summary(self):
        # Esempio di visualizzazione di un riassunto dei dati
        print("Summary:")
        #print("Qualys Data Shape:", self.qualysdata.shape)
        styled_df = self.qualysdata.style.format({'QID': '{:.0f}', 'Titolo': '{:.2f}'}) \
        # Visualizza il DataFrame con la formattazione
        styled_df_html = styled_df.to_html()
        print(styled_df_html)
        #print("Qualys Data Shape:",styled_df)
        print("Arcadia Data Shape:", self.arcadiadata.shape)
