# Agentic SDLC FAQ (it)

[IT guide](README_it.md) · [Mini guida v1.4](MINI_GUIDE_it.md) · [Main README](../../README.md)

### 1. Cos'è Agentic SDLC?

Un'architettura riutilizzabile per organizzare lo sviluppo software con agenti. Non è un generatore autonomo di qualunque applicazione.

### 2. Da dove inizio?

Fai un fork o esamina il repository, inizia con ricognizione in sola lettura, scegli il profilo minimo e segui il prompt di installazione. Il nuovo scaffold parte in HOLD.

### 3. Posso adottarlo in un repository esistente?

Sì. Ricostruisci prima codice, dati e autorizzazioni reali. Non sovrascrivere i file dell'applicazione né trattare gli esempi come stato canonico.

### 4. Quattro ruoli richiedono quattro modelli?

No. CLIENT, Planner I2, Campaign Lead I3 e specialisti I4 descrivono responsabilità, non un numero fisso di processi.

### 5. Chi approva modifiche sensibili?

Il CLIENT mantiene decisioni di prodotto, accettazione soggettiva, pubblicazione, costi e dati sensibili. I3 non può inventare permessi.

### 6. Goals e Codex Desktop sono già integrati?

Non automaticamente. La v1.4 include controlli portabili Goal/Plan e di autorità, ma l'integrazione nativa con Codex Desktop/Goals per ogni invocazione richiede verifiche fisiche separate.

### 7. Gemini è obbligatorio o a pagamento per impostazione predefinita?

No. Il percorso I4 resta disattivato finché consenso, chiave, quota e privacy non sono verificati. Nessun invio predefinito di codice privato.

### 8. Può riavviare o eliminare le chat Codex?

No. Lo starter non riavvia, gestisce né elimina chat native di Codex. Ogni adattatore host richiede autorizzazioni e prove indipendenti; la v1.4 non certifica questo ciclo di vita.

### 9. Quale feedback viene attivato?

Un piccolo rapporto mensile di metadati negli artifacts GitHub Actions del proprio progetto. Aiuta a migliorare lo starter, senza invio esterno automatico.

### 10. Quali dati vengono esclusi?

Codice, conversazioni, nomi di progetti/repository, percorsi, credenziali, identificatori personali, requisiti, SHA e testo libero non controllato.

### 11. Come cambio lingua o disabilito il feedback?

Usa --language auto|en|es|pt|fr|de|it|ja|zh. Per disattivare tutti i report imposta enabled=false; --no-feedback-workflow disabilita soltanto la programmazione. Il README GitHub è statico.

### 12. Che cosa è testato e come segnalo un errore?

**La v1.4.0 è pubblicata** con [tag versionato, ZIP portabile e checksum SHA-256](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0); verifica i file scaricati. Il ramo `main` può contenere documentazione più recente, mentre v1.3.0 rimane disponibile come release precedente. I test portabili Linux/Windows non certificano host nativi per agenti né l'usabilità da parte di terzi. Apri una Issue con passaggi riproducibili e log senza segreti. Il materiale originale usa MIT.

### 13. Posso combinare modalità asincrone, team e IA non dedicata alla programmazione?

Sì, come dimensioni configurabili. L'esecuzione richiede host, autorizzazioni, recupero e verifiche reali. SMALL resta leggero. I2 conserva requisiti e scelte tecniche nel repository canonico; commit e branch inutili sono vietati. Il feedback esterno minimo sarà disattivabile ma non può partire senza un destinatario verificato.

---

[IT guide](README_it.md) · [Mini guida v1.4](MINI_GUIDE_it.md)
