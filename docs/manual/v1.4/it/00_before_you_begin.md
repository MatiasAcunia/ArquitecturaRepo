# 00 — Prima di iniziare

ArquitecturaRepo · Manuale completo per l'utente · Edizione v1.4 · Italiano

> Questo capitolo spiega che cosa offre il framework, quali responsabilità separa e quali risultati non può garantire da solo. Si riferisce alla [release pubblicata v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0); per le istruzioni effettive di installazione consultare la [guida pubblica corrente](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) e le [note di versione](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md).

## Orientamento

1. Che cosa viene installato davvero
2. Perché serve un sistema oltre alla conversazione
3. Responsabilità del CLIENT e dei quattro ruoli interni
4. Evidenze, stato corrente e memoria
5. Distinguere intenzione, modello e implementazione
6. Un primo utilizzo proporzionato
7. Come leggere gli otto capitoli
8. Decisioni riservate all'utente
9. Un esempio dall'idea all'accettazione
10. Come misurare il valore del framework

## 1. Che cosa viene installato davvero

ArquitecturaRepo è una struttura portabile per organizzare lo sviluppo del software intorno a requisiti, responsabilità, evidenze e continuità. Contiene protocolli pubblici, modelli riutilizzabili, profili di installazione, contratti verificabili e strumenti Python per convalidare e ricostruire alcuni stati. È disponibile anche un controller locale opzionale per determinati stati delle campagne di sviluppo. Non è un servizio che, appena installato, trasforma automaticamente qualunque descrizione in un'applicazione pronta.

Il punto centrale è distinguere il controllo del processo dal prodotto finale. Il framework può aiutare a registrare quali decisioni restano valide, quali modifiche sono autorizzate, quale versione del codice è stata provata e che cosa deve fare la prossima sessione. Non sostituisce la comprensione del problema, l'architettura, la programmazione effettiva, la protezione dei dati o la valutazione della qualità da parte di un essere umano.

La release pubblica v1.4.0 è identificata da un tag e da artefatti distribuiti con checksum e manifest. La presenza di una pagina più recente sul ramo main non significa che quella pagina facesse parte dello ZIP pubblicato in precedenza. Quando si installa uno starter verificabile, bisogna controllare l'identità della distribuzione effettivamente utilizzata, non soltanto la stringa della versione.

Anche i test della release hanno un ambito preciso. Possono dimostrare che una struttura portabile si installa e si verifica nelle condizioni previste. Non dimostrano che una diversa applicazione, realizzata successivamente con il framework, sia sicura, integrata, usabile o pronta per la produzione. Gli esempi sintetici del repository sono costruiti per esercitare i meccanismi: non sono clienti reali né approvazioni operative.

Il sistema non richiede un particolare provider di intelligenza artificiale. È possibile svolgere ruoli di pianificazione e sviluppo con persone, strumenti locali o agenti esplicitamente autorizzati. L'installazione non configura in modo implicito credenziali, non abilita spese esterne e non concede il permesso di pubblicare software o dati.

## 2. Perché serve un sistema oltre alla conversazione

Lavorare con un assistente di programmazione in una singola chat può essere molto produttivo. Si chiede una modifica, si riceve del codice, si prova e si corregge. Questo metodo è spesso sufficiente per un esperimento piccolo e temporaneo. I problemi diventano più evidenti quando il progetto dura settimane, attraversa molte conversazioni o coinvolge più persone.

Un nuovo agente può non conoscere tutte le decisioni precedenti. Una vecchia risposta può descrivere un ramo che non è più attuale. Una funzione dichiarata completata può essere stata modificata dopo il test. Il CLIENT finisce allora per ripetere la storia del prodotto, correggere interpretazioni incoerenti e coordinare manualmente i passaggi tecnici.

ArquitecturaRepo tenta di ridurre questa dipendenza dalla memoria conversazionale attraverso superfici canoniche nel repository. Le decisioni importanti, le condizioni di autorizzazione, i riferimenti al codice e le prove devono essere ricostruibili. Una nuova sessione dovrebbe capire l'obiettivo del prodotto, le capacità già ottenute, i rischi aperti e l'azione successiva consentita senza dover leggere ogni messaggio della chat originale.

Non è corretto affermare che questo approccio sia sempre superiore a una chat diretta. Introduce un costo di organizzazione e manutenzione. Per uno script da usare una sola volta, il costo può essere maggiore del beneficio. Per un'applicazione che evolve, conserva dati o deve sopravvivere a passaggi di consegne, la tracciabilità può evitare lavoro ripetuto e decisioni sbagliate. Il confronto onesto misura risultati reali, non quantità di protocolli.

Per valutare la differenza, si può prendere la stessa piccola funzionalità e osservare non soltanto quanto rapidamente viene scritto il primo codice, ma anche come si gestisce una modifica dei requisiti, come un nuovo esecutore riprende il lavoro e quanta evidenza resta dopo l'accettazione. I due metodi possono produrre codice; l'interesse del framework è soprattutto mantenere l'evoluzione comprensibile.

## 3. Responsabilità del CLIENT e dei quattro ruoli interni

Il CLIENT rappresenta il proprietario dell'intenzione di prodotto. Decide quale problema risolvere, chi utilizzerà il sistema, quali comportamenti sono importanti, quale qualità percepita è accettabile e quali limiti economici o di pubblicazione esistono. Può respingere un'interfaccia tecnicamente funzionante se risulta confusa. Non dovrebbe però dover risolvere conflitti Git o progettare i test per permettere al team di continuare.

Il framework distingue quattro classi interne di responsabilità:

| Ruolo | Responsabilità principale | Limite |
| --- | --- | --- |
| I1 Master Owner, quando necessario | Coerenza tra prodotti, risorse condivise e problemi sistemici | Non diventa il Planner di ogni piccola attività |
| I2 Planner | Interpretazione del prodotto, strategia, architettura e criteri di accettazione | Non gestisce i singoli tentativi di debugging |
| I3 Execution Controller | Implementazione, test, integrazione, recupero e revisioni nella campagna autorizzata | Non inventa nuove decisioni di prodotto |
| I4 Specialisti e revisori | Lavoro tecnico circoscritto e verifiche indipendenti | Non sostituiscono autorizzazioni strategiche o del CLIENT |

Quattro classi di ruolo non significano quattro modelli di intelligenza artificiale o quattro processi sempre attivi. Un progetto semplice può avere una sola persona che svolge diverse funzioni, mantenendo però chiare le responsabilità e cercando una revisione realmente indipendente dove il rischio lo richiede.

La distinzione decisiva è tra progettare una capacità e realizzarla. I2 comprende il problema, stabilisce confini e criteri, poi autorizza una campagna. Da quel momento I3 gestisce il lavoro concreto: correzioni, test, refactoring interno, integrazione e recupero. Un bug ordinario non deve generare una nuova campagna né obbligare il CLIENT a scegliere l'algoritmo di correzione.

Un cambiamento sostanziale dei requisiti è diverso. Se il CLIENT trasforma una piccola applicazione locale in un servizio pubblico su Internet, bisogna rivalutare autenticazione, sicurezza, dati personali, distribuzione e costi. Non sarebbe responsabile trattarlo come un semplice dettaglio della campagna esistente.

## 4. Evidenze, stato corrente e memoria

Per stabilire che cosa esiste tecnicamente, si parte da prove fisiche: file, Git, configurazione, database, artefatti e stato di runtime. Poi si controllano le superfici canoniche correnti, i requisiti confermati e le autorizzazioni attive. Un riepilogo di chat può orientare la ricerca, ma non prevale su evidenze tecniche più recenti.

L'intenzione del CLIENT segue una regola complementare. Una decisione esplicita successiva può sostituire una preferenza precedente. La nuova scelta deve però essere riportata nella descrizione corrente del prodotto, con una supersessione comprensibile. Né un documento vecchio né un assistente che indovina possono sostituire una decisione riservata all'utente.

Quando una prova fondamentale manca, il valore corretto è sconosciuto, non PASS. Se due fonti attive si contraddicono, la modifica materiale che dipende dal conflitto si ferma fino alla riconciliazione. La diagnosi in sola lettura può proseguire. Il sistema deve saper dire con precisione che cosa non sa.

Il livello di controllo generato si chiama normalmente .agentic-sdlc/. Il suo stato iniziale HOLD / UNTRUSTED_CONTEXT è intenzionale. Significa che i dati di esempio non sono stati scambiati per realtà del progetto. Solo una scoperta verificata e un'adozione coerente permettono di promuovere i fatti necessari a uno stato operativo.

L'attualità di un dato non deriva dal suo nome. Una cartella chiamata CURRENT può contenere un riferimento obsoleto. Un commit appena creato può non coincidere con il database realmente in uso. Currentness è il legame dimostrabile fra autorità, codice, configurazione, dati e prove nel momento in cui si pretende di lavorare o accettare un risultato.

## 5. Distinguere intenzione, modello e implementazione

Per leggere il progetto senza confondere piani diversi sono utili tre livelli. L0 raccoglie ciò che il CLIENT ha realmente chiesto, chiarito o autorizzato. L1 contiene l'interpretazione confermata: requisiti attuali, modello del prodotto e Product State. L2 raccoglie il codice, i database, le campagne, gli esiti dei test e gli altri artefatti tecnici.

Una funzione può essere ben descritta in L1 e mancare ancora in L2. Oppure può essere implementata in L2 ma non corrispondere al significato richiesto in L0. In entrambi i casi non basta un messaggio di successo. Il team deve poter risalire dalla capacità osservabile alla decisione che l'ha giustificata e al candidato che la realizza.

Questa separazione permette anche di individuare una promessa prematura. «L'applicazione gestisce i pagamenti» può significare soltanto che esiste una schermata dimostrativa, oppure che vengono registrati contributi locali, oppure che vengono realmente eseguite transazioni esterne. Sono capacità molto diverse e richiedono autorizzazioni e prove differenti.

Il modello corrente dovrebbe dire quale di queste affermazioni è stata confermata e quale no. Una buona architettura rende le differenze visibili invece di nasconderle sotto etichette generiche come pronto o completato.

## 6. Un primo utilizzo proporzionato

Per iniziare, scegliete il profilo più piccolo adeguato ai rischi. SMALL è spesso sufficiente per un esperimento senza complessità persistente; STATEFUL è più adatto quando l'applicazione conserva dati importanti; altri profili trattano artefatti pesanti, più workstream, più prodotti o conseguenze particolarmente rilevanti.

Il primo passo non è avviare decine di agenti. È scrivere una breve descrizione del prodotto e verificare il repository reale. Chi sono gli utenti? Quale azione devono poter compiere? Quali dati sono coinvolti? Quale ambiente verrà usato? Che cosa è escluso dalla prima versione? Che cosa resta da decidere?

Il Planner ricostruisce poi il codice esistente, propone la base tecnica e organizza una prima capacità utile. Prima di autorizzare il lavoro, si verifica che una nuova sessione possa comprendere i riferimenti correnti senza l'intera conversazione originale. In mancanza di questa continuità, conviene correggere le informazioni alla fonte invece di produrre altro codice sulla base di ipotesi.

La [guida di installazione](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) è il riferimento pratico per i comandi; il capitolo 01 li spiega in dettaglio. Non è necessario memorizzare subito l'intero manuale per provare un profilo semplice.

## 7. Come leggere gli otto capitoli

| Capitolo | Quando consultarlo | Risultato atteso |
| --- | --- | --- |
| 00 · Prima di iniziare | Prima dell'adozione | Comprendere scopo, responsabilità e limiti |
| 01 · Installazione | Quando si prepara un progetto | Verificare la distribuzione e creare il controllo iniziale |
| 02 · Planner e adozione | Prima della prima capacità | Ricostruire requisiti e base tecnica attuale |
| 03 · Lavoro quotidiano | Durante lo sviluppo | Continuare nella campagna autorizzata |
| 04 · Richiedere modifiche | Quando cambiano i bisogni | Esplicitare effetto, priorità e confini |
| 05 · Errori e recupero | Dopo un incidente | Preservare prove e recuperare con sicurezza |
| 06 · Accettazione | Quando qualcuno dice «finito» | Valutare candidato, gate e qualità umana |
| 07 · Esempio di associazione | Per esercitare l'intero ciclo | Seguire un prodotto fittizio dall'idea alla verifica |

Le [otto mini guide](../../../i18n/MINI_GUIDE_it.md) e le FAQ restano utili come introduzione breve. Non diventano automaticamente la traduzione completa di questo libro. Il manuale spagnolo v1.3 viene conservato separatamente come fonte storica e non viene riscritto per simulare il comportamento della v1.4.

## 8. Decisioni riservate all'utente

Un buon brief iniziale può essere molto semplice: «Voglio un'applicazione locale per registrare i soci e le quote della nostra associazione. La userà un amministrativo. Non voglio pagamenti online nella prima versione. La cronologia delle quote deve restare disponibile e l'interfaccia deve essere leggibile».

Queste informazioni orientano il prodotto senza prescrivere l'architettura. Il CLIENT può aggiungere limiti di tempo, accessibilità, budget e uso di servizi esterni. Può anche lasciare aperte questioni sulle quali non ha ancora deciso. La squadra tecnica deve chiarire solo quelle che cambiano materialmente il risultato.

Non serve che il CLIENT scelga il database, il framework web, il numero di branch o la struttura delle classi. Engineering propone e giustifica tali scelte in relazione al contesto. Se una tecnologia impone conseguenze importanti per costi, privacy o uso, queste vengono spiegate prima di richiedere la decisione riservata.

## 9. Un esempio dall'idea all'accettazione

L'associazione vuole eliminare una gestione fragile dei soci. Il CLIENT conferma che i pagamenti storici non devono sparire quando una persona viene disattivata. Il Planner osserva prima il repository, verifica se esistono dati e applicazioni precedenti, poi definisce una prima capacità che consenta di creare e ritrovare un socio.

I3 implementa il percorso completo, scrive test e gestisce le correzioni. Un test trova duplicati; il controller indaga la causa, corregge e verifica di nuovo nello stesso charter. Il Planner non deve ridisegnare la campagna a ogni bug, e il CLIENT non deve spiegare come creare un vincolo di unicità.

Quando il candidato è pronto, vengono controllati separatamente il comportamento del codice, l'integrazione con i dati, la situazione reale di esecuzione e la comprensibilità dell'interfaccia. Il CLIENT valuta ciò che gli compete: se la gestione dei soci è realmente comoda e coerente con il bisogno espresso.

Un resoconto positivo da solo non chiude la capacità. L'accettazione deve riferirsi a una versione identificabile e a prove adeguate. Il capitolo 07 sviluppa lo scenario con due capacità collegate: soci e quote.

## 10. Come misurare il valore del framework

Dopo alcuni cicli, chiedete una dimostrazione breve: quale nuova capacità funziona, quale rischio è stato ridotto, quale prova sostiene l'affermazione e quale azione successiva è consentita? Se la risposta consiste soltanto in più documenti, agenti o commit, il valore per il prodotto non è ancora stato dimostrato.

Il framework può migliorare la continuità e la distribuzione delle responsabilità. Non elimina giudizio, test reali, sicurezza, privacy o valutazione umana. Un progetto maturo sa fermarsi quando le condizioni concordate sono soddisfatte e sa dichiarare HOLD quando un'incertezza importante impedisce una modifica sicura.

L'obiettivo finale resta un software concretamente utile, costruito e verificato con responsabilità chiare. Le regole hanno valore se rendono questo risultato più affidabile e meno dipendente dalla memoria di una singola conversazione.

**Segue:** capitolo 01, Installazione.

## Fonti e limiti

- [Release v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0)
- [Avvio pubblico v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Note di rilascio e upgrade](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)
- [Panoramica dell'architettura](../../../00_ARCHITECTURE_OVERVIEW.md)
- [Modello delle autorità](../../../../protocols/AUTHORITY_MODEL.md)
- [Licenza MIT](../../../../LICENSE)

Il capitolo descrive il framework e un caso fittizio; non certifica un'applicazione di terzi né autorizza servizi esterni.
