import os
import subprocess

def check_graphviz_installed():
    try:
        result = subprocess.run(['dot', '-V'], capture_output=True, text=True)
        if result.returncode != 0:
            raise FileNotFoundError
    except FileNotFoundError:
        raise RuntimeError("Graphviz non è installato. Installalo e assicurati che 'dot' sia nel PATH.")

def generate_directory_structure(path):
    try:
        result = subprocess.run(['tree', path], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("Errore durante l'esecuzione di 'tree'. Assicurati che 'tree' sia installato.")
        
        # Salva la struttura directory in un file dentro la cartella Doc/
        with open(os.path.join("Doc", "directory_structure.txt"), "w") as f:
            f.write(result.stdout)
        
        print("Struttura directory salvata con successo!")
    except Exception as e:
        print(f"Errore: {e}\nForse devi installare 'tree'? In tal caso usa 'yum install tree' o 'apt-get install tree'.")

def generate_uml_diagrams(path, project_name):
    try:
        result = subprocess.run(['pyreverse', '-o', 'dot', '-p', project_name, path], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        
        dot_files = [f for f in os.listdir() if f.endswith('.dot')]
        if not dot_files:
            raise FileNotFoundError("Nessun file .dot generato da pyreverse. Controlla per errori.")

        # Crea la cartella Doc/ se non esiste
        if not os.path.exists("Doc"):
            os.makedirs("Doc")

        # Sposta i file .dot generati nella cartella Doc/
        for dot_file in dot_files:
            dot_file_path = os.path.join(".", dot_file)
            dest_file_path = os.path.join("Doc", dot_file)
            os.rename(dot_file_path, dest_file_path)

            # Genera i diagrammi .png da ciascun file .dot e salvali nella cartella Doc/
            png_file = dest_file_path.replace('.dot', '.png')
            subprocess.run(['dot', '-Tpng', dest_file_path, '-o', png_file])
        
        print("Diagrammi UML generati con successo!")
    except Exception as e:
        print(f"Errore: {e}\nForse devi installare 'pyreverse'? In tal caso usa 'pip install pylint'.")

if __name__ == "__main__":
    # Eseguire il codice principale qui
    projectBE_path = "BE"
    projectFE_path = "FE"
    projectBE_name = "ArcadiaBE"
    projectFE_name = "ArcadiaFE"
    
    # Controlla se Graphviz è installato
    check_graphviz_installed()

    # Genera la struttura delle directory
    generate_directory_structure(projectBE_path)
    generate_directory_structure(projectFE_path)

    # Genera i diagrammi UML
    generate_uml_diagrams(projectBE_path, projectBE_name)
    generate_uml_diagrams(projectFE_path, projectFE_name)
