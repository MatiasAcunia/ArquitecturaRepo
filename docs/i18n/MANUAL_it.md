# ArquitecturaRepo — Manuale pratico v1.4.0 (italiano)

Questa guida descrive otto passaggi (00–07) per adottare **v1.4.0** in un progetto reale. È una **guida pratica nuova**, non la traduzione completa del precedente manuale spagnolo v1.3, conservato nel repository sorgente. La distribuzione verificabile è la [release immutabile v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0); v1.3.0 resta disponibile come versione precedente.

Questo manuale è stato aggiunto a `main` **dopo** la pubblicazione della v1.4.0. Lo ZIP e il container originali e immutabili v1.4.0 **non lo includono**. Una futura distribuzione offline richiederà una nuova versione distinta.

## 00 · Prima di iniziare

ArquitecturaRepo è un livello di coordinamento **locale al repository** per requisiti, decisioni, responsabilità, stato corrente, campagne, prove e recupero dopo interruzioni. Non è un generatore automatico di applicazioni né sostituisce Codex.

- CLIENT definisce il prodotto, autorizza operazioni sensibili e valuta il risultato visibile.
- I1 coordina più progetti solo quando serve; I2 Planner definisce strategia, capacità e criteri di accettazione.
- I3 Controller implementa, integra, testa, corregge e riprende il lavoro nella campagna autorizzata.
- I4 è opzionale; **quattro ruoli non richiedono quattro agenti**.

L'applicazione può restare privata. Lo starter pubblico non richiede codice, database, credenziali o conversazioni private. L'accesso di fornitori esterni dipende da autorizzazioni separate: l'installazione non concede permessi automaticamente.

## 01 · Installazione sicura

Usa Python 3.12, verificato nella CI. Scarica lo [ZIP portabile v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/download/v1.4.0/ArquitecturaRepo-v1.4.0-portable.zip), verifica il `.sha256` pubblicato, estrai il contenuto e apri un terminale **nella cartella del framework**. In alternativa usa il tag Git immutabile `v1.4.0`.

Per un progetto nuovo, o già con codice ma **senza controllo canonico**, scegli `SMALL`:

```bash
python "tools/scaffold_project.py" --target "../mio-progetto" --profile SMALL --product-id MIO_PROGETTO --objective "Obiettivo iniziale da confermare" --language it --no-feedback-workflow
```

Windows PowerShell:

```powershell
python "tools\scaffold_project.py" --target "..\mio-progetto" --profile "SMALL" --product-id "MIO_PROGETTO" --objective "Obiettivo iniziale da confermare" --language "it" --no-feedback-workflow
```

Il programma aggiunge `.agentic-sdlc/` preservando codice e workflow esistenti; rifiuta di sovrascrivere un controller precedente. `--no-feedback-workflow` disabilita la pianificazione, **non** il generatore locale. Per fermare qualsiasi report imposta `enabled=false` in `.agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json`. Non è incluso un collettore esterno.

Poi, **nella cartella del progetto di destinazione**:

```bash
python -m pip install -r ".agentic-sdlc/requirements-validation.txt"
python ".agentic-sdlc/tools/project_status.py" --control-root ".agentic-sdlc"
python ".agentic-sdlc/tools/discover_project.py" --project-root "."
python ".agentic-sdlc/tools/reconstruct_context.py" --root ".agentic-sdlc"
```

Su PowerShell usa percorsi tra virgolette con `\`. Il primo stato `HOLD / UNTRUSTED_CONTEXT` è **normale**: prima bisogna confermare requisiti, sorgente e autorità. Se esistono Product State, campagne o controller, **non installare sopra**: segui la [verifica in sola lettura](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/32_EXISTING_GOVERNED_ATTACHMENT.md). Nessuna migrazione automatica generale da v1.2/v1.3.

## 02 · Planner e adozione

Esamina codice reale, utenti, dati, requisiti, vincoli di sicurezza, integrazioni e rischi. CLIENT conferma la base del prodotto. I2 redige un charter di **capacità**: risultato, confini, responsabili, interfacce, verifiche e condizioni di rifiuto. Non copiare il Product State sintetico degli esempi né confondere l'installazione con un'autorizzazione a eseguire.

## 03 · Lavoro quotidiano

Riparti sempre da Git, stato CURRENT e prove, non solo dalla cronologia del chat. I3 gestisce sviluppo, test, correzioni e recupero nella **stessa campagna autorizzata**; un bug ordinario non richiede una nuova campagna. In caso di conflitti su Git, SQLite WAL, identità o lease, resta in `HOLD`. La CI portabile non dimostra integrazioni native Codex Desktop/Goals o servizi esterni.

## 04 · Richiedere modifiche

Specifica risultato osservabile, contesto, limiti e verifica di accettazione. Esempio: “Mostrare quote non pagate senza perdere i pagamenti precedenti; controllare i casi pagati e scaduti”. I2 valuta i cambiamenti strategici; I3 gestisce le modifiche interne già autorizzate.

## 05 · Errori e recupero

- `UNTRUSTED_CONTEXT`: verifica la realtà del progetto; non modificare il valore di stato per ottenere un falso verde.
- `jsonschema` mancante: installa `requirements-validation.txt` dal progetto creato.
- `EXISTING_CONTROL_PRESERVED`: fermati, usa il percorso in sola lettura, senza `--force` né cancellazioni.
- Conflitti Git/SQLite WAL/lease: sospendi le modifiche finché le prove non coincidono.
- Interruzione: conserva journal, identità di esecuzione e artefatti; riprendi la campagna originale. Elimina solo file di cui è verificata la proprietà.

Negli Issues pubblici pubblica solo passi riproducibili e log anonimizzati, mai token, percorsi personali, nomi privati, dati o conversazioni.

## 06 · Accettazione delle capacità

Valuta separatamente test unitari, integrazione, DB/currentness, semantica, funzionamento fisico, esperienza umana e release. Test verdi non sostituiscono l'accettazione del CLIENT. Registra fonte precisa, prove, responsabili e decisione negli archivi canonici. La CI sintetica non certifica un'applicazione in produzione.

## 07 · Esempio: associazione soci

1. CLIENT chiede anagrafica soci, quote e elenco degli arretrati.
2. I2 controlla database e autorizzazioni reali e definisce la capacità minima utile.
3. I3 realizza socio → quota → arretrati e verifica persistenza e ripresa.
4. Un errore di calcolo viene corretto nella **stessa** campagna.
5. CLIENT prova il flusso reale e accetta o restituisce osservazioni; le prove restano nel repository.

## Riferimenti e limiti

[Guida breve](README_it.md) · [FAQ](FAQ_it.md) · [README principale](../../README.md) · [Ambito verificato v1.4](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/46_V1_4_PUBLIC_START_AND_SUPPORT.md).

Questo documento non certifica sicurezza di produzione, usabilità indipendente, integrazione nativa o superiorità misurata rispetto a Codex diretto. La licenza MIT non copre automaticamente contenuti di terzi.
