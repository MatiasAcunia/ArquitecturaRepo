# 03 — Täglicher Betrieb und kontrollierte Umsetzung

ArquitecturaRepo · Vollständiges Benutzerhandbuch · Ausgabe v1.4 · Deutsch

> Dieses Kapitel beschreibt den normalen Arbeitszyklus nach bestätigter Adoption und einem autorisierten Entwicklungsauftrag. Die Regeln beruhen auf dem [Execution Team OS](../../../../protocols/EXECUTION_TEAM_OS.md), der [Kampagnenvereinbarung](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md) und der [Rekonstruktion aktueller Zustände](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md).

## Kapitelübersicht

1. Einen Arbeitstag ohne Neustart beginnen
2. Von einer Produktabsicht zur überprüfbaren Fähigkeit
3. Die operative Verantwortung von I3
4. Externe und reservierte Freigaben
5. Ergebnisse eines Ausführenden kritisch lesen
6. Git, Branches und technische Kontinuität
7. Die tägliche Fünffragenkontrolle
8. Ein vollständiger Tagesablauf
9. Ein klar begrenzter Arbeitsauftrag
10. Zustände und Probleme im Controller
11. Bericht, Prüfung und Rückroute
12. Die Sitzung rekonstruierbar beenden

## 1. Einen Arbeitstag ohne Neustart beginnen

Ein zuverlässiger Tagesbeginn besteht nicht darin, alle alten Gesprächsnotizen neu zu lesen. Der Bearbeiter öffnet das tatsächlich zuständige Repository und rekonstruiert die aktuellen Fakten. Welcher Branch und welche Arbeitsspur gelten? Welche Änderungen sind ungesichert? Gibt es einen aktiven Charter, eine eindeutige Eigentümerschaft und einen konkreten nächsten Arbeitszustand? Welche früheren Testergebnisse sind noch an den aktuellen Code gebunden?

Diese Prüfung erfolgt möglichst deltaorientiert. Wenn bereits ein vertrauenswürdiger Checkout existiert, muss nicht jedes Mal das ganze Repository neu geklont werden. Ein gezielter Abruf des relevanten Branches, die Sichtung neuer Commits und die Kontrolle der veränderten Dateien reichen oft. Vermeiden Sie wahllose neue Worktrees und dauerhafte Duplikate großer Artefakte.

Bei einem echten Kontextwechsel darf der neue Ausführende nicht annehmen, dass seine eigene Erinnerung aktuell ist. Ein alter Handoff kann eine inzwischen überholte Kampagne enthalten. Umgekehrt kann eine neue Chatnachricht eine Produktentscheidung ausdrücken, die noch nicht im Product State dokumentiert wurde. Technische Wahrheit und Produktabsicht müssen sorgfältig auseinandergehalten werden.

Eine einfache Tagesnotiz kann so lauten: „Gültiger Entwicklungsauftrag: Mitgliedersuche; aktueller Kandidat: konkret benannter Git-Stand; offenes Gate: Datenbankmigration auf realistischem Datensatz; nächste erlaubte Aktion: Test und in-scope Korrektur; keine Berechtigung zur öffentlichen Veröffentlichung.“ Diese fünf Sätze sind nützlicher als eine unüberprüfbare Zusammenfassung von hundert vergangenen Nachrichten.

## 2. Von einer Produktabsicht zur überprüfbaren Fähigkeit

Der CLIENT sagt vielleicht: „Ich möchte Mitglieder schnell wiederfinden können.“ Der Planner untersucht zunächst, welche Suche das Arbeitsproblem löst. Geht es um vollständige Namen, Teilstrings, Mitgliedsnummern, Statusfilter oder Duplikate? Wie groß ist die Datenmenge und wer darf die Ergebnisse sehen? Welche Antwortzeit fühlt sich im vorgesehenen Kontext ausreichend an?

Eine gute Fähigkeit ist ein Ende-zu-Ende-Ergebnis aus Sicht des Nutzers. „Suchservice implementieren“ ist eine mögliche technische Aufgabe, aber noch keine vollständige Produktfähigkeit. Ein nutzbarer Suchablauf umfasst Eingabe, Berechtigungen, Datenabfrage, Rückmeldung bei keinen Treffern, Fehlerbehandlung und tatsächliche Anzeige. Der Charter beschreibt die Grenzen und Nachweise dieser zusammenhängenden Wirkung.

Ein technisch kleiner Auftrag darf absichtlich eng gefasst werden. Wenn zuerst nur die sichere Suche nach Mitgliedsnummern benötigt wird, muss nicht sofort eine universelle Suchmaschine entwickelt werden. Der Umfang folgt der bestätigten Produktabsicht und den Voraussetzungen. Ein gutes Framework verhindert Scope-Ausweitung, ohne jede Entwicklung in winzige Planungskampagnen zu zerlegen.

Das [Charter-Standarddokument](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md) trennt strategische Abnahmebedingungen von taktischen Einzelarbeiten. Die genaue Implementierungsfolge wird erst innerhalb der autorisierten Arbeit entschieden. Das verschafft der Ausführung die notwendige technische Beweglichkeit und lässt den CLIENT bei den produktrelevanten Fragen.

## 3. Die operative Verantwortung von I3

Nach einer gültigen Freigabe übernimmt der Execution Controller die operative Arbeit. Er entscheidet, welche Dateien und Schnittstellen untersucht werden, wie Fachkräfte eingesetzt werden, welche Tests sinnvoll sind und wie ein Fehler innerhalb des festgelegten Bereichs korrigiert wird. Der Planner muss diese Entscheidungen nicht täglich freigeben.

Zum Arbeitsbereich von I3 gehören Implementierung, Debugging, Integration, interne Refaktorierungen, nötige Migrationen innerhalb des Charters, Testwiederholungen, Wiederaufnahme nach Abstürzen und fachlich begrenzte unabhängige Prüfungen. I3 hält den aktuellen Stand und die Abweichungen vom geplanten Ergebnis nachvollziehbar. Ein Reviewer darf einen Kandidaten wegen eines konkreten Fehlers zurückweisen; die Korrektur bleibt normalerweise in derselben Kampagne.

Angenommen, die Mitgliedersuche liefert bei Umlauten falsche Ergebnisse. Das ist zunächst ein gewöhnlicher Implementierungsfehler. Die zuständige Ausführung untersucht Normalisierung, Datenbankkollation und Testfälle, korrigiert den Code und wiederholt die relevanten Prüfungen. Es wäre ineffizient, hierfür einen neuen strategischen PASS, eine neue Kampagne oder eine neue Kundenbesprechung zu verlangen.

Tritt dieselbe Fehlklasse wiederholt auf, muss die Antwort systemisch werden. Nach mehreren Rückläufen hilft es wenig, nur den nächsten offensichtlichen Testfall zu patchen. I3 untersucht den betroffenen Teilbereich vollständig, überprüft die Architektur und veranlasst eine echte unabhängige Prüfung, bevor erneut eine strategische Endmeldung abgegeben wird.

Die Grenze ist erreicht, wenn der bestehende Charter durch neue Produktabsicht, unerwartete wesentliche Sicherheitsfolgen oder eine grundlegende Architekturänderung ungültig wird. Dann dokumentiert I3 den Befund und routet die strategische Entscheidung an den richtigen Eigentümer. Gewöhnliche Bugs sind keine solche Ungültigkeit.

## 4. Externe und reservierte Freigaben

Ein ausführender Agent kann nicht allein deshalb auf einen Dienst zugreifen, weil Anmeldedaten vorhanden sind. Er muss wissen, ob die konkrete Handlung vom CLIENT und den technischen Zuständigkeiten erlaubt ist. Lesende lokale Untersuchung, Testen in einer isolierten Umgebung und das Erstellen eines Entwurfs unterscheiden sich von Veröffentlichungen, Geldausgaben, echten Kundennachrichten und Änderungen an Produktionsdaten.

Behalten Sie für sensible Operationen Ziel, Umfang und zulässige Kosten fest. Ein allgemeiner Satz wie „Mach das Projekt fertig“ autorisiert keine unbegrenzten kostenpflichtigen API-Aufrufe und keine Veröffentlichung personenbezogener Daten. Ebenso ist die Anwesenheit eines Tools keine Genehmigung, es außerhalb der vorgesehenen Umgebung zu verwenden.

Eine vernünftige Freigabe lautet zum Beispiel: „Du darfst in der lokalen Testdatenbank die Migration ausführen, nachdem das Backup geprüft wurde; Produktionsdaten bleiben unverändert.“ Eine solche Aussage lässt konkrete Kontrollen zu. Bei einem unbekannten Produktionszustand bleibt die abhängige Handlung auf HOLD, während lesende Diagnose weiterlaufen darf.

Bei dritten Inhalten müssen Urheberrechte, Nutzungsbedingungen und tatsächliche Lizenzgrenzen berücksichtigt werden. Verlangen Sie eine angemessene Nutzungsberechtigung, aber stellen Sie nicht jede harmlose lokale technische Prüfung durch endlose rein formale Dokumentationsforderungen still. Wichtig ist die reale Rechts- und Sicherheitslage.

## 5. Ergebnisse eines Ausführenden kritisch lesen

Ein guter Bericht benennt den tatsächlich veränderten Code, die Dateien, den überprüften Kandidaten, seine Testumgebung und das Ergebnis jedes relevanten Gates. Ein schlechter Bericht behauptet nur „fertig“ und zählt Commits, Dateien oder Testfälle. Die reine Zahl bestandener Tests sagt nichts darüber, ob die richtige Nutzerfunktion gebaut wurde.

Lesen Sie besonders auf drei Stellen:

- **Behauptung:** Was wird ausdrücklich als funktionierend bezeichnet?
- **Zeuge:** Welcher konkrete Code, Datenbankstand oder Artefakt beweist das?
- **Grenze:** Welche Umgebung, Eingabe, Nutzerprüfung oder Freigabe wurde nicht abgedeckt?

Wenn die Quelle seit dem Test verändert wurde, ist der frühere Test nicht automatisch aktuell. Ein Prüfer muss den exakten Kandidaten nachweisen, gegen den er geprüft hat. Ein neuer Commit kann einen bekannten Fehler beheben und zugleich einen anderen Fehler eingeführt haben. Daher benötigen materielle Änderungen eine passende erneute Prüfung.

Ein visuell überzeugendes Video kann die Bedienbarkeit zeigen, aber keine Datenbanksicherheit beweisen. Umgekehrt kann ein ausführlicher Unit-Test nicht belegen, dass die Oberfläche tatsächlich lesbar oder für den vorgesehenen Nutzer verständlich ist. Jede Aussage braucht den dazu passenden Nachweis.

## 6. Git, Branches und technische Kontinuität

Git speichert Quellhistorie. Es ist kein automatisches Register dafür, welcher Mensch oder Agent die tatsächliche Arbeit ausgeführt hat. Ein Commit zeigt eine Änderung und ihren Autorbeleg, aber nicht zwangsläufig die vollständige Rollenidentität, Freigabe oder den aktuellen Zustand der Produktdatenbank.

Für mehrere gleichzeitige Aufgaben beurteilen Sie, welche Dateien und Ressourcen tatsächlich betroffen sind. Zwei Aufgaben in verschiedenen Produktbereichen können denselben Migrationsordner oder dieselbe Konfigurationsdatei verändern und sich damit stören. Zwei Aufgaben im selben Repository können hingegen unabhängig sein, wenn ihre Oberflächen wirklich getrennt sind. Planen Sie Konkurrenz nach Interferenz, nicht nur nach Projektname.

Bewahren Sie ungesicherte Änderungen. Benutzen Sie weder einen erzwungenen Reset noch das Löschen des gesamten Arbeitsverzeichnisses als Standardlösung für einen unklaren Zustand. Ein temporärer Worktree kann für echte Parallelität sinnvoll sein; entfernen Sie ihn kontrolliert, wenn er keine aktive Autorität oder Beweisfunktion mehr besitzt.

Die aktuellen technischen Referenzen werden zusammen mit ihrem Gültigkeitsbereich gehalten. Eine Änderung im Branch macht nicht automatisch jede frühere Annahme über Datenbankzustand oder Artefakte falsch. Umgekehrt macht ein unveränderter Commit keine inzwischen geänderte externe API oder Datenbank automatisch aktuell.

## 7. Die tägliche Fünffragenkontrolle

Am Ende einer Arbeitseinheit lohnt sich eine kurze, wiederholbare Prüfung. Erstens: Welche nutzbare Fähigkeit wurde tatsächlich verbessert? Zweitens: Welcher konkrete Kandidat und welche Belege liegen vor? Drittens: Welche Risiken oder offenen Gates bleiben? Viertens: Welche Zuständigkeit hat die nächste Entscheidung? Fünftens: Könnte eine neue Sitzung morgen diese Antworten ohne Gesprächsarchäologie selbst rekonstruieren?

Wenn die Antworten ausschließlich „zehn Tests mehr“, „drei neue Agenten“ oder „noch ein großer Bericht“ lauten, fehlt möglicherweise die Verbindung zum Produkt. Das ist kein Vorwurf an den Arbeitsaufwand. Es ist ein Signal, die nächste technische Handlung wieder an überprüfbare Fähigkeiten und Risiken zu binden.

Die Tageskontrolle soll kompakt bleiben. Sie ersetzt nicht die genaueren Kampagnen- und Gate-Nachweise, aber sie verhindert, dass ein scheinbar aktives Projekt seinen eigentlichen Zweck aus den Augen verliert. Sie darf auch das Ergebnis „kein Fortschritt wegen fehlender autorisierter Datenbank“ zeigen, solange der Blocker präzise und der nächste sichere Schritt klar ist.

## 8. Ein vollständiger Tagesablauf

Am Morgen öffnet die technische Rolle die Vereinsanwendung und bestätigt den letzten freigegebenen Charter. Die Aufgabe ist eine robuste Suchfunktion für Mitglieder. Der aktuelle Kandidat stammt von einem konkreten Git-Stand, und eine Testdatenbank enthält synthetische Mitgliederdaten. Die echte Vereinsdatenbank wird nicht berührt.

Zunächst läuft eine kleine Regression der vorhandenen Mitgliedsverwaltung. Dann implementiert der Ausführende einen zusätzlichen Suchfilter. Ein Test zeigt, dass deaktivierte Mitglieder fälschlich unsichtbar werden, obwohl die Anforderung ihren historischen Zugriff erlaubt. I3 prüft den betroffenen Filter, korrigiert ihn und ergänzt einen Regressionstest.

Anschließend überprüft ein unabhängiger Blick die gesamte Suche unter unterschiedlichen Datenzuständen: kein Treffer, viele Treffer, Namensgleichheit, ungültige Eingaben und unberechtigte Zugriffe. Technische Tests werden um eine echte UI-Demonstration ergänzt. Wenn die Bedienelemente schwer verständlich sind, wird der Unterschied zwischen technischer Korrektheit und wahrgenommener Qualität sichtbar.

Am Abend wird der Kandidat mit dem exakten Quellstand, den Ergebnissen und den offenen Grenzen dokumentiert. Der Planner erhält einen konsolidierten strategischen Bericht, sobald eine wirkliche Abnahmeentscheidung ansteht. Ein weiteres kleines Testversagen am nächsten Tag gehört weiterhin zur technischen Ausführung und löst nicht automatisch einen neuen Charter aus.

## 9. Ein klar begrenzter Arbeitsauftrag

Eine gute Übergabe an I3 enthält Ziel, aktuelle Quellen, erlaubte Grenzen, notwendige Checks und die Definition eines vorlegbaren Ergebnisses. Eine kompakte Fassung könnte lauten:

> Ziel: Die bestätigte Mitgliedersuche end-to-end verfügbar machen. Ausgangspunkt: aktueller Anwendungsbranch und synthetische Testdaten. Grenzen: keine Produktionsdatenänderungen, kein neuer externer Anbieter, keine Erweiterung des Mitgliedsmodells ohne Rückfrage. Gates: Unit, Integration und reale UI-Prüfung getrennt nachweisen. Abschluss: exakten Kandidaten, Testergebnisse, Gegenbelege und offene Risiken melden.

Ein solcher Auftrag überlässt technische Detailarbeit dem dafür zuständigen Controller. Er schützt zugleich die Produktabsicht und die externen Befugnisse des CLIENT. Zu lange Übergaben mit vollständiger Chatgeschichte schaffen eher Widersprüche, wenn dieselbe Information im Repository bereits aktuell vorhanden ist.

Nach der Übergabe bleibt I3 verantwortlich, bis ein sinnvoller terminaler Kandidat vorliegt oder eine echte Charter-Ungültigkeit festgestellt wird. Das Framework soll nicht bei jedem Debugging-Schritt die Verantwortung zurück an den Auftraggeber werfen.

## 10. Zustände und Probleme im Controller

Der optionale lokale [campaignctl.py](../../../../tools/campaignctl.py) kennt Zustände für die von ihm verwalteten Kampagnen. Eine Zustandsänderung in diesem Werkzeug ist nur ein Nachweis über seine eigene kontrollierte Oberfläche. Sie beweist weder, dass ein externer Coding-Agent tatsächlich ausgeführt wurde, noch dass Produktdaten korrekt migriert oder die Nutzeroberfläche abgenommen wurden.

Wenn der Controller einen offenen Vorgang meldet, prüfen Sie zuerst die zugehörige Identität, den letzten gültigen Checkpoint und die vorhandenen Quellen. Ein Neustart des Programms darf einen bereits verbuchten externen Effekt nicht wiederholen. Für irreversible Aktionen sind idempotente Quittungen und klare Ownership wichtig.

Besonders gefährlich sind stillschweigende Reparaturen: eine ungültige Datenbankreferenz durch eine beliebige andere ersetzen, einen fehlenden Reviewer durch ein eigenes PASS markieren oder einen alten Charter nur durch Umbenennung als aktuell deklarieren. Die korrekte Reaktion ist eine kausale Diagnose mit nachvollziehbarer Wiederherstellung.

## 11. Bericht, Prüfung und Rückroute

Der Bericht am Ende einer Kampagne sollte die gebaute Fähigkeit, den exakten Kandidaten, die gemessenen Ergebnisse und die offenen Probleme benennen. Ein unabhängiger Review muss gegen denselben Kandidaten erfolgen. Wenn der Reviewer wesentliche Fehler findet, werden diese im bestehenden Auftrag korrigiert. Eine erneute strategische Planung ist nur bei veränderter Absicht oder materiell neuer Architektur- beziehungsweise Risikolage erforderlich.

Eine strategische Annahme beurteilt andere Fragen als ein Test. Hat die Umsetzung tatsächlich das vereinbarte Produktverhalten geliefert? Sind die Schnittstellen und abhängigen Fähigkeiten konsistent? Wurde ein neues relevantes Risiko geschaffen? Sind die richtigen menschlichen Entscheidungen eingeholt worden?

Für die Qualität der Oberfläche muss der CLIENT oder eine geeignete reale Nutzerprüfung einbezogen werden, wenn das Produkt dies verlangt. I3 kann die Oberfläche technisch liefern, darf seine eigene ästhetische Einschätzung aber nicht als endgültige Kundenfreigabe ausgeben.

## 12. Die Sitzung rekonstruierbar beenden

Bevor Sie schließen, sichern Sie die gültigen aktuellen Artefaktreferenzen, den Stand der Arbeitsfreigabe, die Tests und das nächste zulässige Vorgehen auf den dafür vorgesehenen kanonischen Oberflächen. Halten Sie einen nachweislich alten Bericht nicht neben einer neuen „Wahrheit“ als gleichrangige aktuelle Quelle. Markieren Sie Supersessionen und offene Unsicherheiten.

Legen Sie keinen riesigen neuen Handoff an, der dieselben Regeln mehrfach kopiert. Dauerhafte Zustandsinformationen und stabile Richtlinien benötigen unterschiedliche Eigentümer und Speicherorte. Eine kurze Navigation zur maßgeblichen Quelle ist oft wertvoller als eine weitere vollständige Abschrift.

Der Abschlusstest ist schlicht: Ein anderer Bearbeiter öffnet morgen das Repository, prüft die aktuelle Autorität und kann sicher fortfahren, ohne Ihre heutige Unterhaltung zu kennen. Genau diese Kontinuität rechtfertigt den organisatorischen Aufwand.

**Weiter:** Kapitel 04, Änderungen anfordern.

## Quellen und Gültigkeit

- [Ausführungsteam und Verantwortungen](../../../../protocols/EXECUTION_TEAM_OS.md)
- [Kampagnen-Charter](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Aktualität und Rekonstruktion](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md)
- [Quell- und Arbeitsbereichseffizienz](../../../../protocols/REPOSITORY_EFFICIENCY_AND_WORKSPACE_HYGIENE.md)
- [Review- und Terminalintegrität](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Lokaler Kampagnencontroller](../../../../tools/campaignctl.py)

Das Kapitel beschreibt den belegbaren Kontrollzyklus; es behauptet keine automatische Ausführung externer Programmierdienste.
