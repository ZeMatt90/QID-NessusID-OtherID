from typing_extensions import deprecated
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing



class ArcadiaDictionary:
    def __init__(self, nessus_csv, qualys_csv, allcve_csv, output_csv):
        self.nessus_csv = nessus_csv
        self.qualys_csv = qualys_csv
        self.allcve_csv = allcve_csv
        self.output_csv = output_csv
        self.df_nessus = None
        self.df_qualys = None
        self.df_cve = None

    
    def load_data(self):
        """
        load CSV
        """
        self.df_nessus = pd.read_csv(self.nessus_csv, usecols=['cves', 'doc_id', 'solution', 'see_also'])
        self.df_qualys = pd.read_csv(self.qualys_csv, usecols=['CVE ID', 'QID', 'Title'])
        self.df_cve = pd.read_csv(self.allcve_csv)
    # Pulizia dei dati
        self.df_nessus['cves'] = self.df_nessus['cves'].fillna('')
        self.df_qualys['CVE ID'] = self.df_qualys['CVE ID'].fillna('')

    def filter_cve_to_update(self):
        """
        load only new CVEs
        """
        return self.df_cve[(self.df_cve['Updated'].isna()) | (self.df_cve['Updated'] == 'no')]

    def process_cve(self, cve_value):
        """
        process CVE
        """
        qualys_filter = self.df_qualys['CVE ID'].str.contains(cve_value, regex=False)
        nessus_filter = self.df_nessus['cves'].str.contains(cve_value, regex=False)
        
        qualys_values = self.df_qualys[qualys_filter]['QID'].tolist()
        nessus_values = self.df_nessus[nessus_filter]['doc_id'].tolist()

        # versione da verificare, elimina i dati duplicati direttamente nei risultati
        # qualys_values = list(set(self.df_qualys[qualys_filter]['QID'].tolist()))
        # nessus_values = list(set(self.df_nessus[nessus_filter]['doc_id'].tolist()))

        
        # if nessus_values and qualys_values:
        return {
            'CVE': cve_value,
            'QID': qualys_values,
            'doc_id': nessus_values,
            'Vari titoli Qualys': self.df_qualys[qualys_filter]['Title'].tolist(),
            'possibili soluzioni Nessus': self.df_nessus[nessus_filter]['solution'].tolist(),
            'info aggiuntive Nessus': self.df_nessus[nessus_filter]['see_also'].tolist(),
            # 'info': ""
        }

    # Funzione per processare i CVE in parallelo usando il multiprocessing
    @deprecated
    def parallel_processing_multiprocess(self, df_cve_to_update):
        nuove_righe = []
        
        # Definisci il numero di processi in base al numero di CPU disponibili
        num_processes = multiprocessing.cpu_count() - 1  # Lascia una CPU libera
        
        # Creiamo il pool di processi
        with multiprocessing.Pool(processes=num_processes) as pool:
            # Prepariamo i dati per il multiprocessing (argomenti per la funzione)
            tasks = [(cve, self.df_qualys, self.df_nessus) for cve in df_cve_to_update['CVE']]
            
            # Usare imap_unordered per eseguire le funzioni in parallelo e ottenere i risultati man mano che vengono pronti
            for result in tqdm(pool.imap_unordered(process_cve_multiprocess, tasks), total=len(df_cve_to_update['CVE']), desc="Processing CVE", bar_format="{l_bar}{bar:10}{r_bar}{remaining}", dynamic_ncols=True):
                if result is not None:
                    nuove_righe.append(result)
        
        # Aggiorno la colonna Updated
        self.df_cve.loc[self.df_cve['CVE'].isin(df_cve_to_update['CVE']), 'Updated'] = 'yes'
        
        return nuove_righe
    
    def sequential_processing(self, df_cve_to_update):
        nuove_righe = []
        
        # Iteriamo su ogni CVE da processare
        for cve in tqdm(df_cve_to_update['CVE'], desc="Processing CVE", bar_format="{l_bar}{bar:10}{r_bar}{remaining}", dynamic_ncols=True):
            result = self.process_cve(cve)
            if result is not None:
                nuove_righe.append(result)
        
        # Aggiorno la colonna Updated
        self.df_cve.loc[self.df_cve['CVE'].isin(df_cve_to_update['CVE']), 'Updated'] = 'yes'
        
        return nuove_righe

    # Funzione per processare i CVE in parallelo usando multithread
    @deprecated
    def parallel_processing(self, df_cve_to_update):
        # Ottieni il numero di CPU disponibili per il parallelismo con i thread
        # num_threads = multiprocessing.cpu_count()  # Numero di thread che vogliamo usare
        num_threads = 12#min(multiprocessing.cpu_count() - 1, 4)
        
        nuove_righe = []
        
        # Creiamo il pool di thread
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Inviamo ogni task individualmente con submit, per ottenere risultati appena completati
            futures = {executor.submit(self.process_cve, cve): cve for cve in df_cve_to_update['CVE']}
            
            # Barra di avanzamento che si aggiorna man mano che i thread completano
            for future in tqdm(as_completed(futures), total=len(df_cve_to_update['CVE']), desc="Processing CVE", bar_format="{l_bar}{bar:10}{r_bar}{remaining}", dynamic_ncols=True):
                result = future.result()
                if result is not None:
                    nuove_righe.append(result)
        
        # Aggiorno la colonna Updated
        self.df_cve.loc[self.df_cve['CVE'].isin(df_cve_to_update['CVE']), 'Updated'] = 'yes'
        
        return nuove_righe
    
    def update(self):
        # Carica i dati dai CSV
        self.load_data()
        
        # Filtra le CVE da aggiornare
        df_cve_to_update = self.filter_cve_to_update()
        
        nuove_righe = self.sequential_processing(df_cve_to_update)
        #nuove_righe = self.parallel_processing_multiprocess(df_cve_to_update)
        # nuove_righe = self.parallel_processing(df_cve_to_update)
        
        # Converti le nuove righe in un DataFrame
        df_values = pd.DataFrame([x for x in nuove_righe if x is not None])
        
        # Carica il CSV esistente che contiene i dati vecchi
        df_existing = pd.read_csv(self.output_csv)
        # Check if df_values is empty before attempting the merge
        if df_values.empty:
            # If there are no new values, just keep df_existing as it is
            #df_merged = df_existing
            pass
        else:
            # Esegui un full outer join tra df_existing e df_values sulla colonna CVE
            df_merged = pd.merge(df_existing, df_values, on='CVE', how='outer', suffixes=('_existing', '_new'), validate="many_to_many")

            # # Mantieni le colonne da df_existing e df_values (esempio per alcune colonne che hai menzionato)
            # Verifica l'esistenza di ogni colonna prima di combinare
            if 'QID_new' in df_merged.columns and 'QID_existing' in df_merged.columns:
                df_merged['QID'] = df_merged['QID_new'].combine_first(df_merged['QID_existing'])

            if 'doc_id_new' in df_merged.columns and 'doc_id_existing' in df_merged.columns:
                df_merged['doc_id'] = df_merged['doc_id_new'].combine_first(df_merged['doc_id_existing'])   

            if 'Vari titoli Qualys_new' in df_merged.columns and 'Vari titoli Qualys_existing' in df_merged.columns:
                df_merged['Vari titoli Qualys'] = df_merged['Vari titoli Qualys_new'].combine_first(df_merged['Vari titoli Qualys_existing'])

            if 'possibili soluzioni Nessus_new' in df_merged.columns and 'possibili soluzioni Nessus_existing' in df_merged.columns:
                df_merged['possibili soluzioni Nessus'] = df_merged['possibili soluzioni Nessus_new'].combine_first(df_merged['possibili soluzioni Nessus_existing'])

            if 'info aggiuntive Nessus_new' in df_merged.columns and 'info aggiuntive Nessus_existing' in df_merged.columns:
                df_merged['info aggiuntive Nessus'] = df_merged['info aggiuntive Nessus_new'].combine_first(df_merged['info aggiuntive Nessus_existing'])

            # Mantieni la colonna info solo da df_existing, se esiste
            if 'info_existing' in df_merged.columns:
                df_merged['info'] = df_merged['info_existing']
        
            # Rimuovi le colonne temporanee
            df_merged = df_merged.drop(columns=[col for col in df_merged.columns if col.endswith('_new') or col.endswith('_existing')])
        
            # Ora df_merged ha tutte le righe e i valori aggiornati

            # Scrivi il file aggiornato nel CSV esistente
            df_merged.to_csv(self.output_csv, index=False)

            # Salva anche il file con il flag 'Updated' settato correttamente
            self.df_cve.to_csv(self.allcve_csv, index=False)

# Funzione per processare un CVE (deve essere esterna per funzionare con multiprocessing)
@deprecated
def process_cve_multiprocess(args):
    cve_value, df_qualys, df_nessus = args
    
    qualys_filter = df_qualys['CVE ID'].str.contains(cve_value, regex=False)
    nessus_filter = df_nessus['cves'].str.contains(cve_value, regex=False)
    
    qualys_values = df_qualys[qualys_filter]['QID'].tolist()
    nessus_values = df_nessus[nessus_filter]['doc_id'].tolist()

    return {
        'CVE': cve_value,
        'QID': qualys_values,
        'doc_id': nessus_values,
        'Vari titoli Qualys': df_qualys[qualys_filter]['Title'].tolist(),
        'possibili soluzioni Nessus': df_nessus[nessus_filter]['solution'].tolist(),
        'info aggiuntive Nessus': df_nessus[nessus_filter]['see_also'].tolist(),
    }


# Esempio di utilizzo della classe
if __name__ == "__main__":
    processor = ArcadiaDictionary("data/nessus-kb.csv", "data/qualys-kb.csv", "data/all_cve.csv", "data/dictionary.csv")
    processor.update()

