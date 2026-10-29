# Changelog · sito business

## 3.0 · 29 ottobre 2026 · Redesign "light"

Non pubblicato: tutte le modifiche sono pronte per la tua revisione, nessun commit e nessun deploy.

### Design
- Nuovo design system condiviso con il sito musicale (vedi `DESIGN_SYSTEM.md`): **Archivo** al posto di System UI + TeX Gyre Adventor, colori blu notte e verde petrolio con contrasto AA, spaziatura 8 pt, quattro raggi, solo tema chiaro (anche con il dispositivo in modalità scura).
- Edizione business: titoli a larghezza normale, gerarchia sobria, molta aria.
- Home: hero con nome, claim "Marketing, client relationships and digital projects" e pannello profilo (foto, base, cittadinanza, studi, lingue, disponibilità) → **Focus areas** (Marketing / Clients / Projects come segmented control) → **Selected work** (APPLAUS, Verbano con metrica, Gebrüder Fritz CRM) → Experience → Education → References → Documents (lista unica) → Languages and tools → Contact.
- Ogni prova negli ambiti mostra la fonte come chip: Zeugnis, screenshot, post LinkedIn, attestato, articolo, ricerca; la "dichiarazione propria" è volutamente neutra.
- I link `?fokus=content|kontakte|koordination` (anche `sales`, `projects`, …) aprono l'ambito giusto ed evidenziano le esperienze collegate; senza JavaScript tutti gli ambiti sono visibili.
- Pagine esperienza con ordine fisso: Contesto → Obiettivo → Il mio contributo (+ Cosa non è mio) → Risultati (con fonte) → Trasferibile a → Riscontri → Strumenti → Cosa porto con me → esperienze più recenti/precedenti.
- Logo LI vettoriale (`static/images/brand/li-logo.svg`), favicon SVG/PNG e apple-touch-icon nuovi.
- Immagini di anteprima (Open Graph) bianche, con Archivo e logo, generate da `build.py` per home ed esperienze in tre lingue.
- Mobile: post e documenti compatti, nessuno scorrimento orizzontale a 360/390/768/1024/1440 px.
- Tolti `refined.css`, il vecchio CSS "carta e caramello" e i font Adventor.

### Contenuti (EN/DE/IT)
- Initiative Musik: testi della maggior parte dei post APPLAUS 2026 pubblicati (non foto, grafica o guida della campagna), monitoring, report, newsletter, sito, storie live; articolo domicil solo come supporto redazionale (testo Thomas Venker); Herbstfest al Tresor separato da APPLAUS. Tolti "Grafik und Video" e il nome della reception alla Most Wanted.
- Eintracht Pankow: compiti come da Zeugnis; tolti i "highlight" senza fonte; "Teilnahme" a Branchentreffen invece di "Vertretung"; citazione letterale della valutazione.
- Gebrüder Fritz: CRM Pipedrive, Sevdesk, Mailchimp, eventi, Eisenhower-Matrix, tutto come da Zeugnis; cosa decidevano direzione e team sales.
- Verbano Unihockey: 83.767 visualizzazioni in 14 giorni, 59,8 % da non follower, 4.775 account raggiunti (+1.931,9 %) con fonte e limiti; ruolo "Digital Marketing & Social Media (ehrenamtlich)".
- Progetto musicale: "einzelne Beiträge mit über 30.000 Aufrufen (eigene Angabe)" al posto di "im Schnitt 30.000"; Jake La Furia solo "mögliche Zusammenarbeit in Vorbereitung", tolta la "Managementvereinbarung".
- Formazione: "Passerelle Berufsmaturität – universitäre Hochschulen" (non "gymnasiale Maturität"); FFHS con fine prevista 07/2028 e nome inglese ufficiale nella versione EN.
- Strumenti in gruppi (vendite, web e newsletter, contenuti, organizzazione, IA); Excel indicato come "basic".
- Meta description e titoli di pagina più corti (≤ 160 / ~75 caratteri).

### Privacy
- PDF con metadati puliti (titolo, autore, lingua): Zeugnisse, attestato TOPSIM, lavori di ricerca.
- Screenshot del panel Zoom sostituito da un ritaglio con le sole domande (nessun volto né nome); l'originale è tolto dal repository e consegnato a parte.
- CV pubblico senza telefono e senza cittadinanza (si attivano nel sorgente).
- Note di lavoro interne tolte dal repository (consegnate a parte).

### CV
- Nuovo `cv_source/business-general-2026.tex`: CV generale business in inglese (non personalizzato per un'azienda), XeLaTeX con Archivo, A4 una pagina, testo selezionabile, link `https://invernizziluca.github.io/work/`. Sostituisce il vecchio template Letter con telefono. PDF in `static/pdf/luca-invernizzi-cv-general-en.pdf`.

### Tecnica (`build.py`)
- Controlli nuovi: hero, ambiti (ogni prova con `href` se non è "eigen"), lavori scelti (`mine` obbligatorio, `metric` con fonte), campi `category`/`goal`/`scope`/`highlights_source`, `expected_end`, post per la formazione, `show_on_home`.
- Periodi con fine prevista ("02/2024 – voraussichtlich 07/2028").
- Pagina 404 con link assoluti (`/work/…`), così funziona a qualsiasi indirizzo.
- JSON-LD: `alumniOf` solo per titoli conseguiti, `affiliation` per la FFHS.
- `requirements.txt` con limiti di versione; workflow con cache pip e azioni che girano su Node 24 (richiesto da GitHub da settembre 2026).
- Modelli in `vorlagen/` aggiornati, più due nuovi: `ausgewaehlte-arbeit.yaml` e `beleg.yaml`. Tutti verificati con una build di prova.

### Verifiche eseguite (29.10.2026)
- `pip install` **non eseguibile** (registro PyPI bloccato in questo ambiente); PyYAML 6.0.3, Jinja2 3.1.6 e Pillow 12.3 erano già installati.
- `python3 build.py`: 20 pagine HTML (EN/DE/IT + root + 404), 45 immagini, 18 immagini di anteprima, nessun errore.
- Controlli automatici su tutte le 20 pagine: link interni e immagini (154 URL, nessun errore), un solo `h1`, nessun salto di titoli, alt su tutte le immagini, contrasto AA, target ≥ 24 px, canonical/hreflang/og:image, modalità scura del browser (resta chiaro), "riduci movimento".
- Tastiera: skip link, focus visibile, menu mobile (Invio/Esc), tab degli ambiti con frecce, link `?fokus=`, lightbox (Invio, frecce, Esc).
- Nessun layout shift (CLS 0) su home e pagine esperienza a 390 e 1440 px.
- CV: una pagina, testo selezionabile, link corretti.
