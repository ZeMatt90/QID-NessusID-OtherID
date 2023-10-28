import multiprocessing 
import data_handling
from main_module import distance,pd
import numpy as np
from multiprocessing import Pool
import time
from difflib import SequenceMatcher

def process_data_chunk(df_chunk, df2_complete, result_queue, idarcadia):
    try:
        for i, row1 in enumerate(df_chunk):
            for j, row2 in enumerate(df2_complete):
                #print(f"Iteration i{i}:j{j}")#, RowQualys {row1}")
                #print(f"Iteration {j}")#, Row2 {row2}")
                #print(f"Iteration i{i}, RowQualys chunked\n {row1}\n\n\n")
                #print(f"Iteration {j}, Row2\n {row2}\n\n\n")
                cve1 = row1.get('CVE ID', '')
                #cves1 = row1.get('cves', [])
                #cveid2 = row2.get('CVEID', '')
                cve2 = row2.get('cves', [])

               # Calcola la similarità tra i valori utilizzando SequenceMatcher
                similarity_cveid = SequenceMatcher(None, cve1, cve2).ratio()

                # Confronta gli insiemi di CVEs
                #common_cves = set(cve1) & set(cve2)
                #similarity_cves = len(common_cves) / max(len(cve1), len(cve2))



                
                # Calcola una misura complessiva di similarità basata sulle due chiavi
                overall_similarity = (similarity_cveid )#+ similarity_cves) / 2

                if overall_similarity>0.5:
                    print("\nsimilarity_cveid:",similarity_cveid)
                    #print("\nsimilarity_cves:",similarity_cves)
                    print("\nsimilarity overall:",overall_similarity)
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
    finally:
        print(f"Process {idarcadia} esce.")
    #print(f"Process {idarcadia} ha terminato.")
if __name__ == '__main__':
    try:
        num_processes = multiprocessing.cpu_count() 
        num_processes=1
        data_handler =data_handling.DataHandler()
        data_handler.load_data()

        print("Dividi i DataFrame in chunk", num_processes)    
        #chunk_size = len(data_handler.qualysdata) // num_processes  # Dividi in base al numero di processi desiderati
        #df_chunks = [data_handler.qualysdata[i:i + chunk_size] for i in range(0, len(data_handler.qualysdata), chunk_size)]
        #df2_complete= data_handler.nessusdata.copy()

        #df_chunk =data_handler.qualysdata# [data_handler.qualysdata[i:i + chunk_size].copy() for i in range(0, len(data_handler.qualysdata), chunk_size)]
        chunk_size = len(data_handler.qualysdata) // num_processes
        df_chunks = [data_handler.qualysdata[i:i + chunk_size].copy() for i in range(0, len(data_handler.qualysdata), chunk_size)]
        #df2_complete = data_handler.nessusdata.copy()

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
         # Imposta la condizione di uscita in modo che il processo principale esca in modo pulito
        should_exit = True
        
        time_end = time.time()
        times.append(float(time_end - time_init))

        print(f'Serial execution took {time_end - time_init}s.')
        print("**********FINE****************")
        final_result = pd.DataFrame(result_dfs)
        final_result.to_excel("./data/arcadia-light.xlsx", index=False)


    except Exception as e:
        print("Si è verificato un'errore:", str(e))