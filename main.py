import data_handling,canederli#user_interface
canederli.stampa_loading()
from main_module import *

print("imported all motors successfully from Arcadia\n" )
#print(canederli.HEADER1)


# Istanziamento della classe
data_handler = data_handling.DataHandler()
data_handler.load_data()
data_handler.display_summary()

# print("istanziati i dati e caricati in memoria al modico prezzo di %s byte",sys.getsizeof(data_handler))
# total_memory_usage = 0
# for df in [data_handler.nessusdata, data_handler.qualysdata, data_handler.arcadiadata]:
#     total_memory_usage += df.memory_usage(deep=True).sum()  # Calcola la dimensione effettiva dei DataFrame
# print(f"Dimensione totale: {total_memory_usage} byte")
