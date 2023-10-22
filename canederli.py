from main_module import *
global header1
HEADER1= """
    _                      _ _
   / \   _ __ ___ __ _  __| (_) __ _
  / _ \ | '__/ __/ _` |/ _` | |/ _` |
 / ___ \| | | (_| (_| | (_| | | (_| |
/_/   \_\_|  \___\__,_|\__,_|_|\__,_|   v 1.0.0

                    project_canederli_cotti
                                    """


PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'

global header2
header2 = """
    \                       |_)
   _ \    __| __|  _` |  _` | |  _` |
  ___ \  |   (    (   | (   | | (   |
_/    _\_|  \___|\__,_|\__,_|_|\__,_|
                                      """

global header3
header3= """
      _/_/                                        _/  _/
   _/    _/  _/  _/_/    _/_/_/    _/_/_/    _/_/_/        _/_/_/
  _/_/_/_/  _/_/      _/        _/    _/  _/    _/  _/  _/    _/
 _/    _/  _/        _/        _/    _/  _/    _/  _/  _/    _/
_/    _/  _/          _/_/_/    _/_/_/    _/_/_/  _/    _/_/_/

                                      """
global header4
header4="""
                            _ _
    /\                     | (_)
   /  \   _ __ ___ __ _  __| |_  __ _
  / /\ \ | '__/ __/ _` |/ _` | |/ _` |
 / ____ \| | | (_| (_| | (_| | | (_| |
/_/    \_\_|  \___\__,_|\__,_|_|\__,_|

                                      """
global header5
header5="""
    ___                        ___
   /   |  ______________ _____/ (_)___ _
  / /| | / ___/ ___/ __ `/ __  / / __ `/
 / ___ |/ /  / /__/ /_/ / /_/ / / /_/ /
/_/  |_/_/   \___/\__,_/\__,_/_/\__,_/

                                      """



def header1():
    return header1
def header2():
    return header2
def header3():
    return header3
def header4():
    return header4
def header5():
    return header5


def stampa_loading():
    stampa_matrice_con_refresh(20)

def clear_console():
    #print("\r")
    os.system('cls' if os.name == 'nt' else 'clear')

def stampa_matrice_con_refresh(numero_di_cicli):
    for _ in range(numero_di_cicli):
        clear_console()
        print(PURPLE)
        print(HEADER1)
        print(BLUE)
        matrice=crea_matrice_casuale()
        for riga in matrice:
            for carattere in riga:
                print(carattere, end=' ')
            print()
            #time.sleep(0.2)  # Attendi per un breve istante prima di passare alla successiva iterazione

    print(END)

caratteri_possibili = ['-', '_', '/','\\', '|',']','[']

def crea_matrice_casuale():
    matrice = []
    for _ in range(2):
        riga = [random.choice(caratteri_possibili) for _ in range(20)]
        matrice.append(riga)
    return matrice

# Funzione per stampare la matrice
def stampa_matrice(matrice):
    for riga in matrice:
        for carattere in riga:
            print(carattere, end=' ')
        print()

# Esempio di utilizzo
matrice = crea_matrice_casuale()
stampa_matrice(matrice)
