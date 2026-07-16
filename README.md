# Hand Tracking → TouchDesigner | Blob Sonoro e Visivo Interattivo

Progetto di interazione gestuale in tempo reale: il tracciamento delle mani (MediaPipe, via Python) pilota via OSC un sistema audiovisivo generativo in TouchDesigner — un "blob" di plasma che nasce dal gesto pollice-indice di entrambe le mani, con un sistema sonoro reattivo e un campo di particelle di sfondo con cui il blob interagisce.

## Concept

Il gesto delle mani non è un semplice controller: rappresenta un organismo fluido che l'utente "abita" e nutre. Aprendo/chiudendo le mani si modula energia condivisa tra audio (drone, pluck, pitch, pan, riverbero) e video (dimensione e colore del blob, interazione col campo di particelle di sfondo).

## Struttura del repository

```
.
├── python/
│   ├── hands_osc.py       # Script MediaPipe: tracking mani → invio dati via OSC
│   └── requirements.txt   # Dipendenze Python
├── touchdesigner/
│   └── project1.toe       # Progetto TouchDesigner completo
├── docs/
│   ├── screenshots/                    # Screenshot del progetto in funzione
│   └── hand_tracking_diagram.drawio    # Diagramma architetturale (apri su app.diagrams.net)
└── README.md
```

## Come funziona

1. **`hands_osc.py`** cattura il video dalla webcam, esegue il tracciamento delle mani con MediaPipe Hands, identifica correttamente sinistra/destra tramite `multi_handedness`, ed invia le coordinate normalizzate (x, y, z) di ogni landmark via OSC (indirizzi tipo `/hand/left/8/x`, `/hand/right/4/y`, ecc.) a TouchDesigner.
2. **TouchDesigner** riceve i dati via OSC In CHOP, li elabora (Script CHOP per calcolare centro e apertura pollice-indice per ciascuna mano), e li usa per pilotare:
   - un GLSL TOP che genera due "blob" di plasma organici (uno per mano) che si fondono quando le mani si avvicinano
   - una catena audio (drone continuo + trigger percussivi su apertura/chiusura della mano sinistra, pitch/pan/riverbero pilotati dalla mano destra)
   - un sistema particellare GPU di sfondo, con cui il blob interagisce tramite un effector basato sull'immagine del blob stesso

## Architettura

Il diagramma completo del flusso dati (Webcam → Python/MediaPipe → OSC → TouchDesigner → rami audio e video) è disponibile in [`docs/hand_tracking_diagram.drawio`](docs/hand_tracking_diagram.drawio) — apribile e modificabile su [app.diagrams.net](https://app.diagrams.net) (Open Existing Diagram), oppure visualizzabile direttamente su GitHub cliccando sul file.

## Setup

### Requisiti
- Python 3.9+
- [TouchDesigner](https://derivative.ca/) (build non commerciale o superiore)
- Webcam

### Installazione parte Python

```bash
cd python
pip install -r requirements.txt
python hands_osc.py
```

Lo script apre la finestra della webcam con overlay del tracciamento e inizia a inviare dati OSC su `127.0.0.1:5005`.

### Apertura progetto TouchDesigner

1. Apri `touchdesigner/project1.toe`.
2. Verifica che l'OSC In CHOP sia in ascolto sulla stessa porta (`5005`) usata dallo script Python.
3. Avvia `hands_osc.py` **prima** o in parallelo a TouchDesigner.
4. Premi Play/Cook nel timeline di TD.

## Controlli / Mapping

- **Mano sinistra chiusa**: drone a frequenza grave
- **Mano sinistra aperta**: ampiezza su due sinusoidi (165 Hz e 1100 Hz)
- **Apertura mano destra**: trasla il pitch delle sinusoidi
- **Posizione X mano destra**: pan stereo
- **Posizione Y mano destra**: quantità di riverbero
- **Distanza pollice-indice (entrambe le mani)**: dimensione del blob
- **Distanza tra le due mani**: fusione organica dei due blob

## Note

Progetto realizzato nell'ambito di un percorso didattico/artistico su interazione gestuale, audio generativo e visual coding.

## Licenza

MIT — vedi [LICENSE](LICENSE)
