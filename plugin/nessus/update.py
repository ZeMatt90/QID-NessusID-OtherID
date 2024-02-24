import requests
import json
import pandas as pd
import re
"""
prima di lanciare questo assicurarsi di aver aggiornato il file cleaned numerbers.csv tramite
curl -S https://www.tenable.com/plugins/feeds?sort=newest | grep -o "<link>https://www.tenable.com/plugins/nessus/[0-9]\+</link>" | sed -n 's/.*\/\([0-9]*\)<\/link>.*/\1/p' > cleaned_numbers.csv
"""

file_newid= "plugin/nessus/cleaned_numbers.csv"
file_full= "plugin/nessus/full_id.csv"
file_nessus = "data/nessus-kb.csv"

df_nuovo = pd.read_csv(file_newid, header=None)
df_full = pd.read_csv(file_full, header=None)
df_key = pd.read_csv('plugin/nessus/keyforget.csv' , header=None)
keyforget= df_key.iloc[0, 0]

numeri_esistenti = df_full.values.flatten().tolist()
numeri_nuovi = df_nuovo.values.flatten().tolist()

#carico i nuovi id da scaricare, che non sono presenti in full_id.csv
IDs = [numero for numero in numeri_nuovi if numero not in numeri_esistenti]
print("\n nuovi numeri da aggiungere\n\n")
print(IDs)


# URL da cui effettuare la richiesta GET
#base_url = "https://www.tenable.com/plugins/nessus/NUMEROID"
base_url = "https://www.tenable.com/_next/data/"+str(keyforget)+"/en/plugins/nessus/NUMEROID.json?type=nessus&id=NUMEROID"
json_data_list= []
try:
    for ID in IDs:
        url =base_url.replace("NUMEROID",str(ID))
        print("invio get "+url)
        response = requests.get(url)                                    # Esegui la richiesta GET
        if response.status_code == 200:                                 # Verifica se la richiesta ha avuto successo
#           # Ottieni il JSON dalla risposta
            plugin_data = response.json().get("pageProps").get("plugin")

            # Pulisco la colonna 'cves'
            cves_tmp = re.sub('[\'\[\]]', '', str(plugin_data['cves']))
            plugin_data['cves'] = cves_tmp
            
            # Aggiungi l'oggetto JSON pulito alla lista
            json_data_list.append(plugin_data)

            new_id_inserito = pd.DataFrame([str(ID)], columns=['cves'])
            
            new_id_inserito['cves'] = new_id_inserito['cves'].astype(str)

            # Aggiungo l'id tra quelli già presenti principale
            df_full = pd.concat([df_full, new_id_inserito], ignore_index=True)
            print(str(new_id_inserito['cves'].tolist())+" andato\n")

            #
        
        else:
            print("La richiesta non è riuscita. Codice di stato:", response.status_code)
except Exception as e:
    print(f"curl on {str(ID)} ha generato un errore: {str(e)}")
finally:
    print("TODO gestione salvataggio parziale")
    df_full.to_csv(file_full, header=False, index=False)

    df = pd.concat([pd.DataFrame(json_data_list), pd.read_csv(file_nessus)], ignore_index=True, sort=False)
    #df = pd.DataFrame(json_data_list) 
    df.to_csv(file_nessus, index=False)
