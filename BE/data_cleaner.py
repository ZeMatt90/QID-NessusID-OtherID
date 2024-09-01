import pandas as pd

class DataCleaner:
    def __init__(self, file_fullidnessus, file_allcve, file_nessus, file_qualys, file_dictionary):
        self.file_fullidnessus = file_fullidnessus
        self.file_allcve = file_allcve
        self.file_nessus = file_nessus
        self.file_qualys = file_qualys
        self.file_dictionary = file_dictionary
        self.df_fullidnessus = pd.read_csv(self.file_fullidnessus, header=None)
        self.df_allcve = pd.read_csv(self.file_allcve)
        self.df_nessus = pd.read_csv(self.file_nessus)
        self.df_qualys = pd.read_csv(self.file_qualys)
        self.df_dictionary = pd.read_csv(self.file_dictionary)

    def checkdf(self, dfcheck, key=None):
        # Stampa i duplicati e rimuove i duplicati
        if key is None:
            duplicates_before = dfcheck[dfcheck.duplicated()]
            dfcheck = dfcheck.drop_duplicates()
        else:
            duplicates_before = dfcheck[dfcheck.duplicated(subset=[key], keep=False)]
            dfcheck = dfcheck.drop_duplicates(subset=[key], keep='first')
        
        print("Righe duplicate prima della rimozione:")
        print(duplicates_before)
        return dfcheck

    def deduplicate_and_save(self):
        # Verifica e rimozione duplicati in df_fullidnessus
        df_deduplicated = self.df_fullidnessus.drop_duplicates()
        result_df = df_deduplicated.stack().reset_index(drop=True)
        result_df.to_csv(self.file_fullidnessus, index=False)
        print("\n*********************\nIDnessus")
        # Verifica e rimozione duplicati in df_nessus
        print("\n*********************\nnessus doc_id")
        self.checkdf(self.df_nessus, 'doc_id').to_csv(self.file_nessus, index=False)
        # Verifica e rimozione duplicati in df_qualys
        print("\n*********************\nqualys qid")
        self.checkdf(self.df_qualys, 'QID').to_csv(self.file_qualys, index=False)
        # Verifica e rimozione duplicati in df_dictionary
        print("\n*********************\ndictionary cve")
        self.checkdf(self.df_dictionary, 'CVE').to_csv(self.file_dictionary, index=False)
        # Verifica e rimozione duplicati in df_allcve
        print("\n*********************\nall cve")
        self.checkdf(self.df_allcve).to_csv(self.file_allcve, index=False)

# Esempio di utilizzo della classe
if __name__ == "__main__":
    cleaner = DataCleaner(
        file_fullidnessus="plugin/nessus/full_id.csv",
        file_allcve="data/all_cve.csv",
        file_nessus="data/nessus-kb.csv",
        file_qualys="data/qualys-kb.csv",
        file_dictionary="data/dictionary.csv"
    )
    cleaner.deduplicate_and_save()
