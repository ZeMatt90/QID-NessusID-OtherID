import pandas as pd
""" 1
Formato Parquet:

    Descrizione: Parquet è un formato di file columnar che è altamente efficiente per la compressione e la lettura/scrittura di dati tabulari.
    Vantaggi:
        Compressione migliore rispetto al CSV, riducendo la dimensione del file.
        Maggiore velocità di lettura e scrittura, specialmente per subset di colonne.
"""

df = pd.read_csv('data/dictionary.csv')
df.to_parquet('../FE/dictionary.parquet')

""" 2
Descrizione: HDF5 è un formato di file binario che supporta grandi dataset multidimensionali.
Vantaggi:

    Gestione efficiente di dataset molto grandi.
    Supporta la compressione e l'accesso a porzioni specifiche del dataset.
"""

#df = pd.read_csv('data/dictionary.csv')
df.to_hdf('../FE/dictionary.h5', key='df', mode='w')


""" 3
Descrizione: Feather è un formato di file binario ottimizzato per la velocità di lettura/scrittura con Pandas.
Vantaggi:

    Molto veloce per lettura e scrittura.
    Supportato nativamente da Pandas.
"""
#df = pd.read_csv('data/dictionary.csv')
df.to_feather('../FE/dictionary.feather')
