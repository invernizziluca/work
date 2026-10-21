# Portfolio generale · Luca Invernizzi

Sito portfolio per recruiter di qualsiasi settore (Germania, Svizzera, Polonia), separato dal sito musicale `invernizziluca.github.io`.
Indirizzo previsto: **https://invernizziluca.github.io/profile/** (repository `profile`).
Lingue: **DE** (anche come pagina iniziale `/`), **EN** (`/en/`), **IT** (`/it/`).

Il sito è organizzato in tre aree, le stesse in tutte le lingue:

| Area (id) | DE | EN | IT | Copre |
|---|---|---|---|---|
| `content` | Content | Content | Contenuti | comunicazione, PR, social media, web |
| `kontakte` | Kontakte | Contacts | Contatti | business development, vendite, partnership |
| `koordination` | Koordination | Coordination | Coordinamento | project management, eventi, operations |

Ogni affermazione nella sezione «Schwerpunkte» ha la sua fonte: Zeugnis, screenshot, post LinkedIn, attestato, articolo, ricerca o «Eigene Angabe» (dichiarazione propria).

## Link su misura per le candidature

Lo stesso sito si apre già sull'area giusta:

| Candidatura per | Link |
|---|---|
| Social media, PR, comunicazione, marketing | `…/profile/de/?fokus=content` |
| Business development, sales, partnership | `…/profile/de/?fokus=kontakte` |
| Project management, eventi, operations | `…/profile/de/?fokus=koordination` |

Funziona in tutte le lingue (`/en/?fokus=kontakte`, `/it/?fokus=koordination`). Le esperienze che c'entrano vengono evidenziate.

## Anteprima sul computer

```bash
pip install -r requirements.txt      # una volta (Python 3.9 o più recente)
python3 build.py --preview           # crea la cartella dist/
python3 -m http.server -d dist 8000  # poi apri http://localhost:8000
```

Senza `--preview` si ottiene esattamente la build che fa GitHub.

---

## COME AGGIORNARE IL SITO CON AI

### Regole da dare all'AI (copia e incolla)

```
Sei lo sviluppatore del mio portfolio generale (generatore Python: build.py + Jinja2).
Leggi README.md, sezione "COME AGGIORNARE IL SITO CON AI".
Modifica SOLO i file in content/ (o creane uno nuovo partendo da vorlagen/). Non toccare build.py e templates/ se non serve.
Regole:
- Ogni testo esiste in tre lingue: de / en / it (il tedesco è obbligatorio).
- Testi e date tra "virgolette doppie". Periodi "2025-08", date "2026-06-30". Indentazione YAML: 2 spazi.
- Immagini in static/images/…, nei file si scrivono "/images/…". PDF in static/pdf/…, si scrivono "/pdf/…".
- Niente invenzioni: solo fatti che posso dimostrare. Indica sempre la fonte (source: zeugnis, screenshot, linkedin, zertifikat, artikel, forschung, eigen).
- Restituiscimi il file completo, pronto da copiare.
Compito: <scrivi qui cosa vuoi cambiare>
```

### Dove si trova cosa

| Cosa vuoi cambiare | File |
|---|---|
| Testi della pagina iniziale, aree, prove, ruoli adatti, lingue, strumenti, interessi, contatto | `content/home.yaml` |
| Un'esperienza (testi, foto, documenti, link) | `content/erfahrung/<nome>.yaml` |
| Formazione (FFHS, Kantonsschule, SAMB) | `content/ausbildung/<nome>.yaml` |
| Zeugnisse, attestati, ricerche, articoli | `content/nachweise/<nome>.yaml` |
| Citazioni (Zeugnisse, raccomandazioni) | `content/referenzen/<nome>.yaml` |
| Post LinkedIn | `content/linkedin/<nome>.yaml` |
| Etichette di menu e bottoni | `content/ui.yaml` |
| Indirizzo del sito, lingue, nomi delle cartelle per lingua | `site.yaml` |
| Colori, caratteri, spaziature | `static/css/site.css` |
| Immagini e PDF | `static/images/…`, `static/pdf/…` |
| Modelli per nuovi contenuti | `vorlagen/` |

### Esempi pronti

**Nuova esperienza.** Copia `vorlagen/erfahrung.yaml` in `content/erfahrung/<nome>.yaml` (minuscole e trattini: `label-xyz.yaml` diventa `/de/erfahrung/label-xyz/`). Foto in `static/images/works/<nome>/`. Con `order` decidi la posizione; finché l'esperienza è in corso lascia fuori `end:` e compare «Aktuell». In `areas:` scrivi a quali aree appartiene.

**Nuova prova in un'area.** In `content/home.yaml`, sotto l'area giusta (`focus → areas → evidence`), aggiungi una riga con `text`, `work` (nome del file dell'esperienza) e `source`. Se la fonte si può aprire (PDF, immagine, post), aggiungi `href`.

**Fine dello stage alla Initiative Musik.** In `content/erfahrung/initiative-musik.yaml` aggiungi `end: "2027-02"`, compila `outputs:` e, quando arriva lo Zeugnis, aggiungi il PDF oscurato e il nome in `documents:`.

**CV scaricabile.** Metti il PDF in `static/pdf/` e scrivi il percorso in `content/home.yaml → contact → cv` (per esempio `"/pdf/lebenslauf-luca-invernizzi.pdf"`). Compare da solo il bottone «Lebenslauf (PDF)».

**Nuovo Zeugnis o attestato.** Prima oscura data di nascita e indirizzo. Poi PDF in `static/pdf/`, copia `vorlagen/nachweis.yaml` in `content/nachweise/<nome>.yaml`.

### Se la build segnala un errore
Il messaggio indica file e campo, per esempio `content/erfahrung/label-xyz.yaml → start: use the format "YYYY-MM"`. Correggi quel campo e ripeti. Errori tipici: virgolette mancanti, indentazione sbagliata, nome di un documento scritto male in `documents:` o `posts:`.

---

## Struttura del progetto

```
build.py                 genera il sito in dist/ (controlla anche i contenuti)
site.yaml                indirizzo, lingue, aree
content/                 TUTTI i testi (modificabili con AI)
  home.yaml                pagina iniziale e aree con le prove
  ui.yaml                  etichette dell'interfaccia
  erfahrung/*.yaml         esperienze (1 file = 1 pagina per lingua)
  ausbildung/*.yaml        formazione
  nachweise/*.yaml         Zeugnisse, attestati, ricerche, articoli
  referenzen/*.yaml        citazioni
  linkedin/*.yaml          post LinkedIn
templates/               HTML (Jinja2): base, home, station (esperienza), 404
static/                  css, js, caratteri, immagini, PDF, icone (copiati così come sono)
scripts/fonts/           caratteri per le immagini di anteprima (LinkedIn, WhatsApp)
vorlagen/                modelli per nuovi contenuti
.github/workflows/deploy.yml   pubblicazione automatica su GitHub Pages
```

## Note tecniche

- **Link relativi**: tutte le pagine si collegano tra loro con percorsi relativi, quindi il sito funziona sotto `/profile/`, con un dominio proprio o aperto in locale.
- **Immagini**: a ogni build vengono create versioni da 480, 960 e 1600 px in WebP (`dist/generated/img/`). Le immagini originali restano in `static/images/`.
- **Anteprime per i link**: per la home (una per lingua) e per ogni esperienza la build crea un'immagine 1200 × 630 (`dist/generated/og/`).
- **SEO**: title e description per pagina, canonical, hreflang DE/EN/IT, dati strutturati (Person), `sitemap.xml`, `robots.txt`.
- **Tema scuro**: il sito segue l'impostazione del dispositivo (chiaro o scuro).
- **Accessibilità**: link «Zum Inhalt springen», focus visibile, testo alternativo per ogni immagine, tab navigabili con le frecce, contrasti AA verificati. Senza JavaScript tutte e tre le aree restano visibili una sotto l'altra.
- **Privacy**: nei PDF degli Zeugnisse e nella ricerca qualitativa data di nascita, indirizzo e telefono sono oscurati (la pagina con i dati è stata ricreata come immagine, quindi il testo coperto non esiste più).
- **Caratteri**: TeX Gyre Adventor (gemello libero dell'ITC Avant Garde del CV), licenza GUST in `static/fonts/GUST-FONT-LICENSE.txt`. Nessuna richiesta a Google Fonts.
- **Nessun cookie, nessun tracciamento.**

## Pubblicazione su GitHub Pages

1. Su GitHub crea un repository nuovo e vuoto chiamato **`profile`** (pubblico).
2. Carica il contenuto di questa cartella (GitHub Desktop, oppure «Add file → Upload files»).
3. In **Settings → Pages → Build and deployment → Source** scegli **GitHub Actions**.
4. A ogni push su `main` il workflow installa Python, esegue `build.py` e pubblica `dist/`. Se qualcosa non va, la scheda **Actions** mostra l'errore e online resta la versione precedente.

Dominio proprio (facoltativo): crea `static/CNAME` con il dominio (per esempio `tuodominio.ch`) e configuralo anche in Settings → Pages.
