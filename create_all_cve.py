import pandas as pd
from tqdm import tqdm
from colorama import Fore, Back, Style, init



nessus_csv = "data/nessus-kb.csv"
qualys_csv = "data/qualys-kb.csv"
allcve_csv = "data/all_cve.csv"

df_nessus = pd.read_csv(nessus_csv)
df_qualys = pd.read_csv(qualys_csv)
nessus_values = []
qualys_values = []

with tqdm(total=len(df_nessus['cves']), desc="Processing nessus", bar_format="{l_bar}{bar:10}{r_bar}{remaining}") as bar:
    for row in df_nessus['cves']:
        if isinstance(row, str) :
            nessus_values.extend(row.split(','))
        bar.update(1)

with tqdm(total=len(df_qualys['CVE ID']), desc="Processing qualys", bar_format="{l_bar}{bar:10}{r_bar}{remaining}") as bar:
    for row in df_qualys['CVE ID']:
        if isinstance(row, str) :
            qualys_values.extend(row.split(','))
        bar.update(1)
        #else:
        #    print("riga non inserita perchè nulla o diversa da stringa "+str(row))

df_nessus_values = pd.DataFrame({'CVE': nessus_values})
df_qualys_values = pd.DataFrame({'CVE': qualys_values})

merged_df = pd.concat([df_qualys_values, df_nessus_values], ignore_index=True)
merged_df = merged_df.sort_values(by='CVE',ascending=False)
merged_df = merged_df.drop_duplicates(subset='CVE')


#print(merged_df)

merged_df.to_csv(allcve_csv, index=False)
