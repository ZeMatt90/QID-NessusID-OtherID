import aiohttp
import asyncio
import time
import pandas as pd
import re
from tenable_scraper import  TenableScraper

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
    def __init__(self, base_url, file_newid, file_full, file_nessus, keyforget_file,log):
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
        self.init_scrapering(log)

    def init_scrapering(self,log):
        """
        Effettua due richieste una per scaricare una chiave necessaria per scaricare con la seconda richiesta i plugin nuovi
        Args:
 
        Returns:
 
        """
        scraper = TenableScraper(log)
        scraper.fetch_and_process_build_manifest(
            'https://www.tenable.com/plugins/nessus/186284',
            'plugin/nessus/keyforget.csv'
            #'keyforget.csv'
        )
        scraper.fetch_and_process_plugin_numbers(
            'https://www.tenable.com/plugins/feeds?sort=newest',
            'plugin/nessus/cleaned_numbers.csv'
            #'cleaned_numbers.csv'
        )

        
    async def limited_fetch(self, session, url, semaphore):
        async with semaphore:
            return await self.fetch_url(session, url)

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
            # Controlla il tipo di contenuto della risposta
            content_type = response.headers.get('Content-Type')

            if 'application/json' in content_type:
                try:                    
                    data = await response.json()
                    # Verifica che data contenga "pageProps"
                    page_props = data.get("pageProps")
                    if page_props is None:
                        print(f"Errore: 'pageProps' non trovato nei dati per l'URL: {url}")
                        return None

                    # Verifica che "plugin" esista in pageProps
                    plugin_data = page_props.get("plugin")
                    if plugin_data is None:
                        print(f"Errore: 'plugin' non trovato in 'pageProps' per l'URL: {url}")
                        return None
                    
                    print(f"\nandato: {url}\n")

                    # Verifica se 'cves' esiste e non è None
                    if plugin_data.get('cves') is not None:
                        cves_tmp = re.sub('[\'\[\]]', '', str(plugin_data['cves']))
                    else:
                        cves_tmp = ''
                    
                    plugin_data['cves'] = cves_tmp
                    return plugin_data
                except aiohttp.ContentTypeError as e:
                    print(f"Errore nel parsing JSON: {str(e)}")
                    return None
            else:
                    # Se il contenuto non è JSON, gestisci l'errore
                    print(f"Errore: Contenuto non JSON ricevuto per l'URL: {url}, tipo di contenuto: {content_type}")
                    return None

    async def async_version(self, urls):
        """
        Gestisce le richieste HTTP asincrone parallele.

        Args:
            urls (list): Lista di URL da cui scaricare i dati.

        Returns:
            list: Lista di risultati dalle richieste HTTP.
        """
        semaphore = asyncio.Semaphore(2)  # Limita a 5 richieste simultanee
        delay_between_requests = 1 / 2  # 5 richieste al secondo = 0,5 secondi tra le richieste

        
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.limited_fetch(session, url, semaphore) 
                for url in urls
            ]
            await asyncio.sleep(delay_between_requests)
            results = await asyncio.gather(*tasks)
            return results


        # async with aiohttp.ClientSession() as session:
        #     tasks = []
        #     for url in urls:
        #         tasks.append(self.limited_fetch(session, url, semaphore))
        #         await asyncio.sleep(delay_between_requests)
        #     return await asyncio.gather(*tasks)
        

        # return await asyncio.gather(*tasks)

        # async with aiohttp.ClientSession() as session:
        #     tasks = [self.fetch_url(session, url) for url in urls]
        #     return await asyncio.gather(*tasks)

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
                if result is not None:
                    print(f"manage: {result['doc_id']}, ")
                    # Controlla se il doc_id è già presente nel ds_full
                    if int(result['doc_id']) not in ds_full.values:
                        json_data_list.append(result)
                        ds_full = pd.concat([ds_full, pd.Series([int(result['doc_id'])])], ignore_index=True)
                        print(str(result['doc_id']) + "*inserito.")
                    else:
                        print(f"doc_id {result['doc_id']} già presente in ds_full.")
                else:
                    print("plugin data none")

        finally:
            print("Salvataggio degli aggiornamenti effettuati\n" )
            print(json_data_list)
            ds_full.to_csv(self.file_full, header=False, index=False)

            df = pd.concat([pd.DataFrame(json_data_list), pd.read_csv(self.file_nessus)], ignore_index=True, sort=False)
            df.to_csv(self.file_nessus, index=False)

if __name__ == "__main__":
    nessus_updater = NessusUpdater(
        base_url="https://www.tenable.com/_next/data/",
        file_newid="cleaned_numbers.csv",
        file_full="full_id.csv",
        file_nessus="../../data/nessus-kb.csv",
        keyforget_file="keyforget.csv",
        log = "../../logs/tenable_scraper.log"
    )

    asyncio.run(nessus_updater.process())