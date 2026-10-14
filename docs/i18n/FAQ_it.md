# Agentic SDLC FAQ (it)

[IT guide](README_it.md) · [Main README](../../README.md)

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

Non ancora. La v1.2 include controlli opzionali di Goal e Plan, ma l'integrazione reale per ogni invocazione resta da dimostrare.

### 7. Gemini è obbligatorio o a pagamento per impostazione predefinita?

No. Il percorso I4 resta disattivato finché consenso, chiave, quota e privacy non sono verificati. Nessun invio predefinito di codice privato.

### 8. Può riavviare o eliminare le chat Codex?

Non da solo. Codex Daily Control 2.0.2 è un riferimento separato; l'adattatore host non è ancora accettato nella v1.2.

### 9. Quale feedback viene attivato?

Un piccolo rapporto mensile di metadati negli artifacts GitHub Actions del proprio progetto. Aiuta a migliorare lo starter, senza invio esterno automatico.

### 10. Quali dati vengono esclusi?

Codice, conversazioni, nomi di progetti/repository, percorsi, credenziali, identificatori personali, requisiti, SHA e testo libero non controllato.

### 11. Come cambio lingua o disabilito il feedback?

Usa --language auto|en|es|pt|fr|de|it|ja|zh. Per disattivare: enabled=false o --no-feedback-workflow. Il README GitHub è statico.

### 12. Che cosa è testato e come segnalo un errore?

1.1.0 è stabile; v1.2 resta candidata fino a test fisici indipendenti. Apri una Issue con passaggi riproducibili e log senza segreti. Il materiale originale usa MIT.

### 13. Posso combinare modalità asincrone, team e IA non dedicata alla programmazione?

Sì, come dimensioni configurabili. L'esecuzione richiede host, autorizzazioni, recupero e verifiche reali. SMALL resta leggero. I2 conserva requisiti e scelte tecniche nel repository canonico; commit e branch inutili sono vietati. Il feedback esterno minimo sarà disattivabile ma non può partire senza un destinatario verificato.

---

[IT guide](README_it.md)
