# Arcadia Project

Questo è un progetto Python suddiviso in moduli distinti per una maggiore organizzazione e manutenibilità.

## Moduli del Progetto

### `data_handling.py`
In a very broad aspect, a data science project follows four steps:

    Get the data;
    Process the data;
    Do something with the data;
    Store other data

Questo modulo gestisce la manipolazione dei dati e il dataframe del progetto. Include funzioni per leggere dati da un file, elaborare dati e creare/aggiornare il dataframe.

### `user_interface.py`

Questo modulo utilizza Streamlit per creare un'interfaccia utente interattiva per il progetto. Le funzioni in questo modulo sono responsabili della visualizzazione dei dati, delle interazioni con l'utente e della presentazione dei risultati.

### `calculations.py`

Questo modulo contiene la logica per i calcoli specifici del progetto. Include funzioni che eseguono calcoli e aggiornano ciò che serve per l'interfaccia.

### `.github/workflows/scheduled_data_handling.yml`

Questo file di configurazione definisce un flusso di lavoro GitHub Actions per l'esecuzione di calcoli pianificati. È possibile specificare l'orario o l'azione che attiverà il flusso di lavoro. All'interno di questo flusso di lavoro, i calcoli definiti in `data_handling.py` vengono eseguiti automaticamente.

### `main.py`

Questo è il modulo principale del progetto. Può essere utilizzato come punto di ingresso principale. All'interno di questo modulo, i moduli `data_handling`, `user_interface` e `calculations` vengono importati e il flusso del programma viene coordinato. Il codice principale può essere eseguito all'interno di una costruzione `if __name__ == "__main__":`.

## Come Eseguire il Progetto

1. Installa le dipendenze necessarie eseguendo `pip install -r requirements.txt`.
# altrimenti le seguenti dipendenze puntuali
# pip install scikit-learn
# pip install Levenshtein
# pip install Pandas
# pip install streamlit

Se pip install -r requirements.txt non è bastato una volta sistemato è possibile aggiornare i requirements
	1.1 Aggiorna le dipendeze necessarie nel file requirements.txt eseguendo 'pip freeze > requirements.txt'

2. Esegui `python3 main.py` per avviare il progetto.
