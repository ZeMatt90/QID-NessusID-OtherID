import pandas as pd
from tqdm import tqdm
from colorama import Fore, Back, Style, init

class CveUpdater:
    def __init__(self, nessus_csv, qualys_csv, allcve_csv):
        self.nessus_csv = nessus_csv
        self.qualys_csv = qualys_csv
        self.allcve_csv = allcve_csv
        
    def process(self):
        df_nessus = pd.read_csv(self.nessus_csv)
        df_qualys = pd.read_csv(self.qualys_csv)
        nessus_values = []
        qualys_values = []
        nessus_dates = {}

        with tqdm(total=len(df_nessus), desc="Processing Nessus", bar_format="{l_bar}{bar:10}{r_bar}{remaining}") as bar:
            for _, row in df_nessus.iterrows():
                cves = row['cves']
                if isinstance(cves, str):
                    date = row['plugin_modification_date']
                    for cve in cves.split(','):
                        nessus_values.append(cve)
                        nessus_dates[cve] = date
                bar.update(1)

        with tqdm(total=len(df_qualys['CVE ID']), desc="Processing Qualys", bar_format="{l_bar}{bar:10}{r_bar}{remaining}") as bar:
            for row in df_qualys['CVE ID']:
                if isinstance(row, str):
                    qualys_values.extend(row.split(','))
                bar.update(1)

        df_nessus_values = pd.DataFrame({'CVE': nessus_values})
        df_qualys_values = pd.DataFrame({'CVE': qualys_values})

        merged_df = pd.concat([df_qualys_values, df_nessus_values], ignore_index=True)
        merged_df = merged_df.sort_values(by='CVE', ascending=False)
        merged_df = merged_df.drop_duplicates(subset='CVE')

        df_all_cve = pd.read_csv(self.allcve_csv)

        uptime = []
        updated = []

        for _, row in df_all_cve.iterrows():
            cve = row['CVE']
            if cve in nessus_dates:
                new_uptime = nessus_dates[cve]
                if 'Uptime' in df_all_cve.columns and pd.notna(row['Uptime']):
                    if row['Uptime'] < new_uptime:
                        uptime.append(new_uptime)
                        updated.append('no')
                    else:
                        uptime.append(row['Uptime'])
                        updated.append('yes')
                else:
                    uptime.append(new_uptime)
                    updated.append('no')
            else:
                uptime.append(row['Uptime'] if 'Uptime' in df_all_cve.columns else None)
                updated.append('yes' if 'Updated' in df_all_cve.columns and pd.notna(row['Updated']) else 'no')

        df_all_cve['Uptime'] = uptime
        df_all_cve['Updated'] = updated

        df_all_cve.to_csv(self.allcve_csv, index=False)

if __name__ == '__main__':
    # Esempio di utilizzo della classe
    if __name__ == "__main__":
        processor = CveUpdater("data/nessus-kb.csv", "data/qualys-kb.csv", "data/all_cve.csv")
        processor.process()
