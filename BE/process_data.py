import multiprocessing 
import data_handling
import pandas as pd
from multiprocessing import Pool
import time
from difflib import SequenceMatcher


def process_data_chunk(df_chunk, df2_complete, result_queue, idarcadia):
    try:
        for i, row1 in enumerate(df_chunk):
            for j, row2 in enumerate(df2_complete):
                cve1 = str(row1.get('CVE ID', ''))
                cve2 = str(row2.get('cves', []))
             
               # similarità tra i valori utilizzando SequenceMatcher
                similarity_cveid = SequenceMatcher(None, cve1, cve2).ratio()
                
                # misura complessiva di similarità basata sulle due chiavi
                overall_similarity = (similarity_cveid )#+ similarity_cves) / 2

                if overall_similarity>0.79:
                 #                   print("\nsimilarity overall:",overall_similarity)
                    result_row = {
                        "ID": idarcadia,
                        "similarity": overall_similarity,
                        #parte di qualys
                        "CVE ID qualys": row1.get('CVE ID', ''),
                        "QID": row1.get('QID', ''),
                        "Title": row1.get('Title', ''),
                        #parte di nessus 
                        "doc_id": row2.get('doc_id', ''),
                        "cves nessus": row2.get('cves', []),
                        "script name": row2.get('script_name', '')
                    }
                    result_queue.put(result_row)
    except Exception as e:
        print(f"Process {idarcadia} ha generato un errore: {str(e)}")
    #finally:
    #    print(f"Process {idarcadia} esce.")
    #print(f"Process {idarcadia} ha terminato.")

if __name__ == '__main__':
    try:
        num_processes = multiprocessing.cpu_count() 
        if num_processes >1:
            num_processes -=1
        data_handler =data_handling.DataHandler()
        data_handler.load_data()

        print("Dividi i DataFrame in chunk", num_processes)    
        chunk_size = len(data_handler.qualysdata) // num_processes
        df_chunks = [data_handler.qualysdata[i:i + chunk_size].copy() for i in range(0, len(data_handler.qualysdata), chunk_size)]
        # Converti i DataFrame in liste di dizionari
        df_chunks = [df.to_dict(orient='records') for df in df_chunks]
        
        # Crea una coda per i risultati
        result_queue = multiprocessing.Queue()

        # Crea e avvia i processi
        processes = []
        idArcadia= num_processes
        
        times = []
        time_init = time.time()

        for df_chunk in df_chunks:
            df2_complete = data_handler.nessusdata.copy()
            df2_complete = df2_complete.to_dict(orient='records')
            process = multiprocessing.Process(target=process_data_chunk, args=(df_chunk,df2_complete,result_queue,idArcadia))
            processes.append(process)
            idArcadia += 1
            process.start()
        result_dfs = []

        while True:
            running = any(p.is_alive() for p in processes)
            while not result_queue.empty():
                result = result_queue.get()
                result_dfs.append(result)
            if not running and result_queue.empty():
                break

        for process in processes:    
            process.join()
         # condizione di uscita in modo che il processo principale esca in modo pulito
        should_exit = True


        time_end = time.time()
        times.append(float(time_end - time_init))

        print("istanziati i dati e caricati in memoria al modico prezzo di %s byte",sys.getsizeof(df_chunks))
        total_memory_usage = 0
        for df in [data_handler.nessusdata, data_handler.qualysdata, data_handler.arcadiadata]:
          total_memory_usage += df.memory_usage(deep=True).sum()  #dimensione effettiva dei DataFrame
        print(f"Dimensione totale: {total_memory_usage} byte")

        print(f'Serial execution took {time_end - time_init}s.')
        print("**********FINE****************")
        final_result = pd.DataFrame(result_dfs)
        final_result.to_excel("./data/arcadia-light.xlsx", index=False)


    except Exception as e:
        print("Si è verificato un'errore:", str(e))