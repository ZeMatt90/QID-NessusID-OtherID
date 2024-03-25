import requests
import json
import pandas as pd
import re
import asyncio
import aiohttp
"""
prima di lanciare questo assicurarsi di aver aggiornato il file cleaned numerbers.csv tramite
curl -S https://www.tenable.com/plugins/feeds?sort=newest | grep -o "<link>https://www.tenable.com/plugins/nessus/[0-9]\+</link>" | sed -n 's/.*\/\([0-9]*\)<\/link>.*/\1/p' > cleaned_numbers.csv
"""

async def fetch_url(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            plugin_data = await response.json()
            plugin_data = plugin_data.get("pageProps").get("plugin")
            cves_tmp = re.sub('[\'\[\]]', '', str(plugin_data['cves']))
            plugin_data['cves'] = cves_tmp
            return plugin_data
        else:
            print(f"La richiesta non è riuscita per l'URL {url}. Codice di stato:", response.status)

async def async_fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def main():
    file_newid= "plugin/nessus/cleaned_numbers.csv"
    file_full= "plugin/nessus/full_id.csv"
    file_nessus = "data/nessus-kb.csv"

    df_nuovo = pd.read_csv(file_newid, header=None,dtype=int)
    df_full = pd.read_csv(file_full, header=None,dtype=int)
    df_key = pd.read_csv('plugin/nessus/keyforget.csv' , header=None)
    keyforget= df_key.iloc[0, 0]

    numeri_esistenti = df_full.values.flatten().tolist()
    numeri_nuovi = df_nuovo.values.flatten().tolist()

    #carico i nuovi id da scaricare, che non sono presenti in full_id.csv
    IDs = [numero for numero in numeri_nuovi if numero not in numeri_esistenti]
    print("\n nuovi numeri da aggiungere\n\n")
    print(IDs)
    base_url = "https://www.tenable.com/_next/data/"+str(keyforget)+"/en/plugins/nessus/NUMEROID.json?type=nessus&id=NUMEROID"
    json_data_list = []

    try:
        urls = [base_url.replace("NUMEROID", str(ID)) for ID in IDs]
        results = await async_fetch_all(urls)
        
        for plugin_data in results:
            if plugin_data is not None:
                json_data_list.append(plugin_data)
                new_id_inserito = pd.DataFrame([plugin_data['cves']], columns=['cves'])
                new_id_inserito['cves'] = new_id_inserito['cves'].astype(int)
                df_full = pd.concat([df_full, new_id_inserito], ignore_index=True)
                print(str(new_id_inserito['cves'].tolist()) + " andato\n")
    

            else:
                print("plugin data none")
    except Exception as e:
        print(f"un errore generico : {str(e)}")
    finally:
        print("salvataggio degli aggiornamenti effettuati")
        
        df_full.to_csv(file_full, header=False, index=False)

        df = pd.concat([pd.DataFrame(json_data_list), pd.read_csv(file_nessus)], ignore_index=True, sort=False)
        #df = pd.DataFrame(json_data_list) 
        df.to_csv(file_nessus, index=False)

asyncio.run(main())
