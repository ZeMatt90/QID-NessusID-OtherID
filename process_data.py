import multiprocessing 
import data_handling
from main_module import distance,pd

 

def process_data_chunk(df_chunk, df2_complete, result_df, idarcadia):
    # Creare un DataFrame vuoto per i risultati
    result_dfs = pd.DataFrame(columns=["ID", "Row1", "Row2", "Euclidean Distance"])
    
    for row1 in df_chunk.iterrows():
        print(row1)
        for row2 in df2_complete.iterrows():
            # Calcolo della distanza euclidea tra le due righe
            #euclidean_distance = distance.euclidean(row1 , row2)
            
            # Aggiungi la riga al DataFrame dei risultati
            #if euclidean_distance <= 100:
            result_dfs.concat([idarcadia, row1, row2,idarcadia])
                #result_df = result_df.append(result_row, ignore_index=True)

    # Metti il risultato nella coda
    result_df.put(result_dfs)


if __name__ == '__main__':
    # ... Altre operazioni di inizializzazione
    num_processes = multiprocessing.cpu_count()
    num_processes=1
    data_handler =data_handling.DataHandler()
    data_handler.load_data()

    print("Dividi i DataFrame in chunk")    
    chunk_size = len(data_handler.qualysdata) // num_processes  # Dividi in base al numero di processi desiderati
    df_chunks = [data_handler.qualysdata[i:i + chunk_size] for i in range(0, len(data_handler.qualysdata), chunk_size)]
    df2_complete= data_handler.nessusdata

    # Crea una coda per i risultati
    result_df = multiprocessing.Queue()

    # Crea e avvia i processi
    processes = []
    idArcadia= num_processes
    for df_chunk in df_chunks:
        process = multiprocessing.Process(target=process_data_chunk, args=(df_chunk,df2_complete,idArcadia, result_df))
        processes.append(process)
        idArcadia -=idArcadia
        process.start()

    print("Attendi che tutti i processi siano terminati")
    for process in processes:
        process.join()

    result_dfs = []
    print("Raccogli i risultati dalla coda")
    while not result_df.empty():
        result = result_df.get()
        result_dfs.append(result)

    # ... Resto del tuo codice
    final_result = pd.concat(result_dfs)

    print("fine elaborazione")
    final_result.to_excel("./data/arcadia-light2.xlsx", index=False)

