# 05 — Errori, incidenti e recupero sicuro

ArquitecturaRepo · Manuale completo per l'utente · Edizione v1.4 · Italiano

> Quando qualcosa non funziona, l'obiettivo è capire la causa e recuperare senza perdere prove o dati. Questo capitolo integra le [regole di ricostruzione](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md), il [protocollo di recupero](../../../12_TRANSACTION_RECOVERY.md) e i [confini di sicurezza](../../../../protocols/SECURITY_PRIVACY_RIGHTS_AND_EXTERNAL_ACTIONS.md).

## Contenuti

1. Conservare le prove prima di intervenire
2. Errori di ambiente, login e permessi
3. Problemi nella struttura di controllo
4. Git non annulla ogni effetto
5. Fallimenti ripetuti e cause sistemiche
6. Sicurezza, privacy e diritti di terzi
7. Dimostrare che il recupero è avvenuto
8. Tre casi di recupero completi
9. Operazioni sensibili e decisioni corrette
10. Limiti di una validazione riuscita
11. Feedback locale e configurazione della privacy

## 1. Conservare le prove prima di intervenire

Un errore è un'informazione. La risposta immediata non dovrebbe essere cancellare il repository, reinstallare il framework o forzare un reset. Prima si registra che cosa è successo, su quale versione, con quali dati e durante quale operazione. Il messaggio di errore completo, l'ambiente, il commit, il database e gli eventuali checkpoint servono a distinguere causa e sintomo.

La pausa necessaria dipende dall'effetto possibile. Se manca una dipendenza Python, si possono continuare altre attività indipendenti. Se una migrazione ha forse modificato i dati reali dei soci, ulteriori scritture sul database devono fermarsi finché non si conosce lo stato. Non è necessario bloccare automaticamente ogni parte del progetto, ma nemmeno procedere come se il rischio non esistesse.

Le operazioni di recupero devono avere una destinazione precisa. Un reset indiscriminato del working tree può cancellare modifiche di altri esecutori. Una nuova migrazione può duplicare un effetto già applicato. Cancellare log e file temporanei prima di classificarli può rimuovere gli unici indizi dell'incidente.

Una sequenza affidabile è osservare, preservare, classificare, formulare un'ipotesi, applicare una correzione autorizzata e verificare l'effetto. Se le prove non permettono di stabilire quale transazione sia stata completata, lo stato resta sconosciuto. La certezza non può essere prodotta scrivendo una dichiarazione rassicurante.

## 2. Errori di ambiente, login e permessi

Molti problemi non derivano dal codice dell'applicazione. L'interprete può essere quello sbagliato, una libreria non essere installata, il percorso del repository essere diverso da quello immaginato oppure la sessione di autenticazione essere scaduta.

Cominciate dalle condizioni osservabili. Controllate il percorso corrente, la versione del linguaggio, le dipendenze dichiarate e i permessi. Se un agente non vede i file, non concedetegli subito accesso a tutte le cartelle: verificate prima quale workspace gli è stato effettivamente aperto.

Un errore di accesso non autorizza a superare una protezione. Se l'operazione richiede un'autenticazione o un permesso aggiuntivo, si coinvolge il proprietario del servizio secondo il flusso previsto. Non è corretto raccogliere credenziali fuori dal contesto autorizzato o riutilizzare segreti di un'altra applicazione.

Quando un provider esterno non risponde, distinguete rete, quota, fatturazione, credenziali, versione API e bug. Un test locale con dati sintetici può restare possibile anche se l'operazione reale è temporaneamente vietata. La diagnosi dovrebbe esplicitare questa separazione.

## 3. Problemi nella struttura di controllo

Il livello .agentic-sdlc/ contiene riferimenti a requisiti, Product State, ruoli e campagne. Un controllo che fallisce non significa sempre che la struttura sia rotta. Potrebbe segnalare correttamente che non si conosce la fonte corrente di una decisione o che due stati sono in contraddizione.

Gli strumenti [project_status.py](../../../../tools/project_status.py), [validate_project.py](../../../../tools/validate_project.py) e [reconstruct_context.py](../../../../tools/reconstruct_context.py) aiutano a vedere queste condizioni. Un errore di sintassi JSON è diverso da una SHA valida nella forma ma riferita a codice vecchio. Nel primo caso serve una correzione di formato; nel secondo serve una ricostruzione della realtà.

Non riempite campi con identificatori inventati per ottenere un PASS. Un valore plausibile può essere più pericoloso di un campo dichiarato sconosciuto, perché porta gli esecutori successivi a compiere azioni basate su una falsa certezza. La documentazione deve distinguere ciò che è osservato da ciò che è proposto.

Se una campagna risulta conclusa ma i test non sono collegati al candidato attuale, la sua accettazione non è dimostrata per quel candidato. Il controller deve recuperare o produrre la prova adeguata, non dichiarare che la revisione precedente vale automaticamente per ogni modifica futura.

Anche il nome CURRENT non è una garanzia magica. La currentness è una relazione verificabile tra file, versione, dati e autorità. Quando il legame manca, si mantiene HOLD per le azioni dipendenti e si ricostruisce il riferimento corretto.

## 4. Git non annulla ogni effetto

Git consente di tracciare e recuperare codice, ma non ripristina da solo un database, una email già inviata o una transazione finanziaria. Una modifica al codice può essere annullata mentre i dati restano nello stato introdotto dalla migrazione. Per questo l'identità del candidato include, quando necessario, schema, migrazioni, configurazione e artefatti esterni.

Prima di un comando distruttivo si deve sapere esattamente quali file saranno coinvolti e a chi appartengono le modifiche locali. Non usate reset forzati o cancellazioni di interi checkout come risposta ordinaria a un errore. Un revert mirato o un fix possono essere più sicuri se preservano la storia e permettono di verificare l'effetto.

Il commit Git non prova l'identità operativa di un agente. La persona che ha integrato una modifica può essere diversa da chi ha scritto il codice e da chi lo ha autorizzato. Le regole del framework mantengono separate storia del repository, responsabilità ed evidenza di esecuzione.

Anche i worktree temporanei devono essere trattati con attenzione. Sono utili per una reale concorrenza, ma non devono accumularsi senza proprietario. Solo dopo aver verificato che non contengano lavoro corrente o prove canoniche possono essere rimossi e la metadata Git ripulita.

## 5. Fallimenti ripetuti e cause sistemiche

Un bug ordinario appartiene a I3 nell'ambito della campagna valida. Se un test fallisce, il controller investiga e corregge. Il Planner non deve emettere un nuovo charter ogni volta che l'esecuzione incontra una difficoltà.

Tuttavia, riparazioni ripetute che risolvono soltanto il sintomo sono un segnale importante. Immaginiamo che una ricerca soci fallisca alternativamente con accenti, maiuscole e spazi. Dopo diverse correzioni, I3 dovrebbe esaminare l'intero percorso di normalizzazione, persistenza, query e interfaccia, cercando la causa comune.

La revisione indipendente deve mettere alla prova le ipotesi dell'implementatore. Non basta leggere il nuovo test che l'autore ha appena scritto. Occorre cercare casi che possano falsificare la correttezza della soluzione. Il risultato deve essere integrato nello stesso lavoro autorizzato, salvo vera invalidazione strategica.

Anche un valutatore può essere difettoso. Potrebbe accettare un risultato che non soddisfa il prodotto oppure bloccare indefinitamente una capacità per una formalità non più rilevante. La riparazione del valutatore è un'attività tecnica, ma non deve rimuovere silenziosamente un controllo di sicurezza necessario.

Il criterio resta il rischio reale. Un sistema che corregge la causa riduce il numero di rientri inutili; un sistema che produce altri PASS per gli stessi errori accumula soltanto attività.

## 6. Sicurezza, privacy e diritti di terzi

Se un incidente riguarda dati personali, accessi o segreti, bisogna limitare l'esposizione preservando le informazioni necessarie a capire il guasto. Non copiate password, token o dati reali in Issue pubbliche o log condivisi senza protezione.

Il gestionale dell'esempio contiene nomi e quote. Per testare il codice si dovrebbero usare dati fittizi o adeguatamente anonimizzati. L'invio di dati reali a un servizio esterno richiede una valutazione separata delle regole applicabili e dell'autorità del CLIENT. La semplice disponibilità tecnica di un endpoint non costituisce consenso.

L'effetto di una simulazione è diverso da un'azione reale. Generare una bozza di email non equivale a inviarla. Mostrare una ricevuta fittizia non prova un pagamento bancario. Preparare un'immagine non significa aver ottenuto il diritto di pubblicarla. Un sistema affidabile conserva queste differenze sia nel codice sia nei rapporti.

Per materiali di terzi rispettate le licenze effettive e le limitazioni del caso. La licenza MIT dello starter non estende automaticamente i propri termini a ogni biblioteca, video, immagine o servizio utilizzato dal prodotto.

## 7. Dimostrare che il recupero è avvenuto

La scomparsa del messaggio di errore non basta. Dopo una correzione si verifica l'effetto che prima falliva e le proprietà che potrebbero essere state danneggiate. Per una migrazione, questo include schema, dati, vincoli, eventuali duplicati e comportamento al riavvio. Per una schermata, può essere necessaria una prova reale del flusso dell'utente.

La verifica deve riferirsi a un candidato preciso. Se dopo i test viene modificato il codice, i risultati precedenti non sono automaticamente applicabili. Il rapporto di recupero descrive ciò che è stato realmente osservato e ciò che resta escluso.

Un incidente chiuso correttamente lascia uno stato corrente coerente: problema, causa, correzione, prove e prossimo passo. Le vecchie note restano evidenza storica, non una seconda fonte di verità attuale. Se una parte dell'effetto non è verificabile, il limite va dichiarato.

In caso di dubbio su una transazione esterna già eseguita, non la si ripete alla cieca. Prima si cerca una ricevuta o un riferimento idempotente e si coinvolge l'autorità competente. La prudenza è particolarmente necessaria quando l'azione è irreversibile.

## 8. Tre casi di recupero completi

**Caso A — Dipendenza Python assente.** Lo scaffold è riuscito, ma la validazione indica che manca jsonschema. L'esecutore controlla l'interprete attivo e requirements-validation.txt, installa la dipendenza dichiarata e ripete il controllo. Non modifica requisiti, Product State né charter. Il recupero riguarda l'ambiente, non il prodotto.

**Caso B — Migrazione interrotta.** Durante una prova su dati sintetici, l'operazione si interrompe. I3 ferma nuove scritture, esamina journal e stato delle transazioni, confronta schema e backup. Solo dopo decide se completare, ripetere in sicurezza o ripristinare. Il successo è verificato con test di integrità e riavvio; non viene dichiarato sulla base di una semplice frase «riprovato».

**Caso C — Rapporto di accettazione vecchio.** Un documento dice che la ricerca soci è stata approvata, ma da allora il codice è cambiato. Il Planner conserva la precedente decisione come storia e segnala che la currentness è venuta meno. I3 identifica il nuovo candidato e ripete i gate interessati. Se necessario, il CLIENT prova nuovamente il flusso visibile.

Questi esempi richiedono strategie diverse. Un unico comando «reinstalla tutto» non risolve simultaneamente ambiente, banca dati e identità delle prove. La diagnosi per causa è più efficace di una sequenza automatica di tentativi.

## 9. Operazioni sensibili e decisioni corrette

| Azione | Gestione ordinaria | Confine importante |
| --- | --- | --- |
| Leggere log locali | Diagnosi tecnica in sola lettura | Non divulgare segreti |
| Ripetere un test unitario | I3 nella campagna | Collegarlo al candidato |
| Ripristinare una banca dati di prova | I3 dopo controllo di stato | Destinazione esatta e ripetibilità |
| Eliminare dati produttivi | Recupero esplicitamente autorizzato | Valutare perdita e backup |
| Ripetere un pagamento reale | Non automaticamente | Verificare effetto precedente e permesso |
| Pubblicare contenuti di terzi | Verifica di diritti e condizioni | Uso specifico e licenza |
| Cambiare una richiesta confermata | CLIENT e Planner quando serve | Registrare la supersessione |
| Sostituire un charter con un nuovo nome | Non è una riparazione valida | Ricostruire l'autorità reale |

La tabella non sostituisce la valutazione di una situazione concreta. Aiuta a riconoscere le operazioni che hanno effetti oltre il codice e che non possono essere autorizzate implicitamente da una richiesta generica di completare il lavoro.

## 10. Limiti di una validazione riuscita

Un test del framework può essere verde mentre l'applicazione non si avvia. Un test della funzione di calcolo può passare mentre l'interfaccia seleziona il socio sbagliato. Un video può sembrare convincente mentre il database perde i dati al riavvio. Sono problemi diversi e richiedono prove diverse.

Mantenete separati i gate: unità, integrazione, DB/currentness, semantica e generalizzazione, funzionamento fisico, qualità percettiva e release. Non tutti i progetti richiedono ogni possibile verifica nella stessa profondità, ma un gate rilevante non può essere sostituito silenziosamente da un altro.

Un HOLD preciso non equivale al fallimento totale del progetto. Indica che una certa affermazione o azione non è ancora giustificata. Si possono proseguire verifiche indipendenti che non dipendono dall'informazione mancante. Questa granularità permette di lavorare senza fingere certezza.

L'accettazione del prodotto resta distinta dai test del pacchetto ArquitecturaRepo. Un buon framework aiuta a raccogliere le prove, ma non può garantire risultati reali per un'applicazione che non ha mai eseguito.

## 11. Feedback locale e configurazione della privacy

La distribuzione v1.4 può generare localmente un piccolo rapporto di metadati sull'uso del framework. Non include automaticamente un collettore esterno verso il maintainer. La pianificazione con GitHub Actions e l'esecuzione del generatore locale sono controlli separati.

L'opzione --no-feedback-workflow disattiva la pianificazione periodica ma non il generatore. Per evitare qualsiasi rapporto, impostate enabled=false in .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json. Per i dettagli consultate la [politica sul feedback](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md).

Se qualcuno segnala una trasmissione indesiderata, verificate il percorso realmente eseguito, la configurazione e il contenuto del rapporto. Non deducete l'invio dal solo fatto che un file esista e non deducete l'assenza di ogni esecuzione dalla mancanza di un scheduler.

Una cultura del recupero matura protegge i dati, preserva le prove e rimuove le cause dei problemi senza moltiplicare inutilmente ruoli o procedure. Il suo successo è una ripresa controllata, non una dashboard piena di indicatori verdi.

**Segue:** capitolo 06, Accettazione delle capacità.

## Fonti e limiti

- [Currentness e ricostruzione](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md)
- [Recupero transazionale](../../../12_TRANSACTION_RECOVERY.md)
- [Sicurezza e azioni esterne](../../../../protocols/SECURITY_PRIVACY_RIGHTS_AND_EXTERNAL_ACTIONS.md)
- [Igiene del repository](../../../../protocols/REPOSITORY_EFFICIENCY_AND_WORKSPACE_HYGIENE.md)
- [Integrità delle revisioni](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Privacy del feedback](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md)

Gli incidenti illustrati sono fittizi e non autorizzano alcuna operazione su dati reali di terzi.
