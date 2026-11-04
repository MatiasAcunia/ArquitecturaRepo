# 01 — Installazione e configurazione

ArquitecturaRepo · Manuale completo per l'utente · Edizione v1.4 · Italiano

> Questo capitolo distingue l'installazione dello starter dalla sua adozione in un progetto reale. I comandi sono allineati alla [guida pubblica v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md). Il successo del programma di installazione non dimostra che l'applicazione sia stata capita, implementata o accettata.

## Contenuti

1. Preparare ambiente e account
2. Separare starter, fork e applicazione
3. Controllare le directory prima di scrivere
4. Scegliere il profilo corretto
5. Creare il livello di controllo
6. Verificare senza falsificare lo stato
7. Avviare la scoperta del prodotto
8. Gestire applicazioni già esistenti
9. Connessioni e protezione dei dati
10. Risolvere gli errori più frequenti

## 1. Preparare ambiente e account

Gli esempi usano Windows, PowerShell, Git e Python. Non è obbligatorio utilizzare esattamente questi strumenti per beneficiare dell'architettura. Serve però un modo affidabile per identificare la versione del codice, accedere ai file del progetto e avviare gli strumenti di verifica compatibili con la distribuzione scelta.

La versione Python 3.12 è stata esercitata nei test portabili della release v1.4. Per controllare l'interprete attivo in PowerShell si possono eseguire questi comandi:

    & "python" --version
    & "py" --version

Se non funzionano, controllate l'installazione dell'interprete e il PATH del terminale. Non scaricate eseguibili da pagine sconosciute per risolvere frettolosamente un errore. Un comando fallito va diagnosticato nel contesto reale: sistema operativo, directory, permessi e dipendenze.

Un servizio di coding remoto può usare risorse esterne, ma non per questo l'applicazione locale richiede una GPU particolare. Allo stesso modo, una potente macchina locale non concede automaticamente accesso a un modello esterno. Il framework non installa modelli, non seleziona provider e non autorizza consumi a pagamento per il semplice fatto di essere presente.

Prima di procedere, scegliete il repository dell'applicazione. È facile aprire la cartella dello starter in un editor e chiedere a un agente di realizzare lì il prodotto. In questo modo la documentazione pubblica, gli esempi e il codice dell'applicazione rischiano di mescolarsi. Il percorso di destinazione deve essere verificato e distinto.

Proteggete gli account collegati. Usate autenticazione adeguata e il minimo accesso necessario. Un collegamento GitHub non dimostra che l'assistente stia guardando il repository corretto; una sessione autenticata non equivale a permesso di effettuare pubblicazioni o modifiche distruttive.

## 2. Separare starter, fork e applicazione

Ci sono tre oggetti diversi che possono sembrare lo stesso progetto:

| Oggetto | Scopo | Che cosa non rappresenta |
| --- | --- | --- |
| Repository ArquitecturaRepo | Protocolli, strumenti, profili, modelli, test e documentazione pubblica | L'applicazione da sviluppare |
| Fork dello starter, eventuale | Personalizzazioni mantenute dall'utilizzatore | Un Product State reale creato automaticamente |
| Repository dell'applicazione | Codice, dati, configurazione e livello .agentic-sdlc/ installato | Una copia indiscriminata degli esempi sintetici |

Una struttura locale sensata può essere:

    C:\Progetti\
        ArquitecturaRepo\
        gestione-soci\

Il nome della cartella è soltanto illustrativo. La separazione delle responsabilità è invece reale: lo starter fornisce meccanismi generici; gestione-soci contiene il prodotto specifico. Il progetto può rimanere privato anche quando il framework usato è pubblico.

Se si intende modificare e mantenere una variante del framework, un fork può essere utile. In caso contrario basta un checkout attendibile o l'archivio della release. Non è necessario creare un repository nuovo ogni volta che una conversazione riparte. Anzi, cloni duplicati e worktree dimenticati possono rendere ambigua la versione corrente e consumare spazio.

Per una distribuzione riproducibile, consultate la [release v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0) e controllate checksum e manifest del pacchetto. Il ramo main può ricevere documentazione successiva alla pubblicazione. Non bisogna descrivere tali aggiunte come contenuto dello ZIP già pubblicato.

## 3. Controllare le directory prima di scrivere

Prima dell'installazione aprite il terminale nel checkout del framework e verificate dove siete:

    Get-Location
    & "python" --version
    & "git" status --short

Get-Location mostra la directory corrente; il controllo dell'interprete conferma l'ambiente; git status rende visibili le modifiche locali. Se il comando Git fallisce, non date per scontato che il progetto sia danneggiato: potreste semplicemente trovarvi fuori dal repository.

Se compaiono modifiche esistenti, non rimuovetele per rendere il tutorial più semplice. Possono appartenere a un altro sviluppatore oppure rappresentare lavoro ancora non integrato. La prima responsabilità è conservarle e comprenderne la relazione con la versione attuale.

Verificate il percorso dell'applicazione separatamente. Editor, terminale, tool di coding e client Git possono puntare a cartelle diverse. Prima di concedere scrittura a un agente, chiarite in quale directory opererà e quali risorse potrà modificare.

Se l'applicazione contiene già .agentic-sdlc/, un controller, Product State, campagne o dati di esercizio, non tentate una seconda installazione sopra la prima. La [procedura di attachment per progetti già governati](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) parte da una verifica in sola lettura. Non promette una migrazione generale e automatica da qualsiasi versione precedente.

## 4. Scegliere il profilo corretto

Il profilo va scelto in relazione ai rischi e alle caratteristiche del prodotto, non al numero di agenti che si desidera lanciare. I profili pubblici sono definiti in [profiles.json](../../../../profiles/profiles.json).

| Profilo | Quando considerarlo |
| --- | --- |
| SMALL | Prodotto circoscritto e rischio operativo limitato |
| STATEFUL | Dati persistenti, utenti, backup, migrazioni e ripresa |
| ARTIFACT_HEAVY | Molti output, file grandi, provenienza, diritti e gestione dello spazio |
| MULTI_WORKSTREAM | Flussi di lavoro diversi che devono integrarsi nello stesso prodotto |
| MULTI_PRODUCT | Prodotti distinti che condividono risorse o governance |
| HIGH_CONSEQUENCE | Conseguenze elevate su sicurezza, privacy, finanza o azioni irreversibili |

Un semplice prototipo può iniziare con SMALL. Un gestionale che conserva dati di soci e quote deve considerare STATEFUL. Questo non impone automaticamente un Master Owner separato o una rete di molti modelli. I ruoli sono responsabilità, non un requisito numerico di processi.

Documentate brevemente il motivo della scelta. Un profilo non certifica che i rischi siano già stati mitigati e non concede nuove autorizzazioni. Se il prodotto cambia, i controlli possono essere adattati sulla base di evidenze aggiornate, senza trasformare ogni piccola modifica in una ricostruzione totale.

## 5. Creare il livello di controllo

Dal checkout verificato dello starter v1.4, in PowerShell, un nuovo progetto non governato può essere preparato così:

    & "python" "tools\scaffold_project.py" --target "..\mio-progetto" --profile "SMALL" --product-id "MIO_PROGETTO" --objective "Obiettivo iniziale da confermare" --language "it" --no-feedback-workflow

Per il caso immaginario dell'associazione, con dati persistenti, una configurazione motivata potrebbe essere:

    & "python" "tools\scaffold_project.py" --target "..\gestione-soci" --profile "STATEFUL" --product-id "GESTIONE_SOCI" --objective "Anagrafica soci e quote" --language "it" --no-feedback-workflow

Sono due esempi alternativi. Non eseguiteli entrambi sulla stessa destinazione. target indica il percorso esatto; profile seleziona i controlli; product-id è un identificatore del progetto; objective è una descrizione iniziale ancora da confermare; language it seleziona la documentazione localizzata.

Il programma crea il livello .agentic-sdlc/ nella destinazione, mantenendo i file applicativi e i workflow preesistenti. Deve rifiutare la sovrascrittura di un controllo canonico già installato. Non esiste una regola generale secondo cui ripetere l'installazione risolve un problema di validazione.

Lo stato iniziale HOLD / UNTRUSTED_CONTEXT è corretto. Il framework non ha ancora verificato quale codice, database, requisito o decisione sia attuale nel progetto. Modificare manualmente questo stato in READY per ottenere un esito verde falsificherebbe la continuità.

L'opzione --with-runtime aggiunge meccanismi locali opzionali. Non installa un provider esterno, non autentica una sessione Codex Desktop e non attiva automaticamente campagne reali. I permessi e i gate di esecuzione sono autonomi rispetto alla creazione delle cartelle.

## 6. Verificare senza falsificare lo stato

Dopo l'installazione, aprite il terminale nella cartella dell'applicazione, non in quella del framework. Il percorso iniziale di verifica comprende:

    & "python" -m pip install -r ".agentic-sdlc\requirements-validation.txt"
    & "python" ".agentic-sdlc\tools\project_status.py" --control-root ".agentic-sdlc"
    & "python" ".agentic-sdlc\tools\discover_project.py" --project-root "."
    & "python" ".agentic-sdlc\tools\reconstruct_context.py" --root ".agentic-sdlc"

La prima riga installa le dipendenze dichiarate per la validazione. Le successive verificano lo stato riconosciuto, raccolgono una descrizione del progetto senza modificare il codice e tentano di ricostruire il contesto. Il risultato HOLD nella ricostruzione è normale finché non esiste una base adottata e confermata.

Controllate tre aspetti fisici: il livello .agentic-sdlc/ si trova davvero nella destinazione prevista; i file e i workflow originali non sono stati sostituiti; gli strumenti restituiscono risultati interpretabili e riproducibili. Se manca jsonschema, installate i requisiti nell'interprete effettivamente utilizzato.

La validazione dei contratti è distinta dalla prova della vostra applicazione. Potete avere file JSON impeccabili e un gestionale che non riesce a salvare un socio. Allo stesso modo, un'applicazione può avviarsi mentre lo stato canonico indica erroneamente una campagna vecchia. I diversi livelli di verifica non si sostituiscono.

Conservate il risultato del primo controllo e il riferimento alla versione del framework. Se un nuovo esecutore torna sul progetto, deve poter capire se una determinata difficoltà riguarda l'ambiente, l'adozione o il codice del prodotto.

## 7. Avviare la scoperta del prodotto

La tappa successiva è la discovery, non l'implementazione immediata di funzionalità. Il [prompt di installazione e adattamento](../../../../prompts/INSTALL_THIS_SDLC.md), il [prompt di discovery](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md) e il [contratto di adozione](../../../16_TRANSFER_ADOPTION.md) chiariscono quali informazioni debbano essere raccolte.

Il Planner controlla il repository reale, le tecnologie, la situazione dei dati, gli utenti, le funzionalità presenti e i rischi operativi. Il CLIENT conferma i requisiti di prodotto. Engineering verifica e decide la base tecnica, pianifica una prima consegna e prepara l'adozione delle informazioni coerenti nel Product State e negli altri archivi previsti.

Non copiate la configurazione sintetica di un esempio come se descrivesse il vostro sistema. Una SHA inventata, un Goal fittizio o un'approvazione mai data non diventano veri perché rispettano uno schema. Se il dato manca, si deve conservare l'incertezza e cercare la prova corretta.

L'adozione avviene dopo un preflight. La ricostruzione in un contesto nuovo deve poter identificare obiettivo, requisiti, versione del codice, stato dei dati, responsabilità e prossima azione autorizzata. Soltanto dopo è ragionevole avviare la prima campagna materiale.

## 8. Gestire applicazioni già esistenti

Molti utenti non partono da zero. Un'applicazione potrebbe contenere codice reale, migrazioni e dati preziosi prima dell'installazione del framework. In questo caso l'operazione deve rispettare la realtà esistente: nessuna pulizia indiscriminata, nessuna cancellazione della cronologia, nessuna sostituzione cieca del controllo.

Distinguete un progetto completamente nuovo, un progetto con codice ma senza governance canonica e un progetto già governato. Nel primo caso si segue l'installazione ordinaria. Nel secondo si effettua prima una verifica del percorso e degli artefatti. Nel terzo si usa il [preflight in sola lettura](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) per capire compatibilità, conflitti e possibili rischi.

Le note di rilascio non devono essere interpretate come prova di una migrazione automatica da qualsiasi versione. Il percorso esatto dipende dai contratti e dallo stato realmente osservati. È meglio mantenere temporaneamente un HOLD ben motivato che perdere le informazioni necessarie alla ripresa.

## 9. Connessioni e protezione dei dati

Un account GitHub o un servizio di coding può essere utile per leggere e modificare il repository, ma i suoi permessi vanno controllati. Non concedete accessi generali semplicemente perché potrebbero servire in futuro. Un comando locale reversibile non equivale all'autorizzazione a pubblicare, cancellare dati reali, inviare messaggi o acquistare servizi.

Non copiate token, password o chiavi nei prompt, nelle Issue pubbliche o nel codice versionato. Se una diagnosi richiede log, eliminate i valori sensibili senza perdere l'informazione utile. Lo starter pubblico non richiede il trasferimento del database privato dell'applicazione ai manutentori.

Nella v1.4 è previsto un feedback architetturale locale con metadati limitati. L'opzione --no-feedback-workflow disattiva la pianificazione periodica del workflow GitHub Actions, ma non il generatore locale. Per disabilitare ogni report impostate enabled=false nella configurazione .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json. Consultate la [descrizione dei controlli privacy](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md).

Generazione locale, pianificazione e trasmissione esterna sono operazioni diverse. Non si deve presumere che l'esistenza di un file di report implichi l'invio a terzi, né che l'assenza di un workflow impedisca l'esecuzione manuale del generatore.

## 10. Risolvere gli errori più frequenti

| Sintomo | Significato possibile | Intervento sicuro |
| --- | --- | --- |
| Python non riconosciuto | Interprete assente o PATH errato | Controllare terminale e installazione |
| Cartella .agentic-sdlc/ non presente | Target sbagliato o comando fallito | Leggere output e percorso esatto |
| HOLD / UNTRUSTED_CONTEXT | Requisiti e stato reale non ancora adottati | Procedere con discovery |
| jsonschema mancante | Dipendenze non installate nell'ambiente attivo | Usare requirements-validation.txt |
| Controller esistente preservato | Protezione contro sovrascrittura | Seguire attachment in sola lettura |
| Ricostruzione incoerente | Riferimenti di codice, stato o autorità incompatibili | Preservare evidenze e riconciliare |
| Tool collegato al repo sbagliato | Workspace o permessi errati | Sospendere le scritture e verificare |
| Test verdi, app inutilizzabile | Prove del controllo, non del prodotto | Avviare l'applicazione e provare il flusso |

Una diagnosi utile classifica il problema prima di intervenire: ambiente, percorso, permessi, dipendenze, compatibilità, schema, stato corrente o reale funzionalità. Ripetere a caso l'installazione e cancellare directory importanti può peggiorare la situazione.

Considerate completato questo capitolo quando l'installazione giusta è verificabile nel percorso previsto, il codice applicativo preesistente è intatto e lo stato iniziale espone onestamente ciò che ancora non si sa. Il capitolo successivo collega il controllo alle esigenze e al codice reali.

**Segue:** capitolo 02, Planner e adozione.

## Fonti e limiti

- [Release v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0)
- [Guida pubblica v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Note di rilascio](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)
- [Fork e bootstrap](../../../01_FORK_AND_BOOTSTRAP.md)
- [Contratto di trasferimento e adozione](../../../16_TRANSFER_ADOPTION.md)
- [Attachment per progetti governati](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Feedback e privacy](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md)
- [Codice dello scaffold](../../../../tools/scaffold_project.py)

Le istruzioni riguardano lo starter. Non dimostrano l'esecuzione o l'accettazione di un'applicazione esterna.
