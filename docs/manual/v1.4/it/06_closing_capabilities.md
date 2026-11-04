# 06 — Accettazione e chiusura delle capacità

ArquitecturaRepo · Manuale completo per l'utente · Edizione v1.4 · Italiano

> Una dichiarazione di PASS non basta a concludere una capacità. Serve un candidato esatto, con evidenze appropriate e l'approvazione delle autorità corrette. Questo capitolo segue il [ciclo di vita delle capacità](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md) e l'[integrità della revisione terminale](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md).

## Argomenti

1. Una capacità è un risultato di prodotto
2. Cinque componenti della chiusura
3. Identificare esattamente il candidato
4. Lacune di prova senza nuove campagne artificiali
5. Accettare, continuare o cambiare obiettivo
6. Revisioni periodiche e regola di arresto
7. Un rapporto di chiusura verificabile
8. Un rifiuto che non obbliga a ricominciare
9. Software utilizzabile e test dello starter
10. Sapere quando concludere la sessione

## 1. Una capacità è un risultato di prodotto

Un endpoint, una tabella e un modulo software sono parti della soluzione. Una capacità è ciò che l'utente può fare grazie a quelle parti. Nell'applicazione dell'associazione, per esempio, la capacità «registrare una quota e ritrovarla nello storico» attraversa interfaccia, validazione, permessi e persistenza.

Il codice può compilare senza essere utile. Una tabella può esistere senza alcuna schermata per consultarne i dati. Un'operazione può funzionare una volta ma duplicare un pagamento se viene ripetuta. La conclusione della capacità deve quindi riguardare il percorso concordato e i suoi principali rischi, non semplicemente la presenza di file.

L'ambito resta importante. Se la prima versione non prevede pagamenti online, il team non deve bloccare indefinitamente la quota locale perché non è stata integrata una banca. Allo stesso tempo, non può sostenere che la funzione locale sia pronta se perde i dati al riavvio o consente a utenti non autorizzati di alterare le registrazioni.

Il requisito di prodotto chiarisce il risultato desiderato. Il charter stabilisce ciò che è autorizzato. Le prove dimostrano che un candidato specifico lo realizza. L'accettazione corretta collega tutte queste parti senza confonderne i proprietari.

## 2. Cinque componenti della chiusura

Un buon rapporto terminale include cinque elementi. Il primo è la capacità e la sua origine: requisito confermato e charter valido. Il secondo è l'identità del candidato: codice, configurazione e dati pertinenti. Il terzo è l'insieme delle verifiche tecniche, semantiche e fisiche richieste. Il quarto è la revisione indipendente e, quando serve, la valutazione umana. Il quinto è la decisione corrente con rischi e prossima azione.

Non sono cinque documenti necessariamente distinti. Un progetto piccolo può usare riferimenti brevi a fonti già esistenti. L'obiettivo non è moltiplicare i PDF o le Issue, ma permettere a una persona nuova di capire esattamente che cosa è stato approvato.

Ogni prova ha una portata. Il test di una funzione copre certe condizioni; un'integrazione prova il passaggio tra componenti; un controllo del database valuta la persistenza; una sessione con l'utente osserva la comprensibilità. Un singolo gate non deve assorbire automaticamente gli altri.

Se manca una verifica importante, il rapporto deve dirlo. Un candidato verificato soltanto in locale con dati sintetici può essere un buon prototipo, ma non si dovrebbe presentarlo come sistema di produzione collaudato. L'onestà dell'affermazione è parte della qualità del prodotto.

## 3. Identificare esattamente il candidato

Il candidato sottoposto a revisione non è «l'ultima versione» in senso generico. Può essere un commit preciso, una configurazione determinata, una versione del database e un insieme di artefatti correlati. Se il branch cambia durante o dopo la prova, bisogna riconciliare quali risultati restino applicabili.

Il review freeze serve a proteggere questa identità. Un revisore indipendente esamina lo stesso contenuto che l'esecutore propone di accettare. Se una modifica importante viene effettuata dopo il review, il candidato cambia e le verifiche interessate vanno ripetute.

Immaginiamo che la funzione di quota sia provata sul commit A. Dopo il test, I3 modifica il modo di gestire la doppia registrazione nel commit B. Il vecchio risultato può restare una fonte storica, ma non certifica automaticamente il nuovo comportamento. Serve almeno una verifica adeguata della logica cambiata e delle sue interazioni.

Neppure il solo Git dimostra che il database corrente corrisponda alle migrazioni del codice. Se la capacità dipende da dati persistenti, la relazione va controllata. Un candidato può essere formalmente identificato e comunque non avere evidenza sufficiente per un gate di currentness.

La responsabilità di chi integra il commit e l'identità dell'agente che ha eseguito il lavoro sono concetti diversi. I progetti che richiedono tracciabilità di esecuzione devono conservarla sulle superfici pertinenti, senza desumerla dalla sola cronologia Git.

## 4. Lacune di prova senza nuove campagne artificiali

Un difetto ordinario o un test mancante, già compreso nel charter, torna a I3. Il controller corregge, aggiunge le verifiche e presenta un candidato aggiornato. Non serve una nuova campagna strategica ogni volta che un revisore trova un problema.

Se la funzione quote supera i test unitari ma non è stata avviata nell'applicazione reale, manca il gate fisico. I3 esegue il flusso e documenta il risultato nella stessa campagna. Se emerge un errore di persistenza, lo corregge e ripete i test pertinenti. Questo è lavoro operativo normale.

Se lo stesso sottosistema fallisce più volte, la risposta deve diventare sistemica. Non basta correggere una eccezione per iterazione. I3 esamina l'intero percorso, i dati, gli errori e la concorrenza, poi richiede una revisione indipendente più ampia prima di un nuovo rapporto terminale.

Una vera invalidazione del charter è diversa. Se il CLIENT decide improvvisamente che i pagamenti devono passare da un provider bancario reale, cambiano responsabilità, sicurezza, costi e requisiti. Questo richiede una decisione di prodotto e una valutazione strategica. Non è una semplice mancanza di test.

## 5. Accettare, continuare o cambiare obiettivo

Le conclusioni possibili possono essere raggruppate in tre categorie. **Accettare** se il candidato corrente soddisfa l'intenzione confermata e i gate necessari sono dimostrati. **Continuare** se restano difetti o prove da completare all'interno dei limiti autorizzati. **Cambiare la direzione** se emerge una nuova esigenza o un rischio materiale incompatibile con il charter.

Queste strade producono azioni diverse. Accettare significa aggiornare lo stato canonico e rendere chiaro che cosa è stato effettivamente ottenuto. Continuare significa restituire falsificatori specifici a I3. Cambiare la direzione significa coinvolgere il CLIENT e il Planner per chiarire la nuova capacità e le sue conseguenze.

Un rifiuto tecnico ben formulato descrive un problema riproducibile. «In due richieste simultanee la quota viene salvata due volte; il test di integrazione sul candidato mostra il duplicato» è utile. «Non mi convince, ricominciamo» non identifica una causa; può però giustificare una prova umana se la difficoltà riguarda davvero l'esperienza.

Un'accettazione con limitazioni deve riportarle. «Funziona in locale con dati sintetici, non è pubblicato» è una conclusione onesta. «Pronto per qualunque ambiente» non segue da quelle prove. È meglio un confine chiaro che un'etichetta apparentemente definitiva ma ingannevole.

## 6. Revisioni periodiche e regola di arresto

La qualità richiede rigore, non perfezionismo senza fine. Se tutti i gate realmente applicabili sono stati soddisfatti e non esistono falsificatori materiali, continuare a cercare microdifetti teorici può consumare tempo senza migliorare il prodotto.

Il Planner può eseguire verifiche periodiche della direzione, delle dipendenze e dei rischi. Questo non significa ripetere una nuova analisi strategica completa ogni volta che I3 incontra un test fallito. I passaggi strategici principali hanno uno scopo distinto dalla normale iterazione tecnica.

Dopo più ritorni dello stesso tipo, la strategia operativa deve cambiare: hardening completo del sottosistema, revisione indipendente e nuovo candidato complessivo. Continuare ad accumulare correzioni marginali senza esaminare la causa non è una dimostrazione di qualità.

Misurate il progresso nelle capacità utilizzabili, nei gate superati e nei rischi effettivamente ridotti. Più commit, più documenti o più ore di esecuzione possono essere strumenti utili, ma non sono indicatori sufficienti di successo.

Il CLIENT deve poter valutare se la funzione risolve il problema reale. Un test può essere perfetto nel proprio ambito ma non rilevare che l'utente non capisca un pulsante o che il report risponda alla domanda sbagliata. La verifica percettiva ha un proprietario e uno scopo diversi.

## 7. Un rapporto di chiusura verificabile

Per l'esempio delle quote, un riepilogo potrebbe essere:

| Campo | Evidenza attesa |
| --- | --- |
| Capacità | Registrare una quota locale e ritrovarla |
| Confine | Nessun pagamento bancario esterno |
| Candidato | Commit, configurazione e database esatti |
| Unit | Importo valido, campi obbligatori e arrotondamenti |
| Integration | Modulo, servizio e persistenza insieme |
| DB/currentness | Migrazione applicata al database verificato |
| Semantic | Nessuna doppia registrazione e corretto storico |
| Physical | Applicazione avviata nell'ambiente previsto |
| Perceptual | Utente capace di completare il percorso |
| Release | Pacchetto e autorizzazioni di pubblicazione distinti |
| Rischi | Solo quelli realmente rimasti, con proprietario |

Le righe sono un modello didattico, non l'affermazione che i test siano stati eseguiti. In un rapporto reale ogni gate riporta la prova effettiva e il candidato a cui si riferisce. Non basta scrivere PASS nella casella.

Un controllo esterno può decidere che una parte dei gate non si applica a una capacità particolare, ma la motivazione deve essere coerente con il rischio. Per esempio, una modifica a un testo non richiede la stessa verifica di un nuovo schema di pagamenti. Non bisogna però nascondere una lacuna significativa dietro una formula generica.

La chiusura include la prossima azione consentita. Dopo la corretta registrazione delle quote, il progetto potrebbe passare a un rapporto mensile. Se invece il database resta incerto, il passo corretto è chiarirne lo stato prima di nuove scritture.

## 8. Un rifiuto che non obbliga a ricominciare

Un revisore scopre che il doppio click su «Salva quota» crea due record. Il charter richiedeva una singola registrazione per operazione. Il difetto è quindi dentro il perimetro autorizzato.

I3 analizza eventi UI, richieste, gestione dei retry, transazioni e chiavi di idempotenza. Dopo la correzione crea casi di test che riproducono il problema e dimostrano che la seconda richiesta non provoca un nuovo effetto indebito. Il revisore indipendente esamina il candidato aggiornato.

Il Planner riceve il rapporto consolidato quando una decisione strategica è matura. Non deve formulare un nuovo charter per ogni esperimento sulla stessa causa. Il CLIENT non deve scegliere se usare una transazione serializzabile o un indice unico, a meno che una conseguenza di prodotto non richieda la sua opinione.

Se durante l'analisi emerge una richiesta di riscuotere denaro reale tramite un provider, si tratta di una nuova questione. La sua autorizzazione e il relativo rischio non possono essere dedotti dal charter delle quote registrate localmente.

## 9. Software utilizzabile e test dello starter

La CI di ArquitecturaRepo può verificare correttamente il pacchetto e i suoi contratti. Questi controlli non certificano tutte le future applicazioni sviluppate con esso. Un controller che recupera uno stato sintetico non prova che un gestionale reale sopravviva alla perdita di un disco.

Anche un'applicazione presentata in un video può sembrare pronta pur non avendo prove di persistenza o autorizzazione. Ogni evidenza deve essere valutata per ciò che mostra. La coerenza delle affermazioni è più importante della quantità di screenshot o rapporti.

Una capacità è davvero utile quando il percorso dell'utente funziona nel contesto previsto e i rischi proporzionati sono stati affrontati. Il framework serve a rendere riconoscibile questo risultato, non a sostituire la verifica.

## 10. Sapere quando concludere la sessione

Una campagna può essere chiusa dopo un'accettazione corretta e la registrazione del suo risultato corrente. Una sessione quotidiana può terminare anche con la campagna ancora aperta, purché siano disponibili checkpoint, evidenze e azione successiva.

Il CLIENT non deve essere continuamente presente per gestire test e correzioni. Se manca una vera decisione di prodotto, si ferma soltanto la parte che ne dipende. Il silenzio dell'utente non significa autorizzazione a spendere o pubblicare, ma nemmeno un ordine implicito di sospendere ogni altra attività già permessa.

Una nuova sessione dovrebbe poter ricostruire la capacità accettata, il candidato, le verifiche, i problemi rimasti e l'autorità del prossimo passo. Se ciò riesce, il sistema ha preservato un risultato oltre la singola conversazione.

**Segue:** capitolo 07, Esempio completo di associazione.

## Fonti e limiti

- [Ciclo di vita ed evidenze](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Integrità della revisione](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Charter di campagna](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Execution Team OS](../../../../protocols/EXECUTION_TEAM_OS.md)
- [Gate della release](../../../17_V1_RELEASE_GATES.md)
- [Ricostruzione del contesto](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md)

La tabella è un modello e non sostituisce le prove reali del progetto che si intende consegnare.
