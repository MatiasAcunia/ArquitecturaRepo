# 07 — Esempio completo: gestione di un'associazione

ArquitecturaRepo · Manuale completo per l'utente · Edizione v1.4 · Italiano

> Questo capitolo segue un prodotto fittizio dalla prima richiesta all'accettazione. Tutti i soci, le quote e i risultati citati sono esempi didattici. Il [progetto di riferimento dello starter](../../../15_STATEFUL_REFERENCE_AND_TRANSFER.md) verifica alcuni meccanismi portabili, non costituisce prova di un'applicazione reale già consegnata.

## Percorso

1. Il prodotto e i suoi utenti
2. Le domande che cambiano la soluzione
3. Un'installazione senza confusione tra repository
4. Prima capacità: anagrafica soci
5. Dal Planner alla campagna eseguibile
6. Verifiche prima dell'accettazione
7. Seconda capacità: registrare le quote
8. Valutare l'intero percorso
9. Primo ciclo con dati fittizi
10. Gestire un difetto e la sua responsabilità
11. Il secondo ciclo dipende dal primo
12. Esercizio finale di ricostruzione

## 1. Il prodotto e i suoi utenti

Immaginiamo una piccola associazione sportiva che gestisce qualche centinaio di soci. L'amministrazione utilizza fogli di calcolo per nomi, contatti, iscrizioni e quote. Più persone possiedono copie diverse dei file e talvolta si registrano pagamenti duplicati. Il consiglio vuole conoscere gli arretrati; l'operatore desidera una ricerca semplice e affidabile.

Il CLIENT definisce la prima versione: «Voglio un programma locale per gestire soci e quote. Lo userà una persona dell'amministrazione. Per ora niente pagamento online e niente applicazione mobile. La cronologia deve essere conservata anche quando un socio non è più attivo».

Questo brief contiene già alcune decisioni importanti. Il sistema deve essere locale e semplice; la conservazione dei pagamenti è funzionale, non un dettaglio tecnico; servizi bancari esterni sono esclusi. Altre questioni restano aperte: autorizzazioni precise, durata delle informazioni e intervallo dei backup.

La squadra non dovrebbe inventare queste risposte. Il Planner verifica il contesto reale, chiarisce i punti materiali e propone una prima capacità consegnabile. Il cliente non è responsabile della struttura delle tabelle, ma deve poter valutare il risultato che userà.

La qualità ricercata è concreta. Una segreteria deve trovare una persona, modificarne i dati e controllare le quote senza leggere documentazione tecnica. Un'interfaccia complicata può vanificare anche una struttura dati corretta.

## 2. Le domande che cambiano la soluzione

Durante la discovery il Planner fa domande pertinenti:

- Chi può creare o modificare un socio?
- Quali dati sono indispensabili?
- Due persone possono avere lo stesso nome?
- Qual è il significato di disattivazione?
- Le quote precedenti restano consultabili dopo la disattivazione?
- I pagamenti sono registrazioni locali o transazioni vere?
- Quanto deve essere veloce la ricerca?
- Che cosa succede se il computer si guasta?
- Quali funzioni devono essere disponibili nella prima dimostrazione?

Supponiamo che il CLIENT confermi una sola postazione amministrativa, identità stabile per ogni socio, storico dei pagamenti e nessun servizio esterno. Conferma anche che i duplicati devono essere segnalati. L'intervallo di backup resta da definire: viene registrato come decisione aperta, senza trasformarlo in un valore arbitrario.

Il Planner interpreta questi requisiti nel contesto tecnico. Una identità stabile evita di collegare quote a persone sbagliate dopo una modifica del nome. La storicità suggerisce che disattivare non debba cancellare automaticamente le registrazioni. Il lavoro offline influenza la scelta della persistenza e del deployment.

Queste sono conseguenze tecniche delle decisioni confermate. Le parti che dipendono da preferenze o autorizzazioni ulteriori devono essere riportate al CLIENT. L'obiettivo non è fargli scegliere una query SQL, ma evitare che la soluzione decida silenziosamente una regola di prodotto.

## 3. Un'installazione senza confusione tra repository

La squadra dispone del repository pubblico dello starter ArquitecturaRepo e di un repository separato gestione-soci. Il primo contiene protocolli, strumenti e documentazione; il secondo è il prodotto da realizzare. È essenziale non chiedere al coding agent di aggiungere i moduli del gestionale direttamente al repository pubblico del framework.

Lo starter è stato identificato tramite la [release v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0) e il checksum del pacchetto. Il ramo main può contenere libri e guide pubblicati più tardi, che non facevano parte dello ZIP iniziale.

Dato che l'applicazione conserva dati persistenti, il profilo STATEFUL è una scelta ragionevole. Nel terminale PowerShell del framework, per un progetto nuovo non ancora governato:

    & "python" "tools\scaffold_project.py" --target "..\gestione-soci" --profile "STATEFUL" --product-id "GESTIONE_SOCI" --objective "Anagrafica e quote dell'associazione" --language "it" --no-feedback-workflow

Il comando è un esempio, non un'operazione già eseguita. Il percorso deve essere controllato prima della scrittura. Se gestione-soci possiede già una struttura .agentic-sdlc/ con stato valido, si segue la [verifica in sola lettura](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) invece di sovrascriverla.

Dopo l'installazione, nella cartella dell'applicazione:

    & "python" -m pip install -r ".agentic-sdlc\requirements-validation.txt"
    & "python" ".agentic-sdlc\tools\project_status.py" --control-root ".agentic-sdlc"
    & "python" ".agentic-sdlc\tools\discover_project.py" --project-root "."
    & "python" ".agentic-sdlc\tools\reconstruct_context.py" --root ".agentic-sdlc"

HOLD / UNTRUSTED_CONTEXT può apparire correttamente. Il framework ha creato la struttura ma non ha ancora adottato le informazioni reali del prodotto. Il Planner raccoglie codice, dati, decisioni e baseline tecnica, poi promuove uno stato coerente tramite il processo di adozione.

## 4. Prima capacità: anagrafica soci

Il primo charter riguarda una capacità circoscritta e utile: creare un socio, ritrovarlo, aggiornare le informazioni e disattivarlo senza perdere la sua identità storica. Una prima capacità così definita permette di testare un flusso reale prima di aggiungere quote e report.

I requisiti osservabili potrebbero essere:

| Operazione | Risultato atteso | Caso limite |
| --- | --- | --- |
| Creazione | Socio memorizzato con ID stabile | Campi obbligatori mancanti |
| Ricerca | Persona ritrovata per nome o codice | Omonimi e caratteri speciali |
| Modifica | Dati aggiornati anche dopo riavvio | Conflitti di aggiornamento pertinenti |
| Disattivazione | Stato inattivo senza cancellare collegamenti storici | Dati già associati a pagamenti |
| Errore | Messaggio chiaro e operazione non distruttiva | Salvataggio interrotto o duplicato |

Si tratta di criteri proposti, non di test già eseguiti. Il CLIENT conferma il comportamento e il Planner collega le condizioni alla baseline. Engineering sceglie componenti, schema, validazione e strategia di persistenza.

Una implementazione potrebbe separare accesso ai dati, logica dei soci e interfaccia, ma il framework non obbliga a una struttura di classi unica. L'importante è che le responsabilità siano coerenti e che il comportamento possa essere verificato e ripreso.

I3 deve testare sia il caso normale sia le situazioni che cambiano significato: due soci con lo stesso nome non sono necessariamente duplicati; un codice già utilizzato potrebbe non essere valido; una disattivazione non dovrebbe eliminare quote storiche. Questi casi derivano direttamente dall'intenzione di prodotto.

## 5. Dal Planner alla campagna eseguibile

Il Planner considera il percorso end-to-end, le dipendenze, i rischi sui dati e le autorizzazioni. Svolge la propria analisi strategica e una revisione avversariale distinta quando l'importanza del charter lo richiede. La revisione cerca ipotesi fragili: sicurezza insufficiente, ambiguità sulla cancellazione, mancanza di recupero o gate non adeguati.

Il charter descrive risultato, confini, input, interfacce, responsabilità e criteri. Non deve trasformarsi in una lunga serie di istruzioni su ogni funzione interna. Una consegna eseguibile potrebbe essere:

> Obiettivo: rendere utilizzabile l'anagrafica soci locale. Stato iniziale: repository e requisiti correnti verificati. Confini: solo dati sintetici nei test, nessun servizio esterno, nessun deployment pubblico, nessuna modifica non autorizzata a pagamenti reali. Verifiche: unità, integrazione, database, semantica e prova effettiva dell'interfaccia come controlli distinti. Risultato terminale: candidato identificato e rapporto con prove e limiti.

Una volta autorizzato, I3 possiede la realizzazione tecnica. Può scegliere l'ordine delle attività, correggere bug, ripetere i test e richiedere una revisione indipendente. Non deve ritornare al Planner per ogni dettaglio di implementazione. La separazione evita che il CLIENT diventi il coordinatore dei tentativi tecnici.

Il controller opzionale dello starter può aiutare a mantenere alcuni stati, ma non certifica automaticamente l'esecuzione di agenti remoti o l'accettazione del prodotto. Le prove devono provenire dalle operazioni realmente compiute nell'applicazione.

## 6. Verifiche prima dell'accettazione

La prima verifica riguarda i componenti singoli: controllo dei dati obbligatori, creazione di identificatori, cambio di stato e gestione degli errori. Seguono test di integrazione che percorrono interfaccia, logica e database, includendo la rilettura di informazioni dopo un riavvio.

Il gate DB/currentness verifica che schema e migrazioni corrispondano al candidato attuale. Il gate semantico cerca errori di significato: un socio disattivato non deve diventare una persona inesistente se la cronologia richiede ancora il riferimento.

La prova fisica avvia l'applicazione nel contesto previsto. Un modulo importato in un test Python non è la stessa cosa di un programma che l'amministrativo riesce a utilizzare. La verifica percettiva guarda leggibilità, passaggi, messaggi di errore e comprensione dell'operazione.

Supponiamo che i dati si salvino correttamente ma l'utente non riceva alcuna conferma visibile. Il risultato potrebbe essere tecnicamente valido e comunque produrre doppi click o errori d'uso. Se il charter prevedeva una interazione comprensibile, I3 corregge il difetto nella stessa campagna.

Le prove devono riferirsi al candidato esatto. Se il codice cambia dopo il review, si ripetono i controlli influenzati dalla modifica. Non basta riutilizzare una pagina con la parola PASS.

## 7. Seconda capacità: registrare le quote

Una volta verificata l'identità stabile dei soci, il Planner può proporre la gestione delle quote. La nuova capacità dipende dalla precedente: ogni pagamento locale deve appartenere a una persona corretta e rimanere collegato anche in caso di modifica del nome o dello stato.

Il CLIENT definisce importi, scadenze, eventuali pagamenti parziali, correzioni consentite e responsabilità di chi registra le quote. Il team tecnico stabilisce lo schema, la logica delle transazioni e le verifiche necessarie. Le banche e i servizi di pagamento veri restano esclusi dalla prima versione.

Un rischio importante è la duplicazione. Se l'operatore clicca due volte o si verifica un retry, non deve comparire automaticamente un doppio pagamento. La capacità richiede quindi un comportamento idempotente o comunque una protezione equivalente, progettata e provata da Engineering.

La disattivazione di un socio non cancella i suoi pagamenti passati. Questa regola collega il secondo charter al primo e mostra perché le capacità non sono semplici cartelle isolate. Quando una funzione precedente cambia, i suoi consumatori devono essere rivalutati in modo proporzionato.

Una volta implementata la quota, l'amministrativo deve poterla registrare, rivedere e correggere secondo regole esplicite. Un report degli arretrati può venire dopo, quando si conosce il significato esatto di pagato, scaduto e parziale.

## 8. Valutare l'intero percorso

La dimostrazione più convincente unisce le capacità: creare un socio, cercarlo, registrare una quota, ritrovare lo storico, disattivare la persona e verificare che i pagamenti restino consultabili. Questo percorso rivela problemi di integrazione che test isolati potrebbero non vedere.

Il Planner controlla il rapporto tra requisiti e risultato. La base tecnica verifica integrità dei dati, autorizzazioni e ripresa. Il CLIENT prova ciò che realmente farà ogni giorno. Una schermata gradevole non sostituisce la sicurezza; una transazione corretta non sostituisce la comprensione umana.

Il progetto deve inoltre conoscere i propri limiti. Un sistema locale provato con qualche centinaio di soci non è automaticamente pronto per migliaia di accessi concorrenti via Internet. Una quota registrata in un database non è una transazione bancaria riuscita.

L'accettazione deve nominare il candidato, l'ambiente e i gate superati. Le limitazioni restano visibili. In questo modo la prossima modifica potrà partire da un fatto verificabile invece che da una promessa generica.

## 9. Primo ciclo con dati fittizi

Create tre persone sintetiche: Socio A attivo, Socio B con un cognome uguale a quello di A e Socio C destinato alla disattivazione. Inserite dati corretti e dati incompleti. Cercate per nome e codice, modificate un contatto e verificate il risultato dopo aver chiuso e riaperto il programma.

Provate anche caratteri speciali e omonimi. Se un test fallisce, preservate il caso riproducibile e lasciate che I3 corregga la causa nel charter. Non è necessario riscrivere la strategia di prodotto perché la normalizzazione di una stringa era sbagliata.

Usate un database di prova e, se previsto dalla baseline, esercitate una procedura di recupero. Controllate che i dati siano davvero persistenti. Un test che si limita a restituire un oggetto in memoria non prova il comportamento del prodotto dopo il riavvio.

Prima dell'accettazione finale, una persona prova i passaggi. Se non riesce a interpretare il pulsante di disattivazione o non capisce un errore, il difetto va registrato con riferimento al candidato. La qualità dell'interazione è parte del risultato.

## 10. Gestire un difetto e la sua responsabilità

Immaginiamo tre problemi. Primo: la ricerca fallisce con le lettere accentate. Si tratta normalmente di un difetto tecnico nel comportamento già concordato; I3 corregge. Secondo: l'associazione vuole improvvisamente iscrizioni pubbliche via Internet. È un cambiamento di prodotto che richiede nuova valutazione strategica. Terzo: dopo un'interruzione non si sa se una quota sia stata già salvata. È una questione di stato e idempotenza: ulteriori scritture dipendenti restano sospese finché non viene chiarita.

Questa classificazione determina il lavoro corretto. Un bug non comporta automaticamente un nuovo Goal. Un requisito completamente nuovo non va nascosto in un refactoring. Un'informazione tecnica sconosciuta non deve essere inventata per rendere verde il rapporto.

Se I3 ha già corretto più volte lo stesso tipo di errore, deve rivedere l'intero sottosistema e richiedere una verifica indipendente. Il problema potrebbe essere nella strategia di confronto, nella persistenza o nei test stessi. Fare una nuova microcampagna ogni giorno non risolve la causa.

Il CLIENT interviene quando l'esito visibile o l'autorità riservata richiedono una decisione. Non deve coordinare le prove di ogni fix né fornire una soluzione tecnica pronta.

## 11. Il secondo ciclo dipende dal primo

La funzione quote si appoggia all'identità dei soci già accettata. Il controller verifica che la base corrente corrisponda a quella su cui si vuole costruire. Se la precedente capacità è stata modificata, può essere necessaria una prova di integrazione prima di procedere.

Si registra una quota sintetica per Socio A. Il programma viene riavviato e la quota resta visibile. La stessa richiesta viene ripetuta per verificare che il risultato non venga duplicato. Socio C viene disattivato e lo storico resta consultabile secondo il requisito.

Un revisore controlla i casi difficili: importo invalido, registrazione ripetuta, errore di salvataggio, autorizzazione e collegamento al socio corretto. Il CLIENT prova il percorso end-to-end. Solo con evidenze adeguate e correntezza del candidato la capacità può essere accettata.

Il report successivo del consiglio dipenderà dalla definizione di arretrato. Una query che somma correttamente un insieme di dati può comunque dare un risultato non utile se la regola economica è ambigua. È il motivo per cui la corretta collaborazione fra CLIENT, Planner e I3 conta più della sola velocità di generazione del codice.

## 12. Esercizio finale di ricostruzione

Per verificare che il framework abbia realmente migliorato la continuità, immaginate di consegnare il repository a una nuova sessione senza il vecchio dialogo. Questa sessione deve poter rispondere:

1. Qual è l'obiettivo del gestionale e chi lo usa?
2. Quali requisiti sono stati confermati e quali restano aperti?
3. Quale versione del codice e del database è corrente?
4. Quali capacità sono state realmente accettate?
5. Quali test e prove umane sostengono l'accettazione?
6. Quali autorizzazioni esterne mancano?
7. Quale campagna è aperta e chi può proseguire?
8. Qual è la prossima azione consentita e quale non lo è?

Se la risposta richiede una ricostruzione manuale di tutta la chat, cercate la fonte mancante: requisiti, currentness, rapporto di review, proprietario del dato o prossimo passo. Correggete la superficie canonica, non soltanto il riepilogo.

Lo scopo non è convincere l'utente con una quantità enorme di file. È rendergli possibile concentrarsi sulle scelte di prodotto, mentre Engineering può sviluppare, verificare, integrare e riprendere il lavoro in modo affidabile.

## Fonti e limiti

- [Riferimento stateful e trasferimento](../../../15_STATEFUL_REFERENCE_AND_TRANSFER.md)
- [Installazione pubblica v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Attachment di progetti governati](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Discovery e baseline](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Adozione](../../../16_TRANSFER_ADOPTION.md)
- [Standard del charter](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Gates ed evidenze](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Currentness](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md)

I dati e gli esiti dell'associazione sono fittizi. Questa dimostrazione non autorizza operazioni reali né afferma che esista un gestionale già prodotto.
