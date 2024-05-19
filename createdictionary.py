import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool

# Carica i file CSV
def load_data():
    df_nessus = pd.read_csv("data/nessus-kb.csv", usecols=['cves', 'doc_id', 'solution', 'see_also'])
    df_qualys = pd.read_csv("data/qualys-kb.csv", usecols=['CVE ID', 'QID', 'Title'])
    df_cve = pd.read_csv("data/all_cve.csv")
    
    df_nessus['cves'] = df_nessus['cves'].fillna('')
    df_qualys['CVE ID'] = df_qualys['CVE ID'].fillna('')
    
    return df_nessus, df_qualys, df_cve

df_nessus, df_qualys, df_cve = load_data()

# Filtro i CVE che devono essere processati
df_cve_to_update = df_cve[(df_cve['Updated'].isna()) | (df_cve['Updated'] == 'no')]

# Funzione per processare un CVE
def process_cve(cve_value):
    qualys_filter = df_qualys['CVE ID'].str.contains(cve_value, regex=False)
    nessus_filter = df_nessus['cves'].str.contains(cve_value, regex=False)
    
    qualys_values = df_qualys[qualys_filter]['QID'].tolist()
    nessus_values = df_nessus[nessus_filter]['doc_id'].tolist()
    
    if nessus_values and qualys_values:
        return {
            'CVE': cve_value,
            'QID': qualys_values,
            'doc_id': nessus_values,
            'Vari titoli Qualys': df_qualys[qualys_filter]['Title'].tolist(),
            'possibili soluzioni Nessus': df_nessus[nessus_filter]['solution'].tolist(),
            'info aggiuntive Nessus': df_nessus[nessus_filter]['see_also'].tolist(),
            'info': ""
        }

# Esegui la funzione process_cve in parallelo
def parallel_processing(df_cve_to_update):
    with Pool() as pool:
        nuove_righe = list(tqdm(pool.imap(process_cve, df_cve_to_update['CVE']), total=len(df_cve_to_update['CVE']), desc="Processing CVE", bar_format="{l_bar}{bar:10}{r_bar}{remaining}"))
        # Aggiorno la colonna Updated
        df_cve.loc[df_cve['CVE'].isin(df_cve_to_update['CVE']), 'Updated'] = 'yes'
    
    return nuove_righe

nuove_righe = parallel_processing(df_cve_to_update)

df_values = pd.DataFrame([x for x in nuove_righe if x is not None])

df_values.to_csv("data/dictionary.csv", index=False)
df_cve.to_csv("data/all_cve.csv", index=False)


