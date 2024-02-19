import pandas as pd
import csv
from tqdm import tqdm
import multiprocessing 
import data_handling
import pandas as pd
from multiprocessing import Pool
import time
from difflib import SequenceMatcher


### prova multiprocessingg

def process_data_chunk(df_chunk, df2_complete, nuove_righe, idarcadia):
    try:
        with tqdm(total=len(df_cve['CVE']), desc="Processing CVE", bar_format="{l_bar}{bar:10}{r_bar}{remaining}") as bar:
            for cve_value in df_cve['CVE']:
                
                qualys_values = df_qualys[df_qualys['CVE ID'].str.split(',').apply(lambda x: cve_value in x)]['QID'].tolist()
                nessus_values = df_nessus[df_nessus['cves'].str.split(',').apply(lambda x: cve_value in x)]['doc_id'].tolist()
                #if nessus_values != [] and qualys_values !=[]:
                nuove_righe.append({'CVE': cve_value, 'QID': qualys_values, 'doc_id': nessus_values,'info': ""})
                #print("\n qualys\n",qualys_values,df_qualys['CVE ID'].str.split(',').apply(lambda x: cve_value in x))
                #print("\n nessus\n",nessus_values)
                bar.update(1)
        result_queue.put(nuove_righe)
    except Exception as e:
        print(f"Process {idarcadia} ha generato un errore: {str(e)}")


df_values = pd.DataFrame(nuove_righe)
df_values.to_csv(dictionary_csv, index=False)
#df_values.to_csv(dictionary_csv, index=False, quoting=csv.QUOTE_NONE, escapechar=' ')  #servirebbe per rimuovere le aggiunte di ""

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
         # Imposta la condizione di uscita in modo che il processo principale esca in modo pulito
        should_exit = True


        time_end = time.time()
        times.append(float(time_end - time_init))

        print("istanziati i dati e caricati in memoria al modico prezzo di %s byte",sys.getsizeof(df_chunks))
        total_memory_usage = 0
        for df in [data_handler.nessusdata, data_handler.qualysdata, data_handler.arcadiadata]:
          total_memory_usage += df.memory_usage(deep=True).sum()  # Calcola la dimensione effettiva dei DataFrame
        print(f"Dimensione totale: {total_memory_usage} byte")

        print(f'Serial execution took {time_end - time_init}s.')
        print("**********FINE****************")
        final_result = pd.DataFrame(result_dfs)
        final_result.to_excel("./data/arcadia-light.xlsx", index=False)


    except Exception as e:
        print("Si è verificato un'errore:", str(e))