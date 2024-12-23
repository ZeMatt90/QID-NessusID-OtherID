import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool

nessus_csv = "data/nessus-kb.csv"
qualys_csv = "data/qualys-kb.csv"
allcve_csv = "data/all_cve-light.csv"
dictionary_csv = "data/dictionary-light.csv"

df_nessus = pd.read_csv(nessus_csv, usecols=['cves', 'doc_id','solution','see_also'])
df_qualys = pd.read_csv(qualys_csv, usecols=['CVE ID', 'QID','Title'])
df_cve = pd.read_csv(allcve_csv)
df_nessus['cves'] = df_nessus['cves'].fillna('')
df_qualys['CVE ID'] = df_qualys['CVE ID'].fillna('')

"""
funzione process_cve che prende un valore CVE 
e restituisce un dizionario contenente le informazioni rilevanti.
Utilizzo quindi il modulo multiprocessing.Pool per eseguire in parallelo la funzione process_cve per ogni valore CVE
"""

def process_cve(cve_value):
    qualys_values = df_qualys[df_qualys['CVE ID'].str.split(',').apply(lambda x: cve_value in x)]['QID'].tolist()
    nessus_values = df_nessus[df_nessus['cves'].str.split(',').apply(lambda x: cve_value in x)]['doc_id'].tolist()
    if nessus_values and qualys_values:
        return {
            'CVE': cve_value, 'QID': qualys_values,'doc_id':nessus_values,
            'Vari titoli Qualys': df_qualys[df_qualys['CVE ID'].str.split(',').apply(lambda x: cve_value in x)]['Title'].tolist(),
            'possibili soluzioni Nessus': df_nessus[df_nessus['cves'].str.split(',').apply(lambda x: cve_value in x)]['solution'].tolist(), 
            'info aggiuntive Nessus': df_nessus[df_nessus['cves'].str.split(',').apply(lambda x: cve_value in x)]['see_also'].tolist(),
            'info': ""
        }




#with tqdm(total=len(df_cve['CVE']), desc="Processing CVE", bar_format="{l_bar}{bar:10}{r_bar}{remaining}") as bar:
with Pool() as pool:
    nuove_righe = list(tqdm(pool.imap(process_cve, df_cve['CVE']), total=len(df_cve['CVE']), desc="Processing CVE", bar_format="{l_bar}{bar:10}{r_bar}{remaining}"))

df_values = pd.DataFrame([x for x in nuove_righe if x is not None])



"""
import pandas as pd
import csv
from tqdm import tqdm

nessus_csv = "data/nessus-kb.csv"
qualys_csv = "data/qualys-kb.csv"
allcve_csv = "data/all_cve-light.csv"
dictionary_csv = "data/dictionary-light.csv"

df_nessus = pd.read_csv(nessus_csv, usecols=['cves', 'doc_id','solution','see_also'])
df_qualys = pd.read_csv(qualys_csv, usecols=['CVE ID', 'QID','Title'])
df_cve = pd.read_csv(allcve_csv)
df_nessus['cves'] = df_nessus['cves'].fillna('')
df_qualys['CVE ID'] = df_qualys['CVE ID'].fillna('')

nuove_righe = []


with tqdm(total=len(df_cve['CVE']), desc="Processing CVE", bar_format="{l_bar}{bar:10}{r_bar}{remaining}") as bar:
    for cve_value in df_cve['CVE']:
        
        qualys_values = df_qualys[df_qualys['CVE ID'].str.split(',').apply(lambda x: cve_value in x)]['QID'].tolist()
        nessus_values = df_nessus[df_nessus['cves'].str.split(',').apply(lambda x: cve_value in x)]['doc_id'].tolist()
        if nessus_values != [] and qualys_values !=[]:
            nuove_righe.append({
                'CVE': cve_value, 'QID': qualys_values,'doc_id':nessus_values,
                'Vari titoli Qualys': df_qualys[df_qualys['CVE ID'].str.split(',').apply(lambda x: cve_value in x)]['Title'].tolist(),
                 'possibili soluzioni Nessus': df_nessus[df_nessus['cves'].str.split(',').apply(lambda x: cve_value in x)]['solution'].tolist(), 
                 'info aggiuntive Nessus': df_nessus[df_nessus['cves'].str.split(',').apply(lambda x: cve_value in x)]['see_also'].tolist(),
                 'info': ""
                 })
        #print("\n qualys\n",qualys_values,df_qualys['CVE ID'].str.split(',').apply(lambda x: cve_value in x))
        #print("\n nessus\n",nessus_values)
        bar.update(1)

df_values = pd.DataFrame(nuove_righe)
"""

"""
# Carica il file CSV
df = pd.read_csv(allcve_csv)

# Estrai la parte numerica dell'ID
df['Numero'] = df['ID'].str.extract('-(\d+)$').astype(int)
# Aggiungi zeri alla parte numerica per avere una lunghezza di 5 cifre
df['Numero_Formattato'] = df['Numero'].apply(lambda x: f'{x:05}')

# Ordina il DataFrame in base all'anno e alla parte numerica formattata
df = df.sort_values(by=['Anno', 'Numero_Formattato'])

# Elimina le colonne intermedie se necessario
df = df.drop(columns=['Numero', 'Numero_Formattato'])

# Salva il DataFrame ordinato in un nuovo file CSV
df.to_csv('tuo_file_ordinato.csv', index=False)
"""


df_values.to_csv(dictionary_csv, index=False)
#df_values.to_csv(dictionary_csv, index=False, quoting=csv.QUOTE_NONE, escapechar=' ')  #servirebbe per rimuovere le aggiunte di ""
