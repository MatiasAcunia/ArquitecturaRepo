# 02 — Il Planner e l'adozione del progetto

ArquitecturaRepo · Manuale completo per l'utente · Edizione v1.4 · Italiano

> L'installazione crea gli strumenti di controllo, non una conoscenza valida del prodotto. Questo capitolo illustra come ricostruire la realtà, ottenere la conferma del CLIENT e adottare uno stato coerente. Le fonti sono le [regole di product discovery](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md) e il [contratto di adozione](../../../16_TRANSFER_ADOPTION.md).

## Argomenti

1. Una conversazione non è lo stato del progetto
2. Preparare una verifica in sola lettura
3. Distinguere domande di prodotto e scelte tecniche
4. Confermare requisiti osservabili
5. Stabilire baseline tecnica e piano delle consegne
6. Effettuare un'adozione fondata su prove
7. Verificare il passaggio a una nuova sessione
8. Autorizzare la prima campagna ingegneristica
9. Un colloquio concreto con il CLIENT
10. Criteri per dichiarare pronta la baseline

## 1. Una conversazione non è lo stato del progetto

Un assistente può aver discusso per ore una buona architettura, ma la discussione non dimostra che il codice esista o sia aggiornato. Un messaggio precedente può sostenere che il database ha già certe tabelle mentre il repository attuale contiene una migrazione diversa. Una schermata mostrata al cliente può appartenere a una versione poi modificata. Il Planner deve distinguere desideri, decisioni confermate, proposte e stato fisico.

La prima domanda non è «quali funzionalità programmiamo oggi?», bensì «che cosa sappiamo realmente del prodotto e da quali fonti?». Vanno ricostruiti l'obiettivo, gli utenti, il codice corrente, i dati, le integrazioni, i rischi e le autorizzazioni. Se esiste una governance precedente, il Planner deve leggerla e rispettarne i confini prima di aggiungere nuovi meccanismi.

Il CLIENT non deve diventare il custode della coerenza tecnica. Può confermare le esigenze e correggere l'interpretazione di un flusso di lavoro, ma non dovrebbe dover ricostruire SHA, migrazioni o responsabilità di un controller. Sono attività tecniche da svolgere consultando le evidenze disponibili.

Quando una fonte manca, l'assenza va dichiarata. È meglio un HOLD preciso che una falsa ricostruzione con identificatori plausibili. Riempire un modello JSON con un hash inventato o copiare il Product State di un esempio sintetico non rappresenta un'adozione: significa creare una descrizione tecnicamente coerente nella forma ma falsa nel contenuto.

## 2. Preparare una verifica in sola lettura

Un buon primo passaggio è sistematico ma proporzionato. Si identifica il repository effettivo, il ramo di lavoro, le modifiche locali, i file di configurazione, i test e i comandi di avvio. Si controlla quali database siano realmente collegati, quali migrazioni siano applicate e se esistano artefatti rilevanti al di fuori del codice.

La verifica iniziale non dovrebbe cancellare file né generare decine di copie del repository. Se esiste un checkout attendibile, lo si riutilizza. Per confrontare il lavoro con la sorgente remota si aggiornano i riferimenti necessari e si analizza il delta, senza interpretare automaticamente il movimento Git come identità o autorizzazione di un agente.

Una traccia utile comprende:

1. Prodotto, utenti e principali percorsi d'uso.
2. Ultima intenzione di prodotto confermata.
3. Identità del codice e stato delle modifiche non integrate.
4. Stack, database, ambiente, rete e distribuzione.
5. Permessi, segreti e servizi esterni coinvolti.
6. Controlli già installati, Product State e campagne.
7. Test fisici disponibili e loro rapporto con il codice corrente.
8. Incertezze che cambiano la prossima azione possibile.

La [sessione di product discovery](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md) e il [protocollo di baseline](../../../../protocols/PRODUCT_DISCOVERY_REQUIREMENTS_AND_TECHNICAL_BASELINE.md) aiutano a dare ordine alla verifica. Non devono però produrre un grande archivio di moduli ripetitivi. Ogni informazione importante deve avere un proprietario canonico e una superficie corrente chiaramente identificabile.

## 3. Distinguere domande di prodotto e scelte tecniche

Il CLIENT definisce ciò che l'utente deve ottenere. Il team tecnico decide come realizzarlo. La divisione sembra semplice, ma nel lavoro quotidiano è facile confonderla. Chiedere al CLIENT quale database utilizzare può essere improprio quando la vera domanda riguarda il numero di persone che useranno il programma contemporaneamente.

| Domanda al CLIENT | Scelta che spetta all'ingegneria |
| --- | --- |
| Quanti operatori modificano i dati allo stesso tempo? | Concorrenza, transazioni, conflitti |
| Che cosa significa disattivare un socio? | Schema, riferimenti e migrazioni |
| Serve accesso da Internet oppure solo locale? | Topologia, porte, autenticazione e distribuzione |
| Chi può consultare lo storico delle quote? | Ruoli e controllo degli accessi |
| Quanto tempo si può perdere dopo un guasto? | Strategia di backup, recupero e ripresa |
| La prima versione prevede pagamenti reali? | Integrazioni esterne dopo autorizzazione distinta |

Domande migliori producono decisioni utilizzabili. Per esempio «dobbiamo conservare i pagamenti dopo la disattivazione?» chiarisce un comportamento concreto. La risposta influenza l'architettura, ma non obbliga il cliente a definire chiavi esterne o indici.

Il Planner segnala anche requisiti in conflitto. Se il cliente vuole eliminazione definitiva di ogni dato e contemporaneamente conservazione completa di tutte le operazioni economiche, le due aspettative devono essere chiarite alla luce delle regole applicabili. Non si dovrebbe implementare una soluzione arbitraria e soltanto dopo comunicarne le conseguenze.

Le decisioni più sensibili riguardano sicurezza, dati personali, pubblicazione e operazioni esterne. Engineering può spiegare rischi e opzioni; la parte riservata al CLIENT deve essere confermata in modo esplicito e tracciabile.

## 4. Confermare requisiti osservabili

Dopo il confronto, il Planner produce una rappresentazione compatta dei requisiti attuali. Non basta una frase generica come «gestire i soci». Occorre sapere quali operazioni sono necessarie, quale comportamento è corretto in condizioni normali e che cosa deve succedere nei principali casi limite.

Per l'associazione del nostro esempio, una prima proposta potrebbe essere:

| Dimensione | Proposta per la prima versione | Stato |
| --- | --- | --- |
| Utente | Un amministrativo su un computer dell'associazione | Da confermare |
| Soci | Creare, trovare, modificare e disattivare | Da confermare |
| Quote | Registrare importo, data e legame con il socio | Da confermare |
| Storico | Mantenere le quote dopo la disattivazione | Da confermare |
| Rete | Uso locale, senza accesso pubblico | Da confermare |
| Interfaccia | Moduli chiari e messaggi comprensibili | Da confermare |
| Recupero | Definire frequenza dei backup e perdita tollerata | Decisione aperta |
| Esclusioni | Niente pagamenti online nella prima versione | Da confermare |

Questa tabella non inventa una conferma. Presenta proposte che il CLIENT può accettare o modificare. Una volta confermate, le decisioni diventano l'autorità di prodotto corrente. Una modifica futura deve essere registrata come supersessione, mantenendo chiara la provenienza della scelta.

Un requisito ben formulato contiene anche una condizione di verifica. «Ritrovare un socio dopo aver riavviato il programma» è osservabile. «Usare un'architettura robusta» è un obiettivo tecnico importante, ma deve essere tradotto in controlli specifici da chi ne è responsabile.

La documentazione dovrebbe distinguere gli aspetti confermati, quelli dedotti da evidenze tecniche e quelli ancora aperti. Non serve trasformare ogni piccola scelta di interfaccia in una nuova campagna strategica, ma i comportamenti che possono causare perdita di dati o alterare il prodotto non devono restare impliciti.

## 5. Stabilire baseline tecnica e piano delle consegne

Una volta chiarita la direzione del prodotto, il Planner definisce la baseline tecnica. Deve contenere informazioni verificabili sullo stack, sulle versioni rilevanti, sulla persistenza, sui confini di sicurezza e rete, sulle modalità di esecuzione e sugli obblighi di recupero. Le preferenze personali non sono sufficienti se contraddicono il codice o l'ambiente effettivo.

Per una piccola applicazione locale una base dati incorporata potrebbe essere adeguata. Se in seguito il prodotto richiede modifiche simultanee da molti utenti, serve una nuova valutazione. La scelta corretta considera concorrenza, capacità, integrità, manutenzione e costo, non soltanto la familiarità dell'agente con una tecnologia.

Il piano delle consegne ordina capacità effettivamente utili. Per esempio: prima anagrafica soci, poi quote, poi elenco degli arretrati. Ogni fase ha dipendenze e criteri riconoscibili. Non occorre anticipare tutto il possibile sviluppo futuro né inventare una data di rilascio che il CLIENT non ha confermato.

Priorità e rischio si influenzano. Una migrazione potenzialmente distruttiva richiede prove e strategia di recupero più approfondite. Una modifica visiva può essere meno rischiosa sul piano dei dati, ma richiedere una verifica umana dell'esperienza. La pianificazione deve identificare quali controlli sono veramente necessari per la capacità scelta.

Gli schemi e strumenti di validazione controllano la forma della baseline. Non certificano automaticamente la verità dei valori. Un documento perfettamente valido può contenere l'hash sbagliato o descrivere un ambiente che nessuno ha mai avviato. La verifica delle fonti fisiche resta indispensabile.

## 6. Effettuare un'adozione fondata su prove

Adottare il progetto significa promuovere informazioni verificate in uno stato di controllo utilizzabile. È un passaggio distinto dallo scaffold. Prima si osserva, poi si conferma, infine si applica una specifica di adozione coerente.

Il preflight confronta riferimenti, file, identità, obblighi e stato esistente. Se una superficie canonica è già governata da un altro sistema, l'operazione non deve sovrascriverla automaticamente. Se manca una prova di currentness, il sistema deve segnalarla e fermare soltanto ciò che dipende materialmente da quel dato.

Gli strumenti [discover_project.py](../../../../tools/discover_project.py), [apply_adoption.py](../../../../tools/apply_adoption.py) e [reconstruct_context.py](../../../../tools/reconstruct_context.py) coprono fasi diverse. Discovery raccoglie elementi osservabili, adoption promuove la configurazione verificata e reconstruction prova che lo stato corrente sia recuperabile.

Le chiamate precise dipendono dalla versione installata e dalle istruzioni contenute nel suo repository. Non si dovrebbero copiare comandi di una release precedente senza confrontarli. La presenza di un pulsante o una voce di menu in un editor non sostituisce la verifica dell'effetto reale.

Se l'adozione fallisce, conservate il rapporto e diagnosticate il motivo. Un conflitto di proprietà, una referenza a una migrazione assente e un requisito non approvato richiedono interventi diversi. Correggete la causa sulla superficie proprietaria e ripetete la verifica pertinente. Non create un secondo Product State concorrente.

## 7. Verificare il passaggio a una nuova sessione

Il test più importante di questo capitolo è eseguire una ricostruzione in un contesto fresco. Un nuovo esecutore, privo della memoria della chat originale, deve identificare:

- scopo e utenti del prodotto;
- requisiti correnti confermati e decisioni aperte;
- fonte precisa del codice e stato dei dati;
- baseline tecnica e vincoli di distribuzione;
- responsabile delle decisioni strategiche e operative;
- eventuale campagna autorizzata e suo gate corrente;
- evidenza più forte disponibile per le capacità esistenti;
- prossima azione consentita e operazioni ancora vietate.

Se la risposta richiede al CLIENT di raccontare di nuovo tutto, il trasferimento non è ancora valido. La soluzione è migliorare la superficie canonica mancante, non produrre una nuova sintesi priva di riferimenti. A volte basta un collegamento corretto a un file già esistente; altre volte serve riconciliare dati realmente contraddittori.

Anche l'informazione negativa è preziosa. «La funzione è stata testata solo con dati fittizi», «nessun provider esterno è autorizzato» oppure «la migrazione di produzione resta sconosciuta» sono fatti che impediscono a un futuro agente di compiere un'azione pericolosa.

La ricostruzione deve essere ripetibile. Se due sessioni, leggendo le stesse fonti correnti, raggiungono versioni incompatibili della realtà, c'è un difetto di ownership o di riferimento da risolvere.

## 8. Autorizzare la prima campagna ingegneristica

Con requisiti e baseline adottati, il Planner può definire il primo charter. Prima considera il prodotto end-to-end, i punti di dipendenza, i dati, le interfacce, i rischi, i limiti operativi e i criteri di accettazione. Una prima analisi strategica viene seguita da una revisione avversariale distinta, adatta all'importanza della decisione.

Il charter descrive una capacità: che cosa si vuole ottenere, perché, quali confini sono autorizzati, chi possiede la realizzazione, quali interfacce devono restare coerenti, quali gate servono e quali fatti invaliderebbero la decisione. Non è un elenco rigido di micro-task.

Una prima capacità sensata è «registrare un socio con dati obbligatori, assegnargli un'identità stabile e ritrovarlo dopo il riavvio». Si può consegnare e verificare come un percorso completo, senza dover costruire in anticipo ogni funzione contabile futura.

Una volta autorizzato il charter, I3 coordina implementazione, test, debugging e integrazione. I2 torna per la verifica strategica terminale o quando emerge una vera modifica dei confini. Un errore di validazione all'interno del charter non richiede una nuova analisi strategica totale.

## 9. Un colloquio concreto con il CLIENT

Il CLIENT dice: «Vorrei sostituire i fogli di calcolo con un piccolo programma per i soci e le quote. Lo userà una persona e per ora deve restare locale. Non voglio abbonamenti esterni».

Il Planner risponde prima sul problema: «Confermo che la prima necessità è registrare e ritrovare un socio in modo affidabile. Che cosa deve succedere allo storico se il socio viene disattivato? Quali dati sono obbligatori? Quale recupero vi serve se il computer si guasta?».

Il CLIENT chiarisce le regole. Il Planner verifica il repository e i dati disponibili, propone la baseline tecnica e mostra un piano con capacità successive. Il CLIENT conferma il lato funzionale, mentre Engineering sceglie implementazione e test.

Prima di avviare la campagna, una nuova sessione ricostruisce il contesto direttamente dal repository. Se manca un collegamento essenziale, lo si corregge. Soltanto dopo la prima capacità viene affidata al controller con limiti e verifiche chiari.

## 10. Criteri per dichiarare pronta la baseline

La baseline è sufficientemente pronta quando un lettore esterno sa quale prodotto costruire, quali requisiti siano stati confermati, quale codice e ambiente siano reali, chi possa prendere la prossima decisione e quale lavoro sia effettivamente permesso.

Non è necessario anticipare ogni futuro dettaglio. È necessario non nascondere le incertezze materiali. Un elenco infinito di documenti non sostituisce la prova di continuità. La qualità della baseline si misura dalla capacità di guidare la prima consegna senza confusione e di resistere al passaggio a un altro contesto.

Se il processo diventa troppo pesante per una piccola applicazione, riducete la complessità organizzativa mantenendo le regole essenziali: intenzione confermata, fonte corrente, responsabilità, prova e prossima azione. La proporzione è parte dell'architettura, non un compromesso vergognoso.

**Segue:** capitolo 03, Lavoro quotidiano.

## Fonti e limiti

- [Discovery, requisiti e baseline](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Trasferimento e adozione](../../../16_TRANSFER_ADOPTION.md)
- [Planner Kernel](../../../../protocols/PLANNER_KERNEL.md)
- [Sessione di discovery](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md)
- [Strumento di discovery](../../../../tools/discover_project.py)
- [Strumento di adozione](../../../../tools/apply_adoption.py)
- [Ricostruzione del contesto](../../../../tools/reconstruct_context.py)

Le proposte relative all'associazione sono illustrative. Non costituiscono requisiti confermati per un altro progetto.
