import requests
import pandas as pd
"""
prima di lanciare questo assicurarsi di aver aggiornato il file cleaned numerbers.csv tramite
curl -S https://www.tenable.com/plugins/feeds?sort=newest | grep -o "<link>https://www.tenable.com/plugins/nessus/[0-9]\+</link>" | sed -n 's/.*\/\([0-9]*\)<\/link>.*/\1/p' > cleaned_numbers.csv
"""

file_newid= "cleaned_numbers.csv"
file_full= "full_id.csv"
file_nessus = "data/nessus-kb.csv"
df_nuovo = pd.read_csv("plugin/nessus/cleaned_numbers.csv", header=None)
df_full = pd.read_csv("plugin/nessus/full_id.csv", header=None)
df_key = pd.read_csv('plugin/nessus/keyforget.csv' , header=None)
keyforget= df_key.iloc[0, 0]
numeri_esistenti = df_full.values.flatten().tolist()
numeri_nuovi = df_nuovo.values.flatten().tolist()

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
            json_data_list.append(response.json().get("pageProps").get("plugin"))     # Ottieni il JSON dalla risposta
            
             # Creazione di un DataFrame temporaneo per la nuova riga
            new_row = pd.DataFrame([ID], columns=['cves'])
            new_row ['cves'] = new_row ['cves'].astype(str)

            # Pulizia della colonna 'cves'
            new_row['cves'] = new_row['cves'].str.replace('[\'\[\]]', '', regex=True)
            # Aggiungi la riga pulita al DataFrame principale
            df_full = pd.concat([df_full, new_row], ignore_index=True)
            #df_full = df_full.append([ID], ignore_index=True)

            print(str(ID)+" andato\n")
        
        else:
            print("La richiesta non è riuscita. Codice di stato:", response.status_code)
except Exception as e:
    print(f"curl on {str(ID)} ha generato un errore: {str(e)}")
finally:
    print("TODO gestione salvataggio parziale")
    df_full.to_csv(file_full, index=False, header=False)
    df = pd.concat([pd.DataFrame(json_data_list), pd.read_csv(file_nessus)], ignore_index=True, sort=False)
    #df = pd.DataFrame(json_data_list) 
    df.to_csv(file_nessus, index=False)
