 # About QID-NessusID-OtherID
 
<p>
 <img align="right" width="350" src="/assets/programmer.gif" alt="Coding gif" />
  
 ✌️ &emsp; Enjoy the research and sharing knowledge <br/><br/>
 ❤️ &emsp; Love to writing code and learning new features<br/><br/>
 📧 &emsp; Reach me anytime: Zenit90+git@gmail.com<br/><br/>
 💬 &emsp; Ask me about anything [here](https://github.com/ZeMatt90/ZeMatt90/issues)

</p>

<br/>
<br/>
<br/>

## Used To Code
![VSCode](https://img.shields.io/badge/Visual_Studio-0078d7?style=for-the-badge&logo=visual%20studio&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Python]([https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white](https://img.shields.io/pypi/pyversions/3
)).
<br/>

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





# QID-NessusID-OtherID Project

Questo è un progetto Python suddiviso in moduli distinti per una maggiore organizzazione e manutenibilità.

## Moduli del Progetto

### `plugin/nessus/update.py`

Questo modulo aggiorna i dati relativi a Nessus

### `create_all_cve-light.py`

Questo modulo crea una lista di cve le quali sono presenti sia dai dati di Nessus che da Qualys

### `createdictionary.py`

Questo modulo crea un semplice dizionario di indici dove è possibile reperire in base alla cve l'id del plugin del rivenditore (Nessus o Qualys).

### `user_interface.py`

Questo modulo utilizza Streamlit per creare un'interfaccia utente interattiva per il progetto. Le funzioni in questo modulo sono responsabili della visualizzazione dei dati, delle interazioni con l'utente e della presentazione dei risultati.

## Come Eseguire il Progetto

1. Installa le dipendenze necessarie eseguendo `pip install -r requirements.txt`.

Se pip install -r requirements.txt non è bastato una volta sistemato è possibile aggiornare i requirements
	1.1 Aggiorna le dipendeze necessarie nel file requirements.txt eseguendo 'pip freeze > requirements.txt'

2. Esegui BE copiare il workflow di github
3. Esegui FE `streamlit run user_interface.py`
