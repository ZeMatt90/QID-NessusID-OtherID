import pandas as pd

class DataMerger:
    def __init__(self, file1_path, file2_path, output_path):
        self.file1_path = file1_path
        self.file2_path = file2_path
        self.output_path = output_path

    def load_data(self):
        df1 = pd.read_csv(self.file1_path, keep_default_na=False, na_values=[''], low_memory=False)
        df2 = pd.read_csv(self.file2_path, keep_default_na=False, na_values=[''], low_memory=False)
        return df1, df2

    def merge_data(self, df1, df2):
        merged_df = pd.concat([df1, df2], ignore_index=True)
        return merged_df

    def save_data(self, merged_df):
        merged_df.to_csv(self.output_path, index=False)

    def process(self):
        df1, df2 = self.load_data()
        merged_df = self.merge_data(df1, df2)
        print(merged_df)
        self.save_data(merged_df)

# Utilizzo della classe
file1_path = 'data/1.csv'
file2_path = 'data/2.csv'
output_path = 'data/nessus-full.csv'

data_merger = DataMerger(file1_path, file2_path, output_path)
data_merger.process()


"""
# Confronta le liste di tipi di dati
differences = types_df1_str != types_df2_str
i=0
# Ottieni le colonne con differenze
for n in types_df1_str:
    i+=1
    if ( types_df1_str != types_df2_str and i<10):
        print(i)
        print("stampa differenzeeeeeee\n\n\n")
        print( types_df1_str)
        print( types_df2_str)
# Stampa le differenze
print("Differenze nei tipi di dati tra i due DataFrame:")
print(differences)
"""

"""
#funzionante, controlla i due DataFrame, consideriamo sia il tipo di dati che il valore effettivo presente in ciascuna cella. Quindi, se il tipo di dati e il valore sono gli stessi in una determinata cella tra i due DataFrame, consideriamo quei dati "uguali".
import pandas as pd

# Carica i due file CSV
file1_path = 'data/1.csv'
file2_path = 'data/2.csv'

# Carica i dati specificando i tipi di dati e gestendo i tipi misti
df1 = pd.read_csv(file1_path, keep_default_na=False, na_values=[''], low_memory=False)
df2 = pd.read_csv(file2_path, keep_default_na=False, na_values=[''], low_memory=False)

# Funzione per inferire il tipo di dati di ogni colonna
def infer_column_types(df):
    inferred_types = {}
    for column in df.columns:
        inferred_type = pd.api.types.infer_dtype(df[column], skipna=True)
        inferred_types[column] = inferred_type
    return inferred_types

# Inferisci il tipo di dati per ciascuna colonna
types_df1 = infer_column_types(df1)
types_df2 = infer_column_types(df2)

# Unisci i tipi di dati tra i due DataFrame
common_columns = set(df1.columns).intersection(set(df2.columns))
common_types = {col: pd.api.types.infer_dtype(types_df1[col], skipna=True) for col in common_columns}

# Seleziona solo le colonne comuni per ciascun DataFrame
df1_common = df1[common_columns]
df2_common = df2[common_columns]

# Carica nuovamente i DataFrame specificando i tipi di dati inferiti
df1_common = pd.read_csv(file1_path, usecols=common_columns, dtype=common_types, keep_default_na=False, na_values=[''], low_memory=False)
df2_common = pd.read_csv(file2_path, usecols=common_columns, dtype=common_types, keep_default_na=False, na_values=[''], low_memory=False)

# Identifica le righe che sono diverse tra i due DataFrame
differences = df1_common.ne(df2_common)

# Stampa le differenze
print("Differenze nei dati tra i due DataFrame:")
print(differences)
"""