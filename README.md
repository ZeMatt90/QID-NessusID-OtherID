 # About me
 
<p>
 <img align="right" width="350" src="/assets/programmer.gif" alt="Coding gif" />
  
 ✌️ &emsp; Enjoy to do programming and sharing knowledge <br/><br/>
 ❤️ &emsp; Love to writing code and learning new features<br/><br/>
 📧 &emsp; Reach me anytime: ZeMatt90.dev@gmail.com<br/><br/>
 💬 &emsp; Ask me about anything [here](https://github.com/ZeMatt90/ZeMatt90/issues)

</p>

<br/>
<br/>
<br/>

## Used To Code
![VSCode](https://img.shields.io/badge/Visual_Studio-0078d7?style=for-the-badge&logo=visual%20studio&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

<br/>
<!-- About public 
## Top Open Source -
[![Web Projects](https://github-readme-stats.vercel.app/api/pin/?username=ZeMatt90&repo=web-projects&border_color=7F3FBF&bg_color=0D1117&title_color=C9D1D9&text_color=8B949E&icon_color=7F3FBF)](https://github.com/ZeMatt90/web-projects)
[![Al Folio](https://github-readme-stats.vercel.app/api/pin/?username=ZeMatt90&repo=al-folio&border_color=7F3FBF&bg_color=0D1117&title_color=C9D1D9&text_color=8B949E&icon_color=7F3FBF)](https://github.com/ZeMatt90/al-folio)
[![Al Siam Readme](https://github-readme-stats.vercel.app/api/pin/?username=ZeMatt90&repo=ZeMatt90&border_color=7F3FBF&bg_color=0D1117&title_color=C9D1D9&text_color=8B949E&icon_color=7F3FBF)](https://github.com/ZeMatt90/ZeMatt90)
[![Al Siam Teminal](https://github-readme-stats.vercel.app/api/pin/?username=ZeMatt90&repo=ZeMatt90.github.io&border_color=7F3FBF&bg_color=0D1117&title_color=C9D1D9&text_color=8B949E&icon_color=7F3FBF)](https://github.com/ZeMatt90/ZeMatt90.github.io)
-->
<p align="left">
  <a href="https://github.com/ZeMatt90?tab=repositories" target="_blank"><img alt="All Repositories" title="All Repositories" src="https://img.shields.io/badge/-All%20Repos-2962FF?style=for-the-badge&logo=koding&logoColor=white"/></a>
</p>

<br/>
<hr/>
<br/>


<p align="center">
  <a href="https://github.com/ZeMatt90">
    <img src="https://github-readme-streak-stats.herokuapp.com/?user=ZeMatt90&theme=radical&border=7F3FBF&background=0D1117" alt="Saif's GitHub streak"/>
  </a>
</p>
<p align="center">
  <a href="https://github.com/ZeMatt90">
    <img src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=ZeMatt90&theme=radical" alt="ZeMatt90's GitHub Contribution"/>
  </a>
</p>

<a> 
    <a href="https://github.com/ZeMatt90"><img alt="Al Siam's Github Stats" src="https://denvercoder1-github-readme-stats.vercel.app/api?username=ZeMatt90&show_icons=true&count_private=true&theme=react&border_color=7F3FBF&bg_color=0D1117&title_color=F85D7F&icon_color=F8D866" height="192px" width="49.5%"/></a>
  <a href="https://github.com/ZeMatt90"><img alt="ZeMatt90's Top Languages" src="https://denvercoder1-github-readme-stats.vercel.app/api/top-langs/?username=ZeMatt90&langs_count=8&layout=compact&theme=react&border_color=7F3FBF&bg_color=0D1117&title_color=F85D7F&icon_color=F8D866" height="192px" width="49.5%"/></a>
  <br/>
</a>

!['s Graph](https://github-readme-activity-graph.vercel.app/graph?username=ZeMatt90&custom_title=Zematt90's%20GitHub%20Activity%20Graph&bg_color=0D1117&color=7F3FBF&line=7F3FBF&point=7F3FBF&area_color=FFFFFF&title_color=FFFFFF&area=true)





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

Se pip install -r requirements.txt non è bastato una volta sistemato è possibile aggiornare i requirements
	1.1 Aggiorna le dipendeze necessarie nel file requirements.txt eseguendo 'pip freeze > requirements.txt'

2. Esegui BE `python3 main.py` per avviare il progetto.
3. Esegui FE 
