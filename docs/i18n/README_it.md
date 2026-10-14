# Agentic SDLC — Guida introduttiva

Architettura riutilizzabile basata sul repository per sviluppare software con agenti. Offre ruoli, stato persistente, pianificazione, ripristino e verifiche. Non costruisce automaticamente ogni applicazione né sostituisce le decisioni del responsabile del prodotto.

## Installare in un progetto

Scegli il profilo minimo adeguato. Inizia con una ricognizione in sola lettura; non copiare il Product State degli esempi in un progetto reale. Un nuovo scaffold parte in HOLD / UNTRUSTED_CONTEXT.

```bash
python tools/scaffold_project.py --target "../my-project" --profile SMALL --product-id EXAMPLE --language auto
```

## Ruoli e autorità

Il CLIENT decide il prodotto e autorizza operazioni sensibili; I2 cura strategia e accettazione; I3 realizza sviluppo e ripristino nella campagna; I4 è facoltativo per consulenze limitate e verifiche indipendenti. Quattro ruoli non implicano quattro processi.

## Privacy e feedback mensile

Per impostazione predefinita, ogni nuovo scaffold genera un piccolo rapporto mensile di metadati come artifact GitHub Actions del progetto. Serve a migliorare la struttura e organizzare i problemi. Non viene inviato automaticamente al manutentore. Non contiene codice, conversazioni, nomi di progetti, percorsi, identificatori o credenziali.

Per disabilitare: enabled=false in .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json, eliminare .github/workflows/agentic-sdlc-feedback.yml oppure installare con --no-feedback-workflow.

## Sicurezza e versioni

La versione stabile è 1.1.0. La 1.2 è candidata: le integrazioni reali con Codex Desktop Goal, Gemini, effetti esterni e task multiprogetto richiedono test fisici. CI verde non equivale ad accettazione del prodotto.

## Lingue

L'installazione rileva la lingua del sistema oppure accetta --language it. La documentazione è offline. Il README principale di GitHub è statico: seleziona la lingua tramite i collegamenti.

[FAQ](FAQ_it.md) · [GitHub README](../../README.md)
