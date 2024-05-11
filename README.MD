
---

# PyWoods_Config

PyWoods_Config è una libreria Python per la gestione delle configurazioni delle applicazioni.

## Introduzione

Questa libreria fornisce un modo semplice ed efficiente per caricare e gestire le configurazioni  Supporta la definizione di configurazioni tramite file JSON e fornisce una struttura Pydantic per rappresentare e validare queste configurazioni.

## Installazione

E' necessario installare il codice sorgente disponibile su GitHub, puoi seguire questi passaggi:

Scarica il codice sorgente dal repository GitHub qui.

Estrai l'archivio scaricato nella posizione desiderata sul tuo computer.

Naviga nella directory estratta nel tuo terminale:

```bash
cd PERCORSO_ALLA_DIRECTORY_ESTRAZIONE
```

Installa la libreria usando il seguente comando:

```bash
python setup.py install
```

Dopo aver eseguito il comando di installazione, la libreria verrà installata nel tuo ambiente Python.

```bash
pip install PyWoods_Config
```

## Utilizzo

Ecco un esempio di come utilizzare la libreria:

```python
from PyWoods_Config import ConfigManager

# Carica le configurazioni
config = ConfigManager.load_configs()

# Accedi ad un'area di configurazione
area_x = config.area_x

# Stampare una proprietà relativa all'area di configurazione x
print("prop:", area_x.prop)
```

## Struttura del Progetto

La struttura del progetto è organizzata nel seguente modo:

- `PyWoods_Config/`: Directory principale della libreria.
  - `__init__.py`: File di inizializzazione del package.
  - `config_manager.py`: Modulo principale per la gestione delle configurazioni.
  - `json_configs/`: Directory contenente i file JSON di configurazione.
    - `camera.json`: Esempio di file JSON di configurazione per una fotocamera.
  - `models/`: Directory contenente i modelli Pydantic.
    - `__init__.py`: File di inizializzazione del package.
    - `camera_model.py`: Modulo contenente la definizione del modello per la configurazione della fotocamera.
- `tests/`: Directory contenente i file di test per la libreria.
  - `__init__.py`: File di inizializzazione del package.
  - `test_config_manager.py`: File di test per il modulo `config_manager.py`.
  - `test_camera_model.py`: File di test per il modulo `camera_model.py`.
- `pyproject.toml`: File di configurazione per il progetto Python.
- `README.md`: Questo file, contenente informazioni dettagliate sulla libreria e le istruzioni per l'utilizzo.
- `setup.cfg`: File di configurazione per il pacchetto Python.

## Contribuire

Le pull request sono le benvenute! Per le modifiche importanti, aprire prima un ticket per discutere delle modifiche proposte.

---

Questo README fornisce una panoramica completa della libreria PyWoods_Config, spiegando come installarla, utilizzarla e contribuire ad essa. Può essere ulteriormente personalizzato per adattarsi alle esigenze specifiche del progetto.
