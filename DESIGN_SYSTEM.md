# Design system · Luca Invernizzi

Un solo sistema per due siti:

| | Sito musicale | Sito business |
|---|---|---|
| Indirizzo | `https://invernizziluca.github.io/` | `https://invernizziluca.github.io/work/` |
| Pubblico | label, management, PR, agenzie musicali | tech, marketing, vendite, consulting, business development |
| Tecnologia | Astro 4 (`src/styles/site.css`) | Python + Jinja2 + YAML (`static/css/site.css`) |
| Edizione | più visiva e narrativa | più asciutta, strutturata e misurabile |

Questo file è identico nei due repository. Se cambi un token, cambialo in entrambi i CSS: i nomi sono gli stessi.

---

## 1. Principi

1. **Il lavoro prima della biografia.** In alto: chi sono, cosa faccio, tre o cinque lavori scelti. Le liste lunghe vengono dopo.
2. **Ogni affermazione ha un proprietario e una fonte.** "La mia parte" e "Team e diritti" sono separati in ogni card e in ogni case study; i numeri dicono sempre da dove vengono.
3. **Chiaro, mai in dark mode automatico.** Solo tema chiaro (`color-scheme: light`, nessuna regola `prefers-color-scheme: dark`): i siti restano chiari anche se il dispositivo è in modalità scura.
4. **Un solo carattere, molte voci.** Archivo variabile per tutto; la gerarchia nasce da peso, larghezza e dimensione, non da caratteri diversi.
5. **Niente decorazione che non informa.** Nessun gradiente, nessuna ombra pesante, nessuna card dentro una card. Le linee separano contenuti, le superfici grigie raggruppano oggetti veri (documenti, post, citazioni).

## 2. Le due edizioni

| Token / scelta | Musica | Business |
|---|---|---|
| `--wdth-display` (larghezza dei titoli) | `112%` (più largo, più "copertina") | `100%` (normale, più sobrio) |
| `--weight-display` | `660` | `640` |
| Colori | caldi, come il sito precedente e il CV: carta `#faf7f2`, fasce sabbia `#f1e7d8`, caramello `#7a4f22`, oro `#c9a25a`, inchiostro `#1c1c20`; contatto su fascia scura | freddi e bianchi (tabella sotto) |
| Hero | ritratto grande, fatti in riga | nome e claim a sinistra, pannello profilo con foto piccola e fatti |
| Lavori scelti | 1 lavoro in evidenza (APPLAUS, 4 visual) + 4 card | 3 card con metrica dove c'è una fonte |
| Elementi propri | player Spotify che si carica al clic, artisti | tre ambiti come segmented control, righe di prova con chip della fonte, link `?fokus=` |
| Marchio | "L" con il disco (il tuo logo musicale), in oro | "LI" geometrico con la sfaccettatura verde petrolio, in SVG |
| CV | `cv-source/music-general-2026.tex` (tedesco, nome in Archivo Expanded) | `cv_source/business-general-2026.tex` (inglese, nome in Archivo Bold) |

## 3. Carattere: Archivo

- **Perché Archivo** (confronto con System UI + TeX Gyre Adventor del vecchio sito business):
  - leggibilità a schermo migliore a 15–17 px (occhio medio-alto, aperture ampie), Adventor è geometrico e stretto nelle lettere tonde;
  - un file variabile con pesi 100–900 e larghezze 62–125 %: le due edizioni usano lo stesso file con impostazioni diverse;
  - corsivo vero (non obliquo sintetico) e cifre tabellari per date e numeri (`font-variant-numeric: tabular-nums`);
  - copre tedesco, italiano e i caratteri dell'Europa centrale (sottoinsieme `latin-ext` caricato solo se serve);
  - licenza SIL OFL 1.1 senza "Reserved Font Name": si può ospitare, ridurre e incorporare nei PDF.
- **File**: `archivo-latin-wdth-normal.woff2` (90 KB) è l'unico che una pagina carica di solito, con `preload` e `font-display: swap`. Corsivo (102 KB) e `latin-ext` (86/93 KB) si scaricano solo se una pagina li usa (`unicode-range`). Nessuna richiesta a Google Fonts.
- **CV**: istanze statiche TTF (Regular, SemiBold, Bold, Italic, BoldItalic, ExpandedBold) generate dal file variabile con fontTools, in `cv-source/fonts/` e `cv_source/fonts/`.

### Scala tipografica

| Token | Valore | Uso |
|---|---|---|
| `--text-xs` | 13 px | meta, etichette, didascalie |
| `--text-sm` | 15 px | testo secondario, link nelle card |
| `--text-base` | 17 px | testo |
| `--text-lg` | 18–20 px | intro di sezione, lead |
| `--text-xl` | 20–24 px | titoli di card e di sezione nei case study |
| `--text-2xl` | 24–36 px | claim, titoli medi |
| `--text-3xl` | 32–54 px | titoli di sezione, metriche |
| `--text-4xl` | 44–96 px | nome nella hero, "Kontakt" |

Le dimensioni da `--text-lg` in su sono fluide (`clamp`). Interlinea 1.6 per il testo, 0.96–1.2 per i titoli; spaziatura negativa solo sui titoli grandi. Righe di testo al massimo ~46 rem (circa 75 caratteri).

## 4. Colori

La tabella vale per il sito business. Il sito musicale usa gli stessi nomi di token con valori caldi (vedi sotto).

| Token | Hex | Uso | Contrasto su bianco |
|---|---|---|---|
| `--ink` | `#15253e` | testo, bottone primario | 15,4 : 1 |
| `--ink-hover` | `#1f3a5f` | hover del bottone primario | 11,5 : 1 |
| `--ink-2` | `#525e6e` | testo secondario | 6,6 : 1 |
| `--ink-3` | `#636e7d` | meta, didascalie | 5,2 : 1 (4,75 : 1 su `--surface`) |
| `--accent` | `#2b6b75` | link, etichette, focus | 6,1 : 1 |
| `--accent-strong` | `#245a63` | hover dei link, testo nei badge | 7,7 : 1 |
| `--accent-soft` | `#e8f1f2` | sfondo di badge e chip della fonte | decorativo |
| `--accent-brand` | `#337781` | sfaccettatura del logo, solo decorativo | — |
| `--surface` | `#f4f5f7` | fasce grigie alternate, pannelli | — |
| `--surface-2` | `#eceff3` | hover su fasce grigie, segmented control | — |
| `--line` / `--line-strong` | `#e3e6eb` / `#cbd1d9` | linee di separazione | — |

**Edizione musicale** (`src/styles/site.css`): `--ink #1c1c20` (15,9 : 1 sulla carta), `--ink-2 #4a4b52` (8,1 : 1), `--ink-3 #5d5e67` (6,0 : 1; 5,3 : 1 sulla sabbia), `--accent #7a4f22` caramello (6,6 : 1; 5,8 : 1 sulla sabbia), `--accent-brand`/`--gold #c9a25a` (logo, bottone sulla fascia scura, 7,1 : 1 su inchiostro), `--bg #faf7f2`, `--surface #f1e7d8`, `--surface-2 #e8dac4`, `--card-bg #fffdf9`, `--line #e4d8c5`.

Tutto il testo supera WCAG 2.2 AA (4,5 : 1; 3 : 1 per testo grande). Il controllo automatico è stato fatto su tutte le pagine dei due siti (vedi CHANGELOG).

## 5. Spazi, raggi, griglia

- **Spaziatura 8 pt**: `--space-1` 4 px · `--space-2` 8 · `--space-3` 12 · `--space-4` 16 · `--space-5` 24 · `--space-6` 32 · `--space-7` 40 · `--space-8` 48 · `--space-9` 64 · `--space-10` 80 · `--space-11` 96 · `--space-12` 128. Le sezioni usano `--section-y` (64–112 px).
- **Raggi** con gerarchia, non uno per tutto: `--radius-sm` 10 px (miniature, chip), `--radius-md` 16 px (immagini nelle liste, note), `--radius-lg` 24 px (card, pannelli), `--radius-xl` 32 px (media grandi, pannelli hero), `--radius-pill` (bottoni, badge, tab).
- **Griglia**: contenitore 1200 px (`--container`), margini laterali 16–40 px (`--gutter`). Punti di rottura usati: 560, 640, 760, 900, 960, 1024 (musica: menu completo) / 1100 px (business: menu completo).
- Verificato a 360, 390, 768, 1024 e 1440 px senza scorrimento orizzontale.

## 6. Componenti (stessi nomi nei due siti)

| Componente | Classi | Note |
|---|---|---|
| Header | `site-header`, `brand`, `site-nav`, `lang-switch`, `menu` | sticky, bianco al 90 % con sfocatura; menu mobile con `<details>` (funziona senza JavaScript) |
| Bottoni | `btn btn--primary / --secondary / --small` | pillola, altezza minima 48 px (40 px la versione piccola) |
| Sezione | `section`, `section--tint`, `section-head` | fasce bianche e grigie alternate |
| Link | `link`, `link--strong` | sottolineati; i link esterni hanno la freccia e "si apre in una nuova scheda" per gli screen reader, e la freccia non va mai a capo da sola |
| Card lavoro | `work-card`, `work-grid` | immagine 3:2 o 4:3, etichetta, titolo, testo, `attribution` |
| Attribuzione | `attribution` (`dt` "La mia parte" / "Team e diritti") | obbligatoria in ogni lavoro scelto |
| Metrica | `metric` (card), `metrics` + `metrics__source` (case study) | solo con fonte visibile |
| Righe | `rows`, `row` | esperienze in home; tutta la riga è cliccabile, focus visibile sulla riga |
| Citazioni | `quotes`, `quote`, `quote--featured` | foto o iniziali, fonte e data, "Tradotto dal tedesco" |
| Documenti | `docs`, `doc` | miniatura, tipo, data, fonte, azione |
| Post LinkedIn | `posts`, `post` | anteprima senza iframe, tutta la card porta al post |
| Case study | `case-hero`, `case-cover`, `facts`, `case-section`, `note`, `gallery`, `lightbox`, `pager` | ordine fisso: Contesto → Obiettivo → Il mio contributo (+ Cosa non è mio) → Risultati → Riscontri → Strumenti → Cosa porto con me |
| Solo musica | `feature` (APPLAUS), `spotify`, `players`, `split` | Spotify si carica solo dopo il clic |
| Solo business | `profile`, `lens` (tab), `evidence`, `source`, `tags`, `edu`, `transfer` | `source--eigen` (dichiarazione propria) è volutamente neutra e solo contornata |

## 7. Immagini

- Formati WebP o JPG, lato lungo 1600–1800 px; le build creano versioni da 480/960/1600 px e immagini di anteprima 1200 × 630.
- Copertine sotto i 1000 px di larghezza non vengono ingrandite: restano alla loro misura (`case-cover--small`).
- Ogni immagine ha `width`/`height` (nessuno spostamento del layout), `loading="lazy"` sotto la piega, testo alternativo che descrive cosa si vede (vuoto solo se decorativa).
- Materiale di terzi (es. visual APPLAUS) porta il credito in didascalia ("Visual: Initiative Musik") e non viene presentato come grafica propria.
- Niente screenshot con dati privati di altre persone (esempio: del panel Zoom si mostra solo la parte con le domande).
- Nessun metadato EXIF/GPS nelle immagini pubblicate (controllato).

## 8. Movimento

Solo transizioni brevi su hover e focus (160–280 ms) e un leggero ingresso del pannello quando si cambia ambito (business). Con "riduci movimento" attivo tutto è immediato e lo scroll non è animato.

## 9. Accessibilità

- Link "Vai al contenuto" come primo elemento, `lang` corretto su ogni pagina e sui link di cambio lingua.
- Focus visibile ovunque (anello 3 px `--focus`), anche sulle righe cliccabili.
- Target di almeno 24 × 24 px (menu mobile 48 px).
- Tab degli ambiti con frecce, Home/End, `aria-selected`; senza JavaScript tutti gli ambiti restano visibili uno sotto l'altro.
- Lightbox con `<dialog>`: si apre con Invio, frecce per le immagini, Esc per chiudere, il focus torna alla galleria.
- Un solo `h1` per pagina, livelli dei titoli senza salti.

## 10. Scrittura

- Prima persona, frasi brevi, verbi concreti. Tedesco: "du" sul sito musicale, "Sie" sul sito business. Italiano: "tu".
- "La mia parte" dice solo ciò che ho fatto io; tutto il resto va in "Team e diritti" o in "Cosa non è mio".
- I numeri riportano periodo e fonte (screenshot, Zeugnis, dichiarazione propria). Le dichiarazioni proprie sono segnate come tali.
- Citazioni da Zeugnisse sempre letterali, tra virgolette („…“ in tedesco, “…” in inglese, «…» in italiano).
- Nessuna parola ripetuta come etichetta sopra ogni titolo, niente maiuscolo per le etichette, niente emoji.

## 11. Dove cambiare cosa

| Cosa | Sito musicale | Sito business |
|---|---|---|
| Token (colori, font, spazi, raggi) | `src/styles/site.css`, sezione 2 | `static/css/site.css`, sezione 2 |
| Font | `src/assets/fonts/` | `static/fonts/` |
| Logo e icone | `scripts/brand/make_brand_assets.py` → `public/images/brand/`, `public/favicon.png`, `public/apple-touch-icon.png` | `static/images/brand/li-logo.svg`, `static/favicon.svg`, `static/favicon.png`, `static/apple-touch-icon.png` |
| Immagini di anteprima (Open Graph) | `scripts/prepare-images.mjs` + `public/images/og/home.jpg` | generate da `build.py` (`build_og_images`) |
| Etichette dell'interfaccia | `src/i18n.ts` | `content/ui.yaml` |
