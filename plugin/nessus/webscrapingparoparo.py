import requests
import json
import pandas as pd
import time
#idnessus di test con cve CVE-2022-3602
IDs=[173835,173139,173113,167841,167263,167024,166965,166960,166959,166808,166801,166798,166796,166789,166788,166787,166782,166781,166774,166773]

# URL da cui effettuare la richiesta GET
base_url ="https://www.tenable.com/_next/data/yHtLwfa7D2y-FVrK1k9cM/en/plugins/nessus/NUMEROID.json?type=nessus&id=NUMEROID"
#url = "https://www.tenable.com/_next/data/HbLEgcen8J-sBub4SqZDm/en/plugins/nessus/NUMEROID.json?type=nessus"
json_data_list= []

for ID in IDs:
    url =base_url.replace("NUMEROID",str(ID))
    print("invio get "+url)
    time.sleep(1)
    response = requests.get(url)                                    # Esegui la richiesta GET
    if response.status_code == 200:                                 # Verifica se la richiesta ha avuto successo
        json_data_list.append(response.json().get("pageProps").get("plugin"))     # Ottieni il JSON dalla risposta
    else:
        print("La richiesta non è riuscita. Codice di stato:", response.status_code)

# Crea un DataFrame da questa lista di oggetti JSON
df = pd.DataFrame(json_data_list)

# Specifica il percorso del file XLSX in cui desideri salvarli
file_path = ".\data\nessus-light2.xlsx"

# Salva il DataFrame nel file XLSX
df.to_excel(file_path, index=False)
