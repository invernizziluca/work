# Portfolio generale · Light Edition

Questo progetto è il **portfolio generale** (business, marketing, consulting, Google, altri datori). **Non** sostituisce il sito musicale: per music industry utilizza `https://invernizziluca.github.io/` senza `/work/`.

## Risultato

- Homepage in inglese all'indirizzo `/work/`; tedesco in `/work/de/`, italiano in `/work/it/`.
- Tema **sempre chiaro**, anche su dispositivi impostati in dark mode.
- Layout desktop: contenuti e prove a sinistra; foto, status e contatti a destra. Mobile: una colonna.
- 3 aree di esperienza, selezionabili anche con `?fokus=content`, `?fokus=kontakte` e `?fokus=koordination`. Mantieni questi ID anche se cambi le etichette.
- Homepage: risultati documentati, esperienza professionale, formazione, referenze, PDF con informazioni sensibili oscurate.

## Come personalizzare il sito tramite ChatGPT

| Modifica | File |
|---|---|
| Testi homepage, residenza, lingua, prove, nuove statistiche | `content/home.yaml` |
| Nuovo incarico (titolo, periodi, attività, immagini) | `content/erfahrung/*.yaml` |
| Università e date | `content/ausbildung/*.yaml` |
| Nuovi attestati / documenti / progetti | `content/nachweise/*.yaml`, `static/pdf/` |
| Nuova citazione / referenza | `content/referenzen/*.yaml` |
| **Colori, bordi arrotondati, font, dimensioni, spaziature** | `static/css/refined.css` |
| Layout HTML e aggiunta sezioni | `templates/home.html` o `templates/station.html` |
| Sezioni, menu, etichette tradotte | `content/ui.yaml` |
| URL produzione e ordine lingue | `site.yaml` |

Le impostazioni visive più importanti sono all'inizio di `static/css/refined.css` sotto `:root`. Non modificare `static/css/site.css` se devi solo cambiare colori o spaziature; è lo scheletro del sito originale.

Ogni testo pubblico deve essere scritto in **EN / DE / IT**. In contenuti YAML mai confondere dati verificati con ipotesi. Per le metriche, conserva intervalli e definizioni (esempio: **83.767 visualizzazioni in 14 giorni**, non 83.767 follower). **Non** dichiarare competenze in paid ads, Google Ads o Analytics senza prova.

### Esempio prompt per i prossimi aggiornamenti

> Aggiorna il mio portfolio generale usando questa nuova esperienza/documento. Leggi README.md e DESIGN_GUIDE.md. Modifica gli YAML corrispondenti in inglese, tedesco e italiano; mantieni il layout Light Edition in `static/css/refined.css`. Usa solo dati verificabili; includi provenienza delle metriche. Esegui `python build.py --preview`, controlla che tutte le pagine siano generate e restituiscimi un ZIP pronto per GitHub Pages.

## Anteprima e pubblicazione

```bash
pip install -r requirements.txt
python build.py --preview
python -m http.server 8000 --directory dist
# Apri http://localhost:8000/ o http://localhost:8000/en/
```

Per pubblicare su `https://invernizziluca.github.io/work/`: usa il repository GitHub chiamato esattamente `work`, carica il progetto, abilita **Settings > Pages > Build and deployment > GitHub Actions**, quindi esegui push su `main`. Il file `.github/workflows/deploy.yml` compila e pubblica automaticamente `dist/`.

**Prima di pubblicare:** verifica l'anteprima e gli URL. Non caricare dati personali non oscurati, né usare il Google CV specifico per una posizione come résumé generale pubblico senza volerlo.

## Nota: alcuni testi da verificare nel tempo

- Termine del tirocinio Initiative Musik, da aggiornare appena confermato.
- Eventuali nuove attività o risultati e i relativi documenti.
- Residenza e disponibilità, da modificare se cambiano.
- Informazioni universitarie se varia la data prevista di laurea.

## Qualità / accessibilità

Una pagina responsive, testo selezionabile, link tradotti, alt per immagini informative, focus tastiera, layout ridotto senza JS, immagini ottimizzate dal generatore. Nessun cookie o tracciamento introdotto.
