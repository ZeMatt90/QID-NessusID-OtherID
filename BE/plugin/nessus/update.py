import aiohttp
import asyncio
import pandas as pd
import re
from .tenable_scraper import  TenableScraper

class NessusUpdater:
    """
    Classe per aggiornare i dati dei plugin Nessus scaricando le informazioni
    necessarie tramite richieste HTTP asincrone.

    Attributi:
        base_url (str): L'URL di base per le richieste HTTP.
        file_newid (str): Percorso al file CSV contenente i nuovi ID da scaricare.
        file_full (str): Percorso al file CSV contenente gli ID completi.
        file_nessus (str): Percorso al file CSV dei dati Nessus.
        keyforget_file (str): Percorso al file CSV contenente il 'keyforget' per la costruzione delle URL.
    """
    def __init__(self, base_url, file_newid, file_full, file_nessus, keyforget_file):
        """
        Inizializza la classe NessusUpdater con i percorsi dei file e l'URL di base.

        Args:
            base_url (str): L'URL di base per le richieste HTTP.
            file_newid (str): Percorso al file CSV contenente i nuovi ID da scaricare.
            file_full (str): Percorso al file CSV contenente gli ID completi.
            file_nessus (str): Percorso al file CSV dei dati Nessus.
            keyforget_file (str): Percorso al file CSV contenente il 'keyforget' per la costruzione delle URL.
        """
        self.base_url = base_url
        self.file_newid = file_newid
        self.file_full = file_full
        self.file_nessus = file_nessus
        self.keyforget_file = keyforget_file
        self.init_scrapering()

    def init_scrapering(self):
        """
        Effettua due richieste una per scaricare una chiave necessaria per scaricare con la seconda richiesta i plugin nuovi
        Args:
 
        Returns:
 
        """
        scraper = TenableScraper()
        scraper.fetch_and_process_build_manifest(
            'https://www.tenable.com/plugins/nessus/186284',
            'keyforget.csv'
        )
        scraper.fetch_and_process_plugin_numbers(
            'https://www.tenable.com/plugins/feeds?sort=newest',
            'cleaned_numbers.csv'
        )

    async def fetch_url(self, session, url):
        """
        Effettua una richiesta HTTP asincrona per ottenere i dati del plugin Nessus.

        Args:
            session (aiohttp.ClientSession): La sessione HTTP.
            url (str): L'URL da cui scaricare i dati.

        Returns:
            dict: I dati del plugin estratti dalla risposta JSON.
        """
        async with session.get(url) as response:
            data = await response.json()
            page_props = data.get("pageProps")
            plugin_data = page_props.get("plugin")
            
            print(f"\nandato: {url}\n")
            cves_tmp = re.sub('[\'\[\]]', '', str(plugin_data['cves']))
            plugin_data['cves'] = cves_tmp
            return plugin_data

    async def async_version(self, urls):
        """
        Gestisce le richieste HTTP asincrone parallele.

        Args:
            urls (list): Lista di URL da cui scaricare i dati.

        Returns:
            list: Lista di risultati dalle richieste HTTP.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_url(session, url) for url in urls]
            return await asyncio.gather(*tasks)

    async def process(self):
        """
        Carica i file CSV, filtra gli ID, genera le URL e aggiorna i file CSV con i nuovi dati.
        """
        ds_nuovo = pd.read_csv(self.file_newid, header=None, dtype=int).iloc[:, 0]
        ds_full = pd.read_csv(self.file_full, header=None, dtype=int).iloc[:, 0]
        df_key = pd.read_csv(self.keyforget_file, header=None)
        keyforget = df_key.iloc[0, 0]

        IDs = [numero for numero in ds_nuovo if numero not in ds_full]
        print("\n nuovi numeri da aggiungere\n\n")
        print(IDs)
        
        base_url = self.base_url + str(keyforget) + "/en/plugins/nessus/NUMEROID.json?type=nessus&id=NUMEROID"
        json_data_list = []

        try:
            urls = [base_url.replace("NUMEROID", str(ID)) for ID in IDs]
            results = await self.async_version(urls)
            
            for result in results:
                print(f"manage: {result['doc_id']}, ")
                if result is not None:
                    json_data_list.append(result)
                    ds_full = ds_full.append(pd.Series(int(result['doc_id'])), ignore_index=True)
                    print(str(result['doc_id']) + "*inserito.")
                else:
                    print("plugin data none")
        except Exception as e:
            print(f"Errore: {str(e)}")
        finally:
            print("Salvataggio degli aggiornamenti effettuati")
            ds_full.to_csv(self.file_full, header=False, index=False)

            df = pd.concat([pd.DataFrame(json_data_list), pd.read_csv(self.file_nessus)], ignore_index=True, sort=False)
            df.to_csv(self.file_nessus, index=False)

if __name__ == "__main__":
    nessus_updater = NessusUpdater(
        base_url="https://www.tenable.com/_next/data/",
        file_newid="plugin/nessus/cleaned_numbers.csv",
        file_full="plugin/nessus/full_id.csv",
        file_nessus="data/nessus-kb.csv",
        keyforget_file="plugin/nessus/keyforget.csv"
    )

    asyncio.run(nessus_updater.process())