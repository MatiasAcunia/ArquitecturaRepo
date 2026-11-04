# 04 — Richiedere modifiche al prodotto

ArquitecturaRepo · Manuale completo per l'utente · Edizione v1.4 · Italiano

> Il CLIENT deve poter formulare desideri e correzioni senza assumersi il lavoro di progettazione tecnica. Questo capitolo segue il [confine delle decisioni del CLIENT](../../../../protocols/CLIENT_BOUNDARY.md) e il [processo di definizione dei requisiti](../../../../protocols/PRODUCT_DISCOVERY_REQUIREMENTS_AND_TECHNICAL_BASELINE.md).

## Contenuti

1. Descrivere il risultato prima del codice
2. Un brief breve ma sufficiente
3. Decisioni dell'utente e del team tecnico
4. Cambiare idea mantenendo la storia
5. Formulare aspettative di qualità
6. Stabilire priorità realistiche
7. Quando una domanda al CLIENT è indispensabile
8. Cinque esempi concreti
9. Nuovo requisito o bug interno?
10. Un risultato funzionante ma inutile
11. Una conversazione di priorità

## 1. Descrivere il risultato prima del codice

Quando si lavora con un agente di programmazione è naturale chiedere direttamente una soluzione: «Aggiungi una nuova tabella», «usa Redis» oppure «riscrivi il servizio». Il problema è che queste richieste tecniche possono nascondere una necessità più semplice. Se il vero obiettivo è trovare un socio rapidamente, può bastare migliorare l'indice esistente invece di introdurre un servizio aggiuntivo.

Il punto di partenza migliore è il comportamento osservabile. Chi usa la funzione? Che cosa prova a fare? Quale risultato deve ottenere? In quali condizioni oggi fallisce? Quali parti del prodotto non devono cambiare? La risposta permette al Planner di scegliere una capacità completa e al Controller di decidere l'implementazione.

Un cambiamento ben descritto non deve essere lungo. «L'amministrativo deve poter filtrare le quote per mese, vedere il totale e correggere un errore di input senza perdere i dati già inseriti» è già molto più chiaro di «rifai la tabella delle quote».

Questo metodo non vieta al CLIENT di imporre vincoli tecnici. Se l'applicazione deve funzionare offline o integrarsi con una piattaforma imposta da un contratto, sono requisiti legittimi. Semplicemente, non bisogna trasferirgli le scelte ordinarie di classi, query e protocolli quando non sono decisioni di prodotto.

## 2. Un brief breve ma sufficiente

Una buona richiesta di modifica comprende quattro parti: contesto, risultato, limiti e modo di verificare. Può aggiungere priorità e data se queste cambiano realmente il lavoro.

Esempio:

> Come responsabile amministrativo voglio consultare tutte le quote scadute di un mese. L'elenco deve indicare socio, importo e scadenza, senza mostrare a utenti non autorizzati i contatti personali. Non devono essere modificati i pagamenti già registrati. Nella prima versione non serve esportare in Excel; desidero prima verificare che i numeri siano corretti.

Il Planner può tradurre questa richiesta in requisiti, dipendenze e criteri di accettazione. I3 decide il percorso tecnico: query, servizio, interfaccia, test e gestione degli errori. La separazione permette di correggere i dettagli senza richiedere nuove istruzioni al CLIENT ogni volta.

Se non è ancora chiaro come gestire un caso particolare, indicatelo come domanda aperta. Per esempio: «Non so se le quote pagate in ritardo debbano ancora apparire nello storico degli arretrati; spiegatemi le conseguenze prima di decidere». Una domanda aperta è meglio di un comportamento inventato in autonomia.

Le richieste più rischiose devono aggiungere informazioni sui dati e sugli effetti esterni. Un nuovo invio automatico di email reali richiede una valutazione diversa da una notifica interna simulata. Un'esportazione con nomi e contatti necessita di controlli di autorizzazione e gestione sicura del file.

## 3. Decisioni dell'utente e del team tecnico

Il CLIENT decide che cosa conta per l'utilizzatore: regole, visibilità, priorità, qualità percepita, costi e pubblicazione. Engineering risponde delle scelte tecniche e delle verifiche: architettura, persistenza, migrazioni, logging, error handling, test e recupero.

Un cliente che chiede un backup deve descrivere quanto storico vuole proteggere e quale perdita recente sia tollerabile. Non dovrebbe dover decidere se usare snapshot, journal o una particolare chiamata di filesystem. Il team tecnico progetta una soluzione coerente con il prodotto e spiega le eventuali conseguenze su tempo e budget.

Se le scelte tecniche presentano alternative che cambiano il comportamento visibile, la decisione torna al CLIENT. Una sincronizzazione eventuale tra più dispositivi, per esempio, potrebbe mostrare dati non immediatamente aggiornati. Questo effetto è una questione di prodotto, anche se viene originato da un compromesso architetturale.

Lo stesso vale per permessi sensibili. Il fatto che una API sia accessibile o che un token esista non autorizza invii reali, pagamenti, pubblicazione di dati personali o operazioni irreversibili. Le richieste devono essere interpretate alla luce delle responsabilità e dei limiti confermati.

## 4. Cambiare idea mantenendo la storia

Durante lo sviluppo si scoprono bisogni che all'inizio non erano evidenti. Il CLIENT può cambiare direzione. Forse un prodotto pianificato per un solo computer deve ora funzionare in due sedi. Forse un report non risponde alla domanda del consiglio direttivo. Questo apprendimento è normale e deve poter aggiornare il prodotto.

La modifica va registrata come nuova decisione corrente. Il precedente requisito resta una fonte storica, ma non deve più guidare silenziosamente il lavoro quando è stato sostituito. Il Planner valuta le conseguenze sui dati, sul codice, sulle campagne attive e sul piano di consegna.

Una nuova decisione importante può invalidare il charter. Passare da un'applicazione locale a un servizio Internet modifica autenticazione, deployment, sicurezza e disponibilità; non dovrebbe essere trattato come un semplice refactoring interno. Serve una rivalutazione strategica appropriata.

Al contrario, una correzione del colore di una notifica già previsto come parte della qualità della stessa schermata può restare nel charter esistente. Non è necessario creare una campagna nuova per ogni dettaglio quando l'obiettivo resta invariato.

Non cancellate indiscriminatamente documenti precedenti. Una tracciabilità delle supersessioni consente di capire perché una scelta era valida ieri e non lo è oggi. Questo riduce contraddizioni apparenti e aiuta una nuova sessione a ricostruire la vera intenzione attuale.

## 5. Formulare aspettative di qualità

La qualità non coincide soltanto con test automatici. Un'interfaccia può salvare correttamente un socio ma richiedere troppi passaggi, usare termini incomprensibili o rendere difficili gli errori più comuni. Il CLIENT può chiedere un risultato leggibile, coerente, accessibile e facile da imparare.

Una buona richiesta può essere: «Una persona che non conosce la struttura del database deve riuscire a inserire un socio senza istruzioni speciali. I campi obbligatori devono essere evidenti, e in caso di dati duplicati il sistema deve spiegare come procedere».

Questa formulazione chiarisce un gate percettivo senza prescrivere il framework grafico. Engineering definisce e realizza l'implementazione. La persona incaricata della valutazione dell'interfaccia prova il percorso reale. Un test unitario non sostituisce la verifica che l'utente capisca una schermata.

L'aspettativa può riguardare anche affidabilità: «Nessun pagamento deve comparire due volte in seguito a un doppio click». Questo comportamento va convertito in controlli di idempotenza, persistenza e integrazione. Il CLIENT definisce la semantica, I3 la tecnica.

Non serve rendere ogni preferenza un criterio matematico. Alcuni giudizi richiedono una vera valutazione umana. È però utile spiegare concretamente il difetto osservato e conservare un candidato identificabile per verificare la correzione.

## 6. Stabilire priorità realistiche

Aprire dieci Goal contemporanei per dieci desideri non produce necessariamente una consegna più rapida. Le richieste possono condividere dati, configurazione e risorse, oppure dipendere l'una dall'altra. Il Planner deve mostrare la sequenza che porta più rapidamente a una capacità utilizzabile senza trascurare rischi reali.

Supponiamo che l'associazione chieda categorie di soci, promemoria email, un riepilogo delle quote e una nuova homepage. Il riepilogo potrebbe dipendere dalle categorie; l'invio email coinvolge permessi e dati; la homepage può essere quasi indipendente se non modifica gli stessi componenti.

Il CLIENT assegna priorità dal punto di vista dell'utilità: ciò che serve davvero prima della data obiettivo, ciò che è importante ma rinviabile, ciò che resta fuori dalla prima versione. Il Planner integra le dipendenze tecniche e propone un percorso realistico.

Una prima consegna non deve essere soltanto un prototipo finto che sembra completo. Può essere volutamente piccola, ma il suo comportamento essenziale deve funzionare, compresa la gestione degli errori e la persistenza quando necessaria. Una piccola capacità reale fornisce feedback migliore di una grande promessa senza prove.

Il principio di proporzione vale anche per la documentazione. Non si dovrebbe spendere più tempo a creare nuove campagne e passaggi formali che a risolvere le incertezze che contano. L'obiettivo è sbloccare valore, non massimizzare il numero di artefatti amministrativi.

## 7. Quando una domanda al CLIENT è indispensabile

Una domanda è indispensabile quando una scelta di prodotto non confermata cambia materialmente ciò che verrà realizzato. Eliminare definitivamente un socio o conservarlo come disattivato è un esempio. Permettere o meno l'accesso pubblico a un report con dati personali è un altro.

Non è invece necessario interrogare il CLIENT per un test di regressione fallito, una correzione di parsing o una migrazione interna già compresa nel charter. Questi casi rientrano nella responsabilità tecnica, purché non introducano nuove conseguenze importanti.

Una buona domanda presenta le alternative dal punto di vista dell'utente: «Se nascondiamo i soci disattivati, la ricerca quotidiana è più semplice, ma per vedere le quote storiche dovrai aprire l'archivio. Se li lasciamo visibili con un filtro, avrai un elenco più lungo ma accesso immediato. Quale flusso è migliore per il tuo lavoro?».

Il CLIENT può decidere senza conoscere query SQL o classi Java. Il team tecnico si assume la responsabilità della traduzione nel sistema. Questa è una distinzione strutturale, non una questione di cortesia.

Se due requisiti confermati sono incompatibili, il Planner deve esplicitare il conflitto. Non deve scegliere arbitrariamente quello più facile da implementare. Una scelta tracciabile evita che in seguito il comportamento del prodotto venga giustificato con una presunta decisione mai presa.

## 8. Cinque esempi concreti

**Ricerca soci:** «L'operatore deve trovare una persona per nome o codice. I soci inattivi devono essere consultabili tramite un filtro e la ricerca non deve alterare i dati». Il comportamento è verificabile senza imporre un indice specifico.

**Pagamento quota:** «Dopo aver registrato una quota, l'operatore deve vederla nello storico. Un doppio click non deve creare due pagamenti». Questa richiesta rende esplicito un rischio di integrità da trattare tecnicamente.

**Disattivazione:** «Un socio disattivato non può prenotare nuove attività; i pagamenti precedenti restano consultabili». La regola collega più capacità e richiede coerenza del modello.

**Report del consiglio:** «Il report mensile deve mostrare importi e conteggi senza esporre inutilmente indirizzi personali. Solo gli autorizzati possono aprirlo». Il vincolo riguarda sia utilità sia privacy.

**Interfaccia:** «Le operazioni quotidiane devono essere riconoscibili senza termini tecnici; in caso di errore il messaggio deve spiegare che cosa correggere». Questo enunciato porta a un gate di verifica umana.

Il Planner può trasformare ciascun esempio in criteri tecnici di accettazione. Si devono osservare casi positivi, limiti, permessi, persistenza e qualità pertinente. I dettagli implementativi restano nella competenza di Engineering.

## 9. Nuovo requisito o bug interno?

Un bug è un comportamento che non soddisfa la decisione già confermata. Se la ricerca deve trattare correttamente i nomi con accenti e non lo fa, I3 corregge nel charter esistente. Una nuova richiesta cambia invece il risultato autorizzato. Collegare la ricerca a una banca dati esterna introduce un nuovo confine.

Un difetto ripetuto non diventa automaticamente un nuovo prodotto. Se cinque correzioni superficiali falliscono, il controller deve investigare in modo sistemico il sottosistema e ottenere una revisione indipendente. Nuovi Planner PASS non riparano di per sé problemi di implementazione.

Al contrario, una decisione sul trattamento di pagamenti reali, su un nuovo deployment pubblico o sulla cancellazione irreversibile di dati deve essere portata all'autorità giusta. Chiamarla «piccola modifica tecnica» non riduce il rischio né crea il permesso mancante.

La classificazione serve anche al tempo del CLIENT. Una governance ben costruita non gli restituisce bug ordinari da coordinare. Gli presenta domande concrete quando una decisione personale o di business è effettivamente necessaria.

## 10. Un risultato funzionante ma inutile

Può accadere che il codice sia corretto e che la funzione non risolva il problema. Un report può calcolare perfettamente la somma delle quote pagate, mentre il consiglio voleva vedere quelle scadute. Un'interfaccia può salvare ogni modifica ma richiedere un percorso troppo complesso per la routine quotidiana.

Il CLIENT può rifiutare il risultato e spiegare che cosa manca: «Posso trovare le informazioni, ma ho bisogno di vedere subito le quote in ritardo, senza aprire ogni socio». Questa osservazione non è un difetto di test unitario; riguarda il significato e l'esperienza dell'applicazione.

Il Planner determina se il comportamento era già previsto dai requisiti o se si tratta di una nuova necessità emersa durante l'uso. La distinzione decide se I3 deve correggere all'interno della campagna o se serve una nuova scelta strategica.

Una valutazione umana non va falsificata per ottenere un PASS. Se l'utente non ha mai provato il flusso, la qualità percettiva resta non dimostrata. Allo stesso tempo non bisogna prolungare indefinitamente una campagna alla ricerca di difetti microscopici dopo che i criteri concordati sono davvero soddisfatti.

## 11. Una conversazione di priorità

Per preparare una modifica, bastano spesso cinque domande: chi vive il problema, quale risultato deve cambiare, quali dati o regole vanno conservati, quale priorità domina e quale decisione ancora aperta può modificare sostanzialmente il lavoro.

Una volta raccolte queste informazioni, il Planner verifica il codice corrente, analizza le dipendenze e formula una capacità ragionevole. I3 realizza e prova l'intervento. Il CLIENT interviene per approvare il comportamento e giudicare l'esperienza, non per prescrivere ogni tentativo di debug.

Se emergono esigenze diverse, registratele con il loro stato: confermate, proposte o escluse. Una lista di desideri non dovrebbe trasformarsi silenziosamente in dieci promesse di consegna. Ogni capacità deve avere confini comprensibili e una prova applicabile.

La buona richiesta di modifica tutela sia la libertà tecnica sia l'autorità dell'utente. Permette a chi sviluppa di scegliere la soluzione adeguata e a chi userà il prodotto di riconoscere quando l'esito desiderato è stato raggiunto.

**Segue:** capitolo 05, Errori e recupero.

## Fonti e limiti

- [Confine del CLIENT](../../../../protocols/CLIENT_BOUNDARY.md)
- [Product discovery e baseline](../../../../protocols/PRODUCT_DISCOVERY_REQUIREMENTS_AND_TECHNICAL_BASELINE.md)
- [Planner Kernel](../../../../protocols/PLANNER_KERNEL.md)
- [Piano di consegna e requisiti](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Charter di campagna](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Ciclo di vita delle capacità](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)

Le richieste illustrate riguardano il caso fittizio dell'associazione e non costituiscono decisioni per un altro prodotto.
