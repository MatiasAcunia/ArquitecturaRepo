# Agentic SDLC — Guida introduttiva

[Mini guida v1.4](MINI_GUIDE_it.md) · [FAQ](FAQ_it.md)

Il [manuale completo in otto capitoli](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/ES/README.md) è disponibile **nel repository sorgente, solo in spagnolo**, come **edizione storica v1.3**; non viene copiato nel progetto installato. Questa pagina è un'introduzione breve alla v1.4, non una traduzione completa; per i comandi aggiornati consulta la [guida all'installazione v1.4](../46_V1_4_PUBLIC_START_AND_SUPPORT.md).

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

Per fermare tutti i report, imposta enabled=false in .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json. Eliminare .github/workflows/agentic-sdlc-feedback.yml o usare --no-feedback-workflow disabilita solo la pianificazione, non il generatore locale.

## Sicurezza e versioni

**La v1.4.0 è stata pubblicata** come [release con versione definita, ZIP portabile e checksum SHA-256](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0). Verifica i file scaricati prima dell'installazione; il ramo `main` può contenere modifiche successive alla documentazione e non è l'artefatto pubblicato. La release precedente v1.3.0 rimane disponibile. Per progetti nuovi o non ancora governati, segui la [guida al primo utilizzo v1.4](../46_V1_4_PUBLIC_START_AND_SUPPORT.md); per progetti già governati è necessaria una [verifica in sola lettura](../32_EXISTING_GOVERNED_ATTACHMENT.md), senza sovrascrivere lo stato. La CI portabile non certifica l'esecuzione nativa di Codex Desktop, provider IA esterni o effetti reali.

## Lingue

L'installazione rileva la lingua del sistema oppure accetta --language it. La documentazione è offline. Il README principale di GitHub è statico: seleziona la lingua tramite i collegamenti.

[Mini guida v1.4](MINI_GUIDE_it.md) · [FAQ](FAQ_it.md) · [GitHub README](../../README.md)
