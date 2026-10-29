# Portfolio business · Luca Invernizzi

Sito per recruiter fuori dalla musica (tech, marketing, vendite, consulting, business development): **https://invernizziluca.github.io/work/**
(per la music industry c'è il sito musicale, senza `/work/`: `https://invernizziluca.github.io/`).

Lingue: **EN** (anche come pagina iniziale `/work/`), **DE** (`/work/de/`), **IT** (`/work/it/`). Il tedesco usa il "Sie".
Tecnologia: generatore **Python + Jinja2 + YAML** (`build.py`), nessun framework JavaScript. Design condiviso con il sito musicale: vedi [`DESIGN_SYSTEM.md`](DESIGN_SYSTEM.md). Novità: [`CHANGELOG.md`](CHANGELOG.md).

```bash
pip install -r requirements.txt      # una volta (Python 3.9 o più recente)
python3 build.py                     # crea dist/ esattamente come GitHub
python3 -m http.server -d dist 8000  # anteprima su http://localhost:8000
python3 build.py --preview           # variante con link a index.html, da aprire anche con doppio clic
```

La build controlla i contenuti: se manca un campo o un file, si ferma e scrive file e campo da correggere.

---

## Pubblicare su GitHub Pages

Nulla viene pubblicato finché non carichi i file sul repository **`work`** (branch `main`). Da lì parte da solo `.github/workflows/deploy.yml`: installa Python, esegue `build.py` con l'indirizzo giusto e pubblica `dist/`.

**Prima volta:**
1. Su GitHub il repository deve chiamarsi **`work`** (così l'indirizzo è `…github.io/work/`) ed essere pubblico.
2. **Settings → Pages → Build and deployment → Source: GitHub Actions**.

**Ogni aggiornamento:**
1. Prova in locale: `python3 build.py` deve finire con "Built 20 pages…" (o più) senza errori.
2. Con **GitHub Desktop** (consigliato): nella cartella del repository cancella tutto tranne la cartella nascosta `.git`, copia dentro il contenuto di questa cartella (senza `dist/` e `.cache/`), poi *Commit to main* → *Push origin*.
3. Dal **sito di GitHub** ("Add file → Upload files") i file con lo stesso nome vengono sostituiti, ma quelli eliminati o rinominati restano: cancellali a mano (es. `static/css/refined.css`, i font `texgyreadventor-*`, il vecchio CV in `cv_source/`; l'elenco completo è nella consegna).
4. Scheda **Actions**: quando il workflow è verde (1–2 minuti) il sito è online. Se è rosso, online resta la versione precedente.
5. Controlla home, un'esperienza, il CV e un link `?fokus=` su telefono e computer.

Dominio proprio (facoltativo): crea `static/CNAME` con il dominio e configuralo anche in Settings → Pages.
**Attenzione alla cronologia:** i file tolti dal repository restano visibili nella cronologia di Git se il repository è pubblico.

### Link su misura per le candidature

| Candidatura per | Link |
|---|---|
| Marketing, comunicazione, PR, social media | `https://invernizziluca.github.io/work/en/?fokus=content` |
| Business development, vendite, account management | `https://invernizziluca.github.io/work/en/?fokus=kontakte` |
| Project management, eventi, operations | `https://invernizziluca.github.io/work/en/?fokus=koordination` |

Funziona in tutte le lingue (`/work/de/?fokus=kontakte`, `/work/it/?fokus=koordination`) e accetta anche `sales`, `bd`, `projects`, `pm`, `communication`. Le esperienze collegate vengono evidenziate.

---

## Come aggiornare i contenuti

Tutti i testi sono in `content/`. `build.py` e `templates/` non vanno toccati per aggiornare i contenuti.

### Regole (da dare anche a un'AI)

```
Sei lo sviluppatore del mio portfolio business (Python: build.py + Jinja2 + YAML).
Leggi README.md e DESIGN_SYSTEM.md. Modifica SOLO i file in content/ (o creane uno nuovo da vorlagen/).
Regole:
- Ogni testo esiste in de / en / it (il tedesco è obbligatorio). Tedesco con "Sie" quando ti rivolgi al lettore.
- Testi e date tra "virgolette doppie". Mesi "2025-08", date "2026-06-30". Indentazione YAML: 2 spazi.
- Immagini in static/images/…, nei file "/images/…". PDF in static/pdf/…, nei file "/pdf/…".
- Solo fatti dimostrabili. "mine" / "contribution" = ciò che ho fatto io; "credit" / "scope" = ciò che ha fatto il team.
- Ogni prova negli ambiti ha una fonte (zeugnis, screenshot, linkedin, zertifikat, artikel, forschung, eigen) e, se non è "eigen", un href.
- Restituiscimi il file completo.
Compito: <cosa vuoi cambiare>
```

### Dove si trova cosa

| Cosa | File |
|---|---|
| Home: hero, fatti del profilo, ambiti con prove e ruoli, lavori scelti, testi delle sezioni, lingue/strumenti/interessi, SEO | `content/home.yaml` |
| Un'esperienza (pagina propria) | `content/erfahrung/<nome>.yaml` |
| Formazione | `content/ausbildung/<nome>.yaml` |
| Zeugnisse, attestati, ricerche, articoli | `content/nachweise/<nome>.yaml` |
| Citazioni | `content/referenzen/<nome>.yaml` |
| Post LinkedIn | `content/linkedin/<nome>.yaml` |
| Etichette di menu e bottoni | `content/ui.yaml` |
| Indirizzo, lingue, nomi delle cartelle per lingua, aree | `site.yaml` |
| Colori, caratteri, spazi | `static/css/site.css` (sezione 2, token) |
| CV | `cv_source/business-general-2026.tex` → `static/pdf/luca-invernizzi-cv-general-en.pdf` |
| Modelli da copiare | `vorlagen/` |

### Le operazioni più frequenti, nelle tre lingue

**Una nuova esperienza (case study)**
1. Copia `vorlagen/erfahrung.yaml` in `content/erfahrung/<nome>.yaml` (minuscole e trattini: `label-xyz.yaml` → `/work/en/experience/label-xyz/`, `/work/de/erfahrung/label-xyz/`, `/work/it/esperienze/label-xyz/`).
2. Foto in `static/images/works/<nome>/` (WebP o JPG, ~1600 px), ognuna con `alt` in de/en/it e, per materiali di altri, il credito in `caption`.
3. Compila `de:` / `en:` / `it:`: `category`, `summary` (max ~160 caratteri), `context`, `goal`, `contribution`, `tasks`, `scope`, `outputs`, `transfer` (per ambito), `learnings`.
4. `areas:` dice a quali ambiti appartiene (`content`, `kontakte`, `koordination`); `order` la posizione; senza `end:` compare "Aktuell".
5. Per mostrarla tra i lavori scelti: copia `vorlagen/ausgewaehlte-arbeit.yaml` in `content/home.yaml` → `featured: items:` (tre card stanno meglio).

**Una nuova prova in un ambito**
Copia `vorlagen/beleg.yaml` sotto l'ambito giusto in `content/home.yaml` (`focus → areas → evidence`). Con `source: "eigen"` la prova è segnata come dichiarazione propria; per tutte le altre fonti serve `href` (PDF, immagine o link) e la build lo controlla.

**Un post LinkedIn o un link Instagram**
- Post LinkedIn: copia `vorlagen/linkedin.yaml` in `content/linkedin/<nome>.yaml`; `url` = link diretto al post; `author` solo se il post non è tuo. Aggiungi `<nome>` a `posts:` di un'esperienza o di una formazione; con `show_on_home: true` compare anche tra i documenti in home (tre stanno meglio).
- Link Instagram (o un altro link pubblico): nel file dell'esperienza, lista `links:`
  ```yaml
  links:
    - label:
        de: "Instagram-Beitrag (APPLAUS 2026)"
        en: "Instagram post (APPLAUS 2026)"
        it: "Post Instagram (APPLAUS 2026)"
      url: "https://www.instagram.com/p/…/"
  ```

**Un Arbeitszeugnis**
1. Oscura data di nascita, indirizzo, telefono e luogo d'origine **trasformando la pagina in immagine** (un rettangolo nero sopra il testo non basta). Controlla con `pdftotext file.pdf -` e pulisci titolo/autore del PDF.
2. PDF in `static/pdf/`, miniatura (dalla versione oscurata) in `static/images/proof/`.
3. Copia `vorlagen/nachweis.yaml` in `content/nachweise/zeugnis-<firma>.yaml` con `type: "zeugnis"`; cita le frasi alla lettera tra „…“.
4. Collegalo all'esperienza (`documents: ["zeugnis-<firma>"]`); per una citazione in home usa `vorlagen/referenz.yaml`; per una prova negli ambiti `source: "zeugnis"` con `href: "/pdf/zeugnis-<firma>.pdf"`.

**Una metrica con screenshot**
1. Screenshot senza dati personali in `static/images/works/<esperienza>/`, nella `gallery` dell'esperienza con un `alt` che riporta i numeri.
2. Nell'esperienza:
   ```yaml
   de:
     highlights:
       - value: "83.767"
         label: "Aufrufe auf Instagram in 14 Tagen (5.–18. August)"
     highlights_source: "Quelle: Instagram Insights des Vereinskontos (Screenshot unten)."
   ```
   e lo stesso in `en:` (83,767 · 59.8%) e `it:` (83.767 · 59,8 %). La build pretende `highlights_source` quando ci sono numeri.
3. In `scope` scrivi a cosa si riferisce il numero (tutto l'account? pubblicità sì/no?). Per mostrarla in home: `metric` in `vorlagen/ausgewaehlte-arbeit.yaml` o una prova con `source: "screenshot"`.

**Un progetto universitario**
- Il PDF (oscurato se serve) in `static/pdf/` e `vorlagen/nachweis.yaml` con `type: "forschung"` o `"zertifikat"` (articoli: `type: "artikel"` con `url`).
- In `content/ausbildung/ffhs.yaml` una riga in `points:` nelle tre lingue; un post LinkedIn in `posts: [...]`.
- Se dimostra una competenza, aggiungi una prova in un ambito con `org: {de: "FFHS, Studium", en: "FFHS, studies", it: "FFHS, studi"}`.

**Altri casi**
- Fine dello stage all'Initiative Musik: `end: "2027-02"` in `content/erfahrung/initiative-musik.yaml`, aggiorna `outputs`; con lo Zeugnis aggiungi PDF e `documents:`.
- Laurea FFHS: in `content/ausbildung/ffhs.yaml` sostituisci `expected_end:` con `end:` (la FFHS passa da `affiliation` ad `alumniOf` nei dati strutturati).
- Errore della build: il messaggio indica file e campo, es. `content/erfahrung/label-xyz.yaml → start: use the format "YYYY-MM"`.

### Il CV

`cv_source/business-general-2026.tex` (XeLaTeX, font Archivo in `cv_source/fonts/`):
```bash
cd cv_source
xelatex business-general-2026.tex && xelatex business-general-2026.tex
cp business-general-2026.pdf ../static/pdf/luca-invernizzi-cv-general-en.pdf
```
Su Overleaf: carica il file e la cartella `fonts/`, compilatore **XeLaTeX**. Telefono e cittadinanza sono nascosti nel PDF pubblico: per un CV da inviare direttamente usa `\showphonetrue` e `\showcitizenshiptrue`. È un CV generale: per una candidatura specifica crea una copia del file, non modificare quello pubblicato.

---

## Prima di pubblicare: controllo rapido

- [ ] `python3 build.py` senza errori.
- [ ] Nessun numero o risultato senza fonte; "La mia parte" contiene solo il tuo lavoro.
- [ ] Nessun dato personale nei PDF e nelle immagini (data di nascita, indirizzo, telefono, volti e nomi di terzi negli screenshot).
- [ ] Nessun documento interno di un datore di lavoro in `static/`.
- [ ] Permesso per i visual di terzi (APPLAUS); altrimenti togli le voci dalla `gallery` e dalla card in home e lascia i link ai post.
- [ ] Home, un'esperienza e un link `?fokus=` controllati su telefono e computer.

## Struttura del progetto

```
build.py                 legge e controlla content/, crea dist/ (pagine, immagini ridotte, anteprime, sitemap)
site.yaml                indirizzo, lingue, cartelle per lingua, ambiti
content/                 tutti i testi
  home.yaml                home: hero, fatti, ambiti con prove, lavori scelti, sezioni, lingue/strumenti
  ui.yaml                  etichette dell'interfaccia (de/en/it con le stesse chiavi)
  erfahrung/*.yaml         esperienze (un file = una pagina per lingua)
  ausbildung/*.yaml        formazione
  nachweise/*.yaml         Zeugnisse, attestati, ricerche, articoli
  referenzen/*.yaml        citazioni
  linkedin/*.yaml          post LinkedIn
templates/               base, _header, _footer, _macros, home, station (esperienza), 404
static/                  css/site.css, js/site.js, fonts/ (Archivo), images/, pdf/, favicon
scripts/fonts/           Archivo statico per le immagini di anteprima
scripts/brand/           logo sorgente
cv_source/               CV in LaTeX + font
vorlagen/                modelli per nuovi contenuti
.github/workflows/deploy.yml  pubblicazione su GitHub Pages
```

## Note tecniche

- **Link relativi**: le pagine si collegano con percorsi relativi, quindi il sito funziona sotto `/work/`, con un dominio proprio o in locale. Solo la pagina 404 usa link assoluti (`/work/…`), perché GitHub la mostra a qualsiasi indirizzo.
- **Immagini**: versioni WebP da 480/960/1600 px in `dist/generated/img/` (cache in `.cache/`); anteprime 1200 × 630 per home ed esperienze in `dist/generated/og/`.
- **SEO**: title e description per pagina, canonical, hreflang EN/DE/IT + x-default, dati strutturati (Person con `alumniOf`/`affiliation`), `sitemap.xml`. Il `robots.txt` che conta è quello alla radice del dominio (sito musicale): indica anche questa sitemap.
- **Tema**: solo chiaro, anche con il dispositivo in modalità scura.
- **JavaScript** (`static/js/site.js`, 8 KB): tab degli ambiti e link `?fokus=`, chiusura del menu mobile, lightbox. Senza JavaScript tutto resta leggibile.
- **Accessibilità**: skip link, focus visibile, alt text, contrasto AA, tab con le frecce, menu e lightbox da tastiera, "riduci movimento".
- **Nessun cookie, nessun tracciamento, nessuna richiesta a servizi esterni.**
