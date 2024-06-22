import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool

class ArcadiaDictionary:
    def __init__(self, nessus_csv, qualys_csv, allcve_csv, output_csv):
        self.nessus_csv = nessus_csv
        self.qualys_csv = qualys_csv
        self.allcve_csv = allcve_csv
        self.output_csv = output_csv
        self.df_nessus = None
        self.df_qualys = None
        self.df_cve = None

    # Carica i file CSV
    def load_data(self):
        self.df_nessus = pd.read_csv(self.nessus_csv, usecols=['cves', 'doc_id', 'solution', 'see_also'])
        self.df_qualys = pd.read_csv(self.qualys_csv, usecols=['CVE ID', 'QID', 'Title'])
        self.df_cve = pd.read_csv(self.allcve_csv)
        
        self.df_nessus['cves'] = self.df_nessus['cves'].fillna('')
        self.df_qualys['CVE ID'] = self.df_qualys['CVE ID'].fillna('')

    # Filtro i CVE che devono essere processati
    def filter_cve_to_update(self):
        return self.df_cve[(self.df_cve['Updated'].isna()) | (self.df_cve['Updated'] == 'no')]

    # Funzione per processare un CVE
    def process_cve(self, cve_value):
        qualys_filter = self.df_qualys['CVE ID'].str.contains(cve_value, regex=False)
        nessus_filter = self.df_nessus['cves'].str.contains(cve_value, regex=False)
        
        qualys_values = self.df_qualys[qualys_filter]['QID'].tolist()
        nessus_values = self.df_nessus[nessus_filter]['doc_id'].tolist()
        
        if nessus_values and qualys_values:
            return {
                'CVE': cve_value,
                'QID': qualys_values,
                'doc_id': nessus_values,
                'Vari titoli Qualys': self.df_qualys[qualys_filter]['Title'].tolist(),
                'possibili soluzioni Nessus': self.df_nessus[nessus_filter]['solution'].tolist(),
                'info aggiuntive Nessus': self.df_nessus[nessus_filter]['see_also'].tolist(),
                'info': ""
            }

    # Esegui la funzione process_cve in parallelo
    def parallel_processing(self, df_cve_to_update):
        with Pool() as pool:
            nuove_righe = list(tqdm(pool.imap(self.process_cve, df_cve_to_update['CVE']), total=len(df_cve_to_update['CVE']), desc="Processing CVE", bar_format="{l_bar}{bar:10}{r_bar}{remaining}"))
            # Aggiorno la colonna Updated
            self.df_cve.loc[self.df_cve['CVE'].isin(df_cve_to_update['CVE']), 'Updated'] = 'yes'
        
        return nuove_righe

    def update(self):
        self.load_data()
        df_cve_to_update = self.filter_cve_to_update()
        nuove_righe = self.parallel_processing(df_cve_to_update)
        df_values = pd.DataFrame([x for x in nuove_righe if x is not None])
        df_values.to_csv(self.output_csv, index=False)
        self.df_cve.to_csv(self.allcve_csv, index=False)


# Esempio di utilizzo della classe
if __name__ == "__main__":
    processor = ArcadiaDictionary("data/nessus-kb.csv", "data/qualys-kb.csv", "data/all_cve.csv", "data/dictionary.csv")
    processor.update()