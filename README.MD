## PyWoodsUtils: Gestione File, Configurazioni e Utilità per VisionPiWoods (Versione Alpha)

**PyWoodsUtils** è una suite di librerie Python progettata per semplificare e ottimizzare lo sviluppo di applicazioni, fornendo funzionalità robuste per la gestione di file, configurazioni e attività comuni. Nasce con l'obiettivo di supportare lo sviluppo del progetto **VisionPiWoods**, un sistema completo per la gestione di una fotocamera Raspberry Pi utilizzando la libreria Picamera2.

### Introduzione

PyWoodsUtils nasce dall'esigenza di semplificare e standardizzare la gestione di file, configurazioni e altre attività comuni all'interno di progetti Python, offrendo un'interfaccia intuitiva e robusta per creare, leggere, aggiornare e organizzare file e cartelle, nonché per caricare e gestire configurazioni in modo efficiente.

**VisionPiWoods**, il progetto a cui PyWoodsUtils è principalmente dedicato, è un sistema in fase di sviluppo che offre diverse funzionalità per la gestione di una fotocamera Raspberry Pi:

* **Streaming video:** Trasmissione video in tempo reale tramite l'interfaccia web FastAPI.
* **Registrazione video in base al movimento:** Avvio automatico della registrazione video in presenza di movimento rilevato dalla fotocamera.
* **Cattura di screenshot:** Acquisizione di screenshot on-demand o automatizzata.

PyWoodsUtils fornisce moduli utili per la gestione di file, configurazioni e altre attività comuni all'interno del progetto VisionPiWoods, semplificando lo sviluppo e l'utilizzo del sistema.

### Moduli Inclusi

* **PyWoods_Files:**
    - Gestisce file e cartelle in modo robusto e flessibile.
    - Crea, elimina, rinomina e sposta file e cartelle con facilità.
    - Recupera elenchi di file filtrati in base a criteri specifici (estensione, ricerca ricorsiva, inclusione nomi directory).
    - Mantiene la struttura delle directory e gestisce percorsi relativi e assoluti.
    - Fornisce funzionalità avanzate per la creazione di cartelle, verifica dei permessi, recupero di elenchi di file con filtri avanzati e gestione dei percorsi relativi e assoluti.

* **PyWoods_Config:**
    - Gestisce le configurazioni per le tue applicazioni in modo semplice ed efficiente.
    - Carica e valida le configurazioni da file JSON utilizzando modelli Pydantic.
    - Offre un'interfaccia intuitiva per accedere e modificare le impostazioni di configurazione.

### Installazione

```bash
pip install pywoodsutils
```

Una volta installato, puoi importare e utilizzare i moduli `PyWoods_Files` e `PyWoods_Config` nei tuoi progetti Python.

### Documentazione

Ogni modulo PyWoodsUtils include una documentazione completa che descrive le sue funzionalità, l'utilizzo e gli esempi. Puoi accedere alla documentazione direttamente dai commenti all'interno del codice sorgente o utilizzando strumenti di documentazione come Sphinx.

### Contribuire

PyWoodsUtils è un progetto open-source e le tue contribuzioni sono le benvenute! Se hai idee per migliorare i moduli esistenti o desideri aggiungere nuove funzionalità, apri un ticket su GitHub o invia una pull request con le tue modifiche.

### Licenza

PyWoodsUtils è distribuito sotto la licenza MIT. Vedere il file [LICENSE](LICENSE) per ulteriori informazioni.

### Esempio di Utilizzo (PyWoods_Files)

```python
from pywoodsutils.files import FileManager

# Crea un'istanza del gestore file
file_manager = FileManager("/path/to/your/root/directory")

# Recupera un elenco di file con estensione ".jpg"
image_files = file_manager.get_files_by_extension("/images", extension=".jpg")

# Recupera un elenco di file ricorsivamente (incluse sottodirectory)
all_files_recursive = file_manager.get_files_recursively("/documents", recursive=True)

# Recupera percorsi file con nomi directory
file_paths = file_manager.get_file_paths_with_dir("/documents", include_dir=True)
```

### Esempio di Utilizzo (PyWoods_Config)

```python
from pywoodsutils.config import ConfigManager

# Carica le configurazioni dal file "config.json"
config = ConfigManager.load_configs("config.json")

# Accedi alla configurazione desiderata
desired_config = config.DesiredConfig

# Stampa un valore specifico dalla configurazione
print("Valore di 'my_key':", desired_config.my_key)
```

### Struttura del Progetto

La struttura del progetto è
## Struttura del Progetto

PyWoodsUtils è suddiviso in due moduli principali:

**1. PyWoods_Files:**

- Fornisce funzionalità robuste per la gestione di file e cartelle.
- Include funzioni per:
    - Creare, eliminare, rinominare e spostare file e cartelle.
    - Recuperare elenchi di file filtrati per estensione, ricerca ricorsiva e inclusione nomi directory.
    - Mantenere la struttura delle directory e gestire percorsi relativi e assoluti.
    - Offrire funzionalità avanzate per la creazione di cartelle, verifica dei permessi, recupero di elenchi di file con filtri avanzati e gestione dei percorsi relativi e assoluti.

**2. PyWoods_Config:**

- Gestisce le configurazioni per le applicazioni in modo semplice ed efficiente.
- Offre funzionalità per:
    - Caricare e validare le configurazioni da file JSON utilizzando modelli Pydantic.
    - Fornire un'interfaccia intuitiva per accedere e modificare le impostazioni di configurazione.

**Struttura del repository:**

```
pywoodsutils
├── LICENSE
├── README.md
├── pywoods_config
│   ├── __init__.py
│   ├── config.py
│   └── config_manager.py
├── pywoods_files
│   ├── __init__.py
│   ├── file_manager.py
│   └── files.py
├── tests
│   ├── test_config.py
│   └── test_files.py
└── tox.ini
```

**Ogni modulo include una documentazione completa che descrive le sue funzionalità, l'utilizzo e gli esempi.**

**Scarica il pacchetto:**

- **Repository Git:** [https://github.com/PythonWoods/PyWoodsUtils.git](https://github.com/PythonWoods/PyWoodsUtils.git)
