import pandas as pd

# Definisci i percorsi dei file
file_fullidnessus = "plugin/nessus/full_id.csv"
file_allcve="data/all_cve.csv"
file_nessus = "data/nessus-kb.csv"
file_qualys = "data/qualys-kb.csv"
file_dictionary = "data/dictionary.csv"


# Carico i DataFrame
df_fullidnessus = pd.read_csv(file_fullidnessus, header=None)
df_allcve = pd.read_csv(file_allcve)
df_nessus = pd.read_csv(file_nessus)
df_qualys = pd.read_csv(file_qualys)
df_dictionary_light = pd.read_csv(file_dictionary)

def checkdf (dfcheck, key=None):
    #stampo i duplicati
    # Visualizza le righe duplicate prima della rimozione
    if key is None:
        # Se key è None, rimuovi i duplicati senza specificare alcuna colonna
        duplicates_before = dfcheck[dfcheck.duplicated()]
        dfcheck = dfcheck.drop_duplicates()
    else:
        # Se key è fornito, rimuovi i duplicati sulla colonna specificata
        duplicates_before = dfcheck[dfcheck.duplicated(subset=[key], keep=False)]
        dfcheck = dfcheck.drop_duplicates(subset=[key], keep='first')
    print("Righe duplicate prima della rimozione:")
    print(duplicates_before)
    return dfcheck


# Verifica e rimozione duplicati in df_fullidnessus
df_deduplicated = df_fullidnessus.drop_duplicates()
# Rimozione dei decimali uguali a zero
#df_deduplicated = df_deduplicated.applymap(lambda x: int(x) if x == int(x) else x)
# Unione di tutte le colonne in una singola colonna
result_df = df_deduplicated.stack().reset_index(drop=True)


#  salvataggio su file CSV
print("\n*********************\nIDnessus")
#checkdf(df_fullidnessus).to_csv(file_fullidnessus, index=False)




# Verifica e rimozione duplicati in df_nessus
print("\n*********************\nnessus doc_id")
checkdf(df_nessus,'doc_id').to_csv(file_nessus, index=False)
# Verifica e rimozione duplicati in df_qualys
print("\n*********************\nqualys qid")
checkdf(df_qualys,'QID').to_csv(file_qualys, index=False)
# Verifica e rimozione duplicati in df_dictionary_light
print("\n*********************\ndictionary cve")
checkdf(df_dictionary_light,'CVE').to_csv(file_dictionary, index=False)
# Pulizia dati sporchi Nessus
#df_nessus  = re.sub('[\'\[\]]', '', str(plugin_data['cves']))
print("\n*********************\nall cve")
checkdf(df_allcve).to_csv(file_allcve, index=False)
