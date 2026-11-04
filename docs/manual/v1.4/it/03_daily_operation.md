# 03 — Lavoro quotidiano e continuità dell'esecuzione

ArquitecturaRepo · Manuale completo per l'utente · Edizione v1.4 · Italiano

> Dopo l'adozione e l'autorizzazione di una campagna, il lavoro deve restare coerente anche quando cambiano persone, sessioni o strumenti. Questo capitolo segue l'[Execution Team OS](../../../../protocols/EXECUTION_TEAM_OS.md), il [contratto del charter](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md) e le [regole di currentness](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md).

## Argomenti

1. Cominciare una giornata senza ricominciare il progetto
2. Collegare richiesta e capacità concreta
3. Il lavoro operativo di I3
4. Limiti delle autorizzazioni esterne
5. Leggere correttamente un rapporto tecnico
6. Git e identità del lavoro
7. Cinque domande utili ogni giorno
8. Esempio di una giornata completa
9. Come formulare una consegna al controller
10. Interpretare gli stati operativi
11. Revisione, correzioni e decisioni
12. Lasciare un contesto recuperabile

## 1. Cominciare una giornata senza ricominciare il progetto

Il primo passo non dovrebbe essere rileggere migliaia di messaggi. Chi riprende un progetto apre il repository effettivo, controlla la versione corrente e ricostruisce l'autorità di lavoro: requisiti attivi, Product State, campagna, checkpoint, prove disponibili e azione successiva permessa.

Una conversazione precedente può essere utile, ma non è automaticamente attuale. Se un vecchio rapporto dichiara completato un modulo, il nuovo esecutore deve verificare se quel risultato si riferisce al codice che esiste ora. Se la banca dati è cambiata, la sola identità Git non prova che la migrazione sia ancora valida.

La ricerca deve essere proporzionata. Con un checkout affidabile si possono leggere le differenze recenti e i riferimenti canonici, senza riclonare tutto. Uno stato locale modificato va preservato finché non si conoscono proprietario e significato delle modifiche. Anche i worktree temporanei e gli artefatti pesanti devono avere uno scopo preciso.

Un buon riepilogo operativo contiene pochi fatti controllabili: «La campagna attiva riguarda la ricerca soci; il candidato esatto è identificato; il gate aperto è l'integrazione con il database; l'azione permessa è eseguire test e correzioni nello stesso charter; non è autorizzata la pubblicazione». Un nuovo agente dovrebbe poter verificare ciascuna parte.

## 2. Collegare richiesta e capacità concreta

Il CLIENT può chiedere «voglio trovare facilmente i soci». Per definire una capacità utile, I2 chiarisce che cosa significa facilmente: ricerca per nome o numero, gestione degli omonimi, persone disattivate, errori e dimensione dei dati. Non deve necessariamente decidere da solo ogni dettaglio; può fare domande di prodotto mirate.

Il risultato non coincide con un singolo componente tecnico. Un endpoint di ricerca può funzionare isolatamente ma restare inutilizzabile se la schermata non mostra correttamente i risultati. Una capacità end-to-end include l'ingresso dell'utente, le verifiche di autorizzazione, la lettura dei dati e una risposta comprensibile.

Il charter descrive questo risultato e i confini del lavoro. Non impone in anticipo tutte le classi, le query o i commit. La decomposizione tecnica spetta a I3 dopo l'autorizzazione. In questo modo la campagna può assorbire normali difficoltà di implementazione senza ritornare continuamente alla pianificazione.

Non è necessario costruire una ricerca universale per soddisfare un bisogno limitato. Se la prima versione richiede unicamente il numero di socio, tale limite può essere esplicito. La qualità dipende dalla corrispondenza tra comportamento concordato e risultato reale, non dal numero massimo di funzionalità possibili.

## 3. Il lavoro operativo di I3

I3 gestisce implementazione, debugging, integrazione, verifiche, eventuali migrazioni interne, ripresa dopo un'interruzione e cicli di revisione già compresi nel charter. Può organizzare specialisti I4 o eseguire direttamente compiti tecnici in un progetto piccolo. La responsabilità resta continua fino a un candidato realmente verificabile.

Supponiamo che la ricerca dei soci non funzioni con lettere accentate. Questo è normalmente un difetto tecnico rispetto a un requisito già confermato. Il controller esamina codifica, normalizzazione, dati e query; corregge la causa e ripete i test. Non serve creare un nuovo Goal né chiedere al CLIENT quale algoritmo usare.

Se la stessa classe di errore ricompare molte volte, il problema non si risolve aggiungendo infinitamente casi speciali. I3 deve esaminare il sottosistema in profondità, rivedere l'ipotesi tecnica e ottenere una verifica indipendente. Un nuovo passaggio strategico è necessario solo se emergono nuove condizioni materiali che invalidano la decisione iniziale.

Un cambio di prodotto è diverso: se il CLIENT vuole rendere pubblica su Internet una ricerca finora locale, cambiano rischi, autorizzazioni e forse architettura. Questa richiesta torna al proprietario della decisione e al Planner. I3 non deve espandere il proprio charter senza una base valida.

## 4. Limiti delle autorizzazioni esterne

La presenza di credenziali o connessioni non equivale a permesso generale. Consultare un file locale, eseguire test sintetici e generare una bozza sono azioni diverse da modificare un database di produzione, inviare email reali, utilizzare un servizio a pagamento o pubblicare contenuti protetti.

Ogni azione sensibile dovrebbe avere un obiettivo preciso, un limite e un'autorità riconoscibile. «Finisci tutto» non autorizza spesa illimitata né trattamento indiscriminato di dati personali. Un agente può proporre un'operazione esterna, ma non deve dedurne automaticamente il consenso del CLIENT.

Per esempio, «puoi provare la migrazione sulla copia sintetica e verificare il backup; non toccare la produzione» è un confine utile. Se non è chiaro se una transazione reale sia già stata eseguita, il controller non la ripete alla cieca. Prima ricostruisce il fatto e cerca una ricevuta idempotente quando il sistema ne dispone.

Per le risorse di terzi, il progetto deve rispettare licenze e condizioni concrete. Un controllo ragionevole dei diritti non significa pretendere certificazioni inutili per ogni file, ma nemmeno considerare liberamente pubblicabile tutto ciò che è tecnicamente scaricabile.

## 5. Leggere correttamente un rapporto tecnico

Un rapporto «tutti i test verdi» è un indizio, non una prova completa. Occorre sapere quali test, quale codice, quale database, quali condizioni e quali requisiti. È importante che la dichiarazione di successo resti legata al candidato esatto che è stato provato.

Un rapporto utile separa affermazioni e prove:

- Quale capacità viene dichiarata disponibile?
- Quale versione concreta è stata eseguita?
- Quali controlli hanno prodotto un risultato osservabile?
- Quali casi o ambienti sono rimasti fuori?
- Quali errori sono stati corretti e quali rischi restano?
- Chi può prendere la decisione di accettazione?

Una registrazione della schermata può mostrare il flusso visivo, ma non necessariamente la correttezza delle transazioni. Un test unitario può dimostrare il comportamento di una funzione, ma non la leggibilità dell'interfaccia. Un hash di un pacchetto identifica il contenuto, non ne certifica la sicurezza o l'utilità.

Il tempo dei test conta. Se il codice viene modificato dopo una revisione materiale, i vecchi risultati potrebbero non essere più applicabili. Il controller deve rivalutare i gate coinvolti e fornire una nuova prova. Questo non è inutile perfezionismo: impedisce di accettare un candidato diverso da quello esaminato.

## 6. Git e identità del lavoro

Git è fondamentale per riconoscere il codice, ma non registra automaticamente tutte le autorizzazioni. Un commit può essere creato da uno strumento per conto di una persona; il suo autore tecnico non prova necessariamente l'identità dell'agente o la validità della campagna. Le informazioni di responsabilità devono essere mantenute separatamente quando necessario.

Non esiste neppure una regola secondo cui due lavori dello stesso repository debbano sempre fermarsi a vicenda. La concorrenza va decisa sulle risorse realmente toccate: codice condiviso, database, migrazioni, configurazioni o artefatti. Due workstream diversi possono interferire sulla stessa tabella; due modifiche allo stesso prodotto possono essere indipendenti.

Quando si creano worktree temporanei per una concorrenza legittima, bisogna rimuoverli una volta completato il loro scopo. Non accumulate cloni, cache, render o screenshot per sicurezza indefinita. Conservate gli artefatti che hanno reale valore probatorio, con percorso, versione e provenienza riconoscibili.

Una riparazione non dovrebbe partire da comandi distruttivi. Se il working tree contiene modifiche non note, indagatele. Il reset forzato non è un metodo universale per eliminare errori e può cancellare lavoro o prove non ancora integrate.

## 7. Cinque domande utili ogni giorno

Alla fine di ogni sessione il team può rispondere a cinque domande. Primo: quale capacità utilizzabile è avanzata? Secondo: quale candidato concreto e quali prove lo dimostrano? Terzo: quale rischio o gate resta aperto? Quarto: chi possiede la prossima decisione? Quinto: la prossima sessione potrà continuare senza consultare tutto il vecchio dialogo?

Le risposte possono essere brevi. Non servono lunghe trascrizioni quotidiane. L'importante è distinguere avanzamento reale da attività. Dieci nuovi commit non sono un risultato se la funzione principale continua a fallire. Un bug di integrità corretto e verificato può invece rappresentare un miglioramento sostanziale anche senza nuove schermate.

Quando il lavoro è bloccato da un'incertezza, il rapporto deve indicare l'esatto fatto mancante. «Non possiamo modificare la banca dati finché non sappiamo quale migrazione è stata applicata» è una conclusione utile. Nel frattempo, un'analisi di codice indipendente può ancora essere permessa.

Queste cinque domande non sostituiscono i test formali. Servono a mantenere il lavoro orientato al prodotto e a rendere visibile una decisione futura senza ricreare l'intera storia.

## 8. Esempio di una giornata completa

La mattina il controller apre il gestionale dell'associazione. Il charter autorizza la ricerca dei soci per nome e numero. Il repository e la base dati sintetica vengono identificati; nessuna modifica alla produzione è permessa. I test esistenti verificano che la registrazione dei soci funzioni ancora.

Durante lo sviluppo emerge un errore: i soci disattivati non appaiono più nei risultati, anche quando l'utente applica il filtro storico. La regola confermata dice invece che la cronologia deve restare consultabile. I3 corregge la query, aggiunge casi di regressione e prova il percorso dalla schermata al database.

Un revisore indipendente esamina i casi difficili: nessun risultato, molti omonimi, campi vuoti, caratteri speciali e accesso non autorizzato. L'esperienza umana viene provata separatamente. Se l'utente non capisce come attivare il filtro, la funzione non soddisfa ancora pienamente la qualità attesa.

La sera il team registra il candidato effettivo, i risultati tecnici, gli eventuali limiti e la prossima azione. Il Planner rientra per una vera decisione strategica, non per rilasciare nuove istruzioni su ogni piccolo fix. Così la continuità non dipende dalla memoria della giornata.

## 9. Come formulare una consegna al controller

Una consegna tecnica efficace può essere breve ma completa:

> Obiettivo: rendere utilizzabile end-to-end la ricerca soci concordata. Fonti: stato corrente verificato e charter in vigore. Limiti: nessun dato di produzione, nessun provider esterno, nessuna modifica del significato di disattivazione. Verifiche: unità, integrazione, database, comportamento reale e usabilità come gate distinti. Conclusione: candidato esatto, prove, falsificatori e problemi rimasti.

L'ordine di lavoro non ripete l'intera conversazione precedente se le informazioni sono già nel repository. Indica invece le responsabilità e i vincoli che permettono a I3 di lavorare in modo autonomo. In questo contesto, autonomo significa gestire i dettagli tecnici autorizzati, non inventare preferenze dell'utente.

La consegna deve evitare microtask eccessivamente prescrittivi. Se il controller scopre che un refactoring interno è necessario per la correttezza, può eseguirlo entro il confine del charter. Se rileva una nuova esigenza di pubblicazione o una dipendenza esterna non prevista, deve fermare l'azione pertinente e richiedere la decisione corretta.

## 10. Interpretare gli stati operativi

Il controller locale opzionale [campaignctl.py](../../../../tools/campaignctl.py) può gestire alcuni passaggi e checkpoint. Le sue transizioni rappresentano lo stato della superficie che controlla; non dimostrano da sole che un agente remoto abbia eseguito codice né che la produzione sia stata aggiornata correttamente.

In caso di interruzione si controllano identità, ultimo checkpoint valido e attività esterne già compiute. Una ripresa non deve ripetere automaticamente un effetto irreversibile. È necessario distinguere un comando non avviato da uno completato ma non ancora registrato nella conversazione.

Se uno stato risulta incoerente, non si dovrebbe correggerlo assegnando casualmente un nuovo identificatore. La diagnosi individua la causa sulla fonte proprietaria. La decisione di continuare o mantenere HOLD dipende dai fatti verificati e dall'effetto della modifica programmata.

## 11. Revisione, correzioni e decisioni

Il rapporto terminale deve descrivere l'intera capacità e non soltanto l'ultimo file modificato. Un revisore controlla il candidato esatto. Se trova difetti già compresi nel charter, questi tornano a I3 come lavoro da correggere nella stessa campagna.

Il Planner valuta se la capacità realizzata corrisponde alla strategia e ai criteri concordati. Il CLIENT conserva la valutazione del risultato visibile e le autorizzazioni riservate. Un test tecnico non diventa automaticamente accettazione umana, così come una demo gradevole non sostituisce la verifica della banca dati.

Se due o più ritorni riguardano lo stesso sottosistema, I3 deve fare hardening complessivo e revisione indipendente prima di proporre un altro candidato. Questa regola evita la produzione infinita di rapporti prematuri e promuove la soluzione delle cause.

La qualità dell'esecuzione si riconosce dal risultato verificabile, non dal numero di agenti coinvolti o di ore di attività. Anche il rapporto più dettagliato resta insufficiente se il candidato non può essere riprodotto.

## 12. Lasciare un contesto recuperabile

Prima di chiudere, aggiornate le superfici canoniche pertinenti: codice o candidato, stato della campagna, gate aperti, prove e prossima azione legale. Una fonte storica può rimanere accessibile, ma non dovrebbe confondersi con l'autorità corrente.

Evitate di copiare le stesse politiche in molti documenti. Una regola stabile ha un proprietario; uno stato che cambia ha una superficie corrente; un rapporto di test conserva il proprio contesto. Collegamenti chiari e versioni riconoscibili sono più affidabili di un enorme riassunto senza provenienza.

La prova finale è chiedere a un'altra sessione di aprire il repository e continuare in sicurezza. Se deve rivolgersi al CLIENT per risolvere ogni dettaglio tecnico, il processo non ha ancora mantenuto la promessa di continuità.

**Segue:** capitolo 04, Richiedere modifiche.

## Fonti e limiti

- [Execution Team OS](../../../../protocols/EXECUTION_TEAM_OS.md)
- [Charter di campagna](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Currentness e ricostruzione](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md)
- [Efficienza e igiene del repository](../../../../protocols/REPOSITORY_EFFICIENCY_AND_WORKSPACE_HYGIENE.md)
- [Integrità del review](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Controller locale opzionale](../../../../tools/campaignctl.py)

Il percorso descritto non conferma esecuzione nativa di servizi esterni o accettazione di un prodotto concreto.
