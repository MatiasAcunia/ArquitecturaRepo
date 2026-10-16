# Ponte di continuità degli agenti — Agent Continuity Bridge 0.2.1

## Perché esiste

ArquitecturaRepo governa autorità, piani e accettazione dello sviluppo. Questo componente facoltativo separa l’integrazione con un controller esterno di continuità degli agenti, con versione indipendente. Non è un modello IA né un secondo responsabile della campagna. Il nucleo portabile funziona senza.

## Funzioni attualmente verificate

Controllo offline di uno ZIP Codex Daily Control 3.1 fornito separatamente: percorsi sicuri, inventario, SHA-256, versione e coerenza della configurazione; registra l’impronta nel progetto, ne verifica l’identità e rimuove soltanto la propria registrazione. Nessun dato privato, credenziale o identificativo Goal viene distribuito.

## Requisiti e collegamento

Python 3.10+; progetto ArquitecturaRepo esistente con .agentic-sdlc; archivio 3.1 ottenuto separatamente. Per eseguire il controller nativo servono Windows, PowerShell 5.1, Codex Desktop compatibile e Git, SQLite ed eventuali Drive/rclone configurati a parte. Il ponte non li installa.

## Sicurezza e limiti

La versione 3.1 è una release candidate senza collaudo fisico Windows/Codex. Chiusura nativa, passaggio Desktop, ripristino quote e consegna remota restano disabilitati/non verificati.

## CLI

```bash
python "bridge.py" inspect --package "CONTROLLER_3_1.zip"
python "bridge.py" install --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" status --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" uninstall --project "MY_PROJECT"
```


Installazione in un progetto esistente: `python install_into_project.py --project "PROGETTO"`. Esegui `.agentic-sdlc/extensions/agent-continuity-bridge/pluginctl.py`. Prima annulla la registrazione del controller, poi usa `--remove`. Nessuna azione nativa viene eseguita.
