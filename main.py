import data_handling,canederli#user_interface
canederli.stampa_loading()
from main_module import *
import subprocess

print("imported all motors successfully from Arcadia\n" )
#print(canederli.HEADER1)

data_handler = data_handling.DataHandler()
data_handler.load_data()
#data_handler.display_summary()
riga = data_handler.qualysdata[data_handler.qualysdata['QID'] == 38170]
print(riga)
riga = data_handler.qualysdata[data_handler.qualysdata['QID'] == 38173]
print(riga)
riga = data_handler.qualysdata[data_handler.qualysdata['QID'] == 38169]

if __name__ == '__main':
    #processo padre
    # Istanziamento della classe
    print ("1")
    data_handler = data_handling.DataHandler()
    data_handler.load_data()
    #data_handler.display_summary()
    riga = data_handler.qualysdata[data_handler.qualysdata['qid'] == 38170]
    print(riga)
    print ("2")
    # Definisci il comando per avviare l'app Streamlit
    #command = ["streamlit", "run", "user_interface.py"]  # Sostituisci con il nome corretto del tuo file Streamlit

        # Avvia l'app Streamlit come processo figlio
    #process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    
    # Attendi che il processo figlio termini
    #process.wait()

    # Leggi l'output standard e gli errori
    #output, errors = process.communicate()

    # Verifica eventuali errori
    #if process.returncode != 0:
    #    print(f"Errore nell'esecuzione. Codice di uscita: {process.returncode}")
    #    print("Errori standard:")
    #    print(errors.decode())
    #else:
    #    print("Esecuzione completata con successo")
    #    print("Output standard:")
    #    print(output.decode())
    # print("istanziati i dati e caricati in memoria al modico prezzo di %s byte",sys.getsizeof(data_handler))
    # total_memory_usage = 0
    # for df in [data_handler.nessusdata, data_handler.qualysdata, data_handler.arcadiadata]:
    #     total_memory_usage += df.memory_usage(deep=True).sum()  # Calcola la dimensione effettiva dei DataFrame
    # print(f"Dimensione totale: {total_memory_usage} byte")
else:
    #processi demone
    print ("a")
