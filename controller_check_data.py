import pandas as pd

# Definisci i percorsi dei file
file_fullidnessus = "plugin/nessus/full_id.csv"
file_allcve="data/all_cve.csv"
file_nessus = "data/nessus-kb.csv"
file_qualys = "data/qualys-kb.csv"
file_dictionary_light = "data/dictionary-light.csv"

# Carico i DataFrame
df_fullidnessus = pd.read_csv(file_fullidnessus, header=None)
df_allcve = pd.read_csv(file_allcve)
df_nessus = pd.read_csv(file_nessus)
df_qualys = pd.read_csv(file_qualys)
df_dictionary_light = pd.read_csv(file_dictionary_light)

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
print("IDnessus")
checkdf(df_fullidnessus).to_csv(file_fullidnessus, index=False)
# Verifica e rimozione duplicati in df_nessus
print("nessus doc_id")
checkdf(df_nessus,'doc_id').to_csv(file_nessus, index=False)
# Verifica e rimozione duplicati in df_qualys
print("qualys qid")
checkdf(df_qualys,'QID').to_csv(file_qualys, index=False)
# Verifica e rimozione duplicati in df_dictionary_light
print("dictionary cve")
checkdf(df_dictionary_light,'CVE').to_csv(file_dictionary_light, index=False)
# Pulizia dati sporchi Nessus
#df_nessus  = re.sub('[\'\[\]]', '', str(plugin_data['cves']))
print("all cve")
checkdf(df_allcve).to_csv(file_allcve, index=False)
