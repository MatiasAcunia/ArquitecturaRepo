# 06 — Fähigkeiten abnehmen und nachvollziehbar abschließen

ArquitecturaRepo · Vollständiges Benutzerhandbuch · Ausgabe v1.4 · Deutsch

> Eine Fähigkeit ist nicht fertig, weil ein Ausführender „PASS“ schreibt. Dieses Kapitel zeigt, wie eine konkrete Produktwirkung an einen aktuellen Kandidaten, getrennte Nachweise und die richtige Entscheidungsautorität gebunden wird. Maßgeblich sind der [Capability-Lebenszyklus](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md) und die [Integrität des Reviews](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md).

## Kapitelübersicht

1. Eine Fähigkeit ist ein benutzbares Ergebnis
2. Fünf Bausteine eines Abschlusses
3. Der genaue Kandidat als Prüfgegenstand
4. Evidenzlücken ohne künstliche neue Kampagne behandeln
5. Annehmen, fortsetzen oder das Ziel ändern
6. Regelmäßige Prüfung und vernünftige Stoppregel
7. Ein überprüfbarer Abschlussdatensatz
8. Zurückweisung und Korrektur im bestehenden Auftrag
9. Brauchbare Software und grünes Framework
10. Wann Arbeit wirklich beendet werden kann

## 1. Eine Fähigkeit ist ein benutzbares Ergebnis

Ein Feature wird häufig in technischen Artefakten beschrieben: ein neuer Endpunkt, eine Datenbanktabelle oder eine Komponente. Für die Produktabnahme genügt diese Sicht nicht. Eine Fähigkeit ist das beobachtbare Ergebnis, das der CLIENT erwartet. Bei einer Vereinsanwendung ist dies beispielsweise die Möglichkeit, einen Mitgliedsbeitrag korrekt zu erfassen, wiederzufinden und im späteren Verlauf unverändert nachzuweisen.

Die Datenbanktabelle kann existieren, obwohl das Formular falsche Beträge zulässt. Der Endpunkt kann alle Unit-Tests bestehen, obwohl die Oberfläche den falschen Mitgliedsdatensatz auswählt. Ein Screenshot kann gut aussehen, obwohl die Speicherung bei einem Neustart verloren geht. Ein erfolgreicher Abschluss muss deshalb den gesamten relevanten Arbeitsweg berücksichtigen.

Das bedeutet nicht, jede denkbare Zukunftsanforderung zu testen. Die Fähigkeit wird gegen ihren ausdrücklich vereinbarten Umfang bewertet. Was ausgeschlossen oder erst für eine spätere Version vorgesehen ist, darf nicht stillschweigend zum aktuellen Abnahmeproblem werden. Gleichzeitig darf ein notwendiger Sicherheits- oder Integritätsnachweis nicht durch die Behauptung „nicht im Scope“ unterdrückt werden, wenn die aktuelle Fähigkeit ohne ihn gefährlich wäre.

Ein guter Abschluss beantwortet: Was kann der Nutzer jetzt tatsächlich tun? Mit welchem konkreten Code- und Datenstand? Unter welchen Bedingungen? Was wurde unabhängig geprüft? Welche Einschränkungen bleiben? Wer hat welche Form der Annahme ausgesprochen?

## 2. Fünf Bausteine eines Abschlusses

Für eine klare Prüfung helfen fünf eng verbundene Bausteine. Erstens muss die vereinbarte Produktfähigkeit wiedergefunden werden können: Anforderung, Charter und zulässige Grenzen. Zweitens muss der genaue technische Kandidat identifizierbar sein. Drittens braucht der Kandidat passende technische, semantische und physische Nachweise. Viertens müssen unabhängige Review- und gegebenenfalls menschliche Qualitätsentscheidungen vorliegen. Fünftens ist der aktuelle Zustand mitsamt den offenen Einschränkungen dauerhaft zu dokumentieren.

Diese Bausteine sind keine fünf zusätzlichen Bürokratieschritte. Häufig entstehen sie aus ohnehin notwendigen Arbeiten. Der Entwickler kennt den Code, die Tests laufen auf einem konkreten Stand, ein Reviewer dokumentiert seine Befunde und der CLIENT sieht eine Demonstration. Das Framework hilft, diese Informationen zusammenzuführen, sodass sie später noch überprüfbar sind.

Ein valider Beleg kann ein Testprotokoll, eine Datenbankquittung, eine lauffähige Anwendung, eine Bildschirmaufnahme oder eine unabhängige Review-Notiz sein. Welcher Beleg angemessen ist, hängt von der Behauptung ab. Ein Git-Commit allein kann eine Datenbankmigration nicht nachweisen; ein Datenbanksnapshot beweist keine gute Bedienbarkeit; ein hübsches Video keine sichere Berechtigungsprüfung.

Legen Sie dabei Wert auf Kausalität. Der Test muss tatsächlich gegen den Kandidaten ausgeführt worden sein, der zur Annahme steht. Eine ältere Testliste, die nach einem wichtigen Codeumbau erneut angehängt wird, ist keine frische Prüfung. Wenn eine materielle Änderung nach dem Review erfolgt, müssen die betroffenen Nachweise erneuert werden.

## 3. Der genaue Kandidat als Prüfgegenstand

Bei veränderlichen Projekten ist die Identität des Kandidaten zentral. Sie kann einen exakten Git-Stand, relevante Konfiguration, Datenbankschema, Migrationen, Laufzeitumgebung und die tatsächlichen Artefakte umfassen. Es reicht nicht, „neueste Version“ zu schreiben, wenn sich der Branch ständig weiterbewegt.

Der Review-Freeze hält den konkreten Gegenstand für die Prüfung fest. Eine unabhängige Person soll denselben Stand untersuchen, nicht einen inzwischen veränderten Arbeitsbaum. Werden danach wichtige Codeänderungen vorgenommen, wird ein neuer Kandidat erstellt und der relevante Review wiederholt. Kleinere Dokumentationskorrekturen können ein anderes Risiko haben; maßgeblich ist ihre tatsächliche Auswirkung auf die geprüfte Fähigkeit.

Ein Beispiel: Der Controller liefert die Mitgliedersuche aus Commit A und ein Reviewer prüft sie auf einer bekannten Testdatenbank. Nach dem Review repariert der Controller eine Zugriffsprüfung in Commit B. Der vorherige Review von A kann nützlich bleiben, belegt aber nicht automatisch B. Die neue Sicherheitslogik verlangt passende frische Tests und eine erneute unabhängige Betrachtung der betroffenen Stelle.

Git allein ist außerdem kein Beweis, wer als verantwortlicher Akteur handelte. Halten Sie Freigaben und Ausführungsidentität auf den dafür vorgesehenen Oberflächen fest, wenn dies für den Kandidaten relevant ist. Die öffentliche Architektur unterscheidet bewusst Commitgeschichte, technische Arbeit und Entscheidungsautorität.

## 4. Evidenzlücken ohne künstliche neue Kampagne behandeln

Wenn eine Abnahmeprüfung eine fehlende Testart oder einen Implementierungsfehler entdeckt, wird der Befund innerhalb des geltenden Charters an I3 zurückgegeben. Der Controller repariert die Ursache, ergänzt den notwendigen Nachweis und liefert einen aktualisierten Kandidaten. Es ist keine neue Planungskampagne nötig, solange die ursprüngliche Produktabsicht und der autorisierte Umfang weiterhin gelten.

Angenommen, alle Unit-Tests der Beitragsfunktion bestehen, aber der tatsächliche Neustart der Anwendung wurde noch nicht geprüft. Das fehlende Physical-Gate kann in derselben Kampagne nachgeholt werden. Falls dabei ein Persistenzfehler auftritt, korrigiert I3 ihn. Ein neuer PASS1/PASS2-Zyklus allein wegen dieser gewöhnlichen Fehler würde nur unnötige Planungsarbeit erzeugen.

Anders ist die Situation, wenn die reale Nutzung zeigt, dass die Fähigkeit einen völlig anderen Sicherheitsrahmen benötigt. Eine lokale Vereinsdatenbank soll plötzlich direkt aus dem öffentlichen Internet erreichbar werden. Das verändert Architektur, Bedrohungsmodell, Betrieb und möglicherweise Datenverarbeitung. Der Planner muss diese neue strategische Lage überprüfen, statt sie als kleinen In-Scope-Bug zu behandeln.

Ein zweiter Sonderfall ist ein dauerhaft falscher Evaluator. Wenn er Belege akzeptiert, die die versprochene Wirkung gar nicht zeigen, muss der Bewertungsmechanismus korrigiert werden. Wenn er einen nachweislich erfüllten und angemessenen Auftrag aus rein formalen Gründen dauerhaft blockiert, muss ebenfalls seine Ursache geprüft werden. Die Reparatur darf keinen notwendigen Gate entfernen, sondern soll ihn wieder sinnvoll machen.

## 5. Annehmen, fortsetzen oder das Ziel ändern

Nach einem konsolidierten Bericht gibt es drei wesentliche Routen. **Annehmen**, wenn der aktuelle Kandidat die vereinbarten Bedingungen mit geeigneter Evidenz erfüllt und alle reservierten Entscheidungen vorliegen. **Fortsetzen**, wenn gewöhnliche Fehler oder Beweislücken innerhalb des gültigen Charters bestehen. **Strategisch ändern**, wenn neue Produktabsicht oder materielle Risikolage die ursprüngliche Vereinbarung ungültig gemacht haben.

Diese Routen sollten nicht vermischt werden. Ein defektes Formular verlangt kein neues Produktziel. Ein komplett neuer öffentlicher Zahlungskanal darf dagegen nicht einfach innerhalb des alten lokalen Beitrags-Chapters gebaut werden. Die richtige Zuordnung schützt sowohl Fortschritt als auch Auftraggeberkontrolle.

Eine Ablehnung sollte konkrete Falsifizierer nennen. Zum Beispiel: „Bei zwei gleichzeitigen Speichervorgängen entsteht ein doppelter Beitrag; die Datenbankprüfung des exakten Kandidaten zeigt das.“ Das ist für I3 ausführbar. „Ich habe ein schlechtes Gefühl, macht alles noch einmal“ ist als technische Anweisung unzureichend, kann aber ein Anlass sein, eine menschliche UX-Demonstration zu verlangen, wenn der Eindruck tatsächlich die Produktqualität betrifft.

Wenn eine Fähigkeit bewusst mit Einschränkungen angenommen wird, müssen diese Einschränkungen eindeutig dokumentiert werden. Eine bedingte Freigabe ist keine heimliche Behauptung, alles sei gelöst. Ein offenes Risiko mit realer Datenverlustmöglichkeit kann zudem eine Annahme ausschließen, selbst wenn die Oberfläche gut wirkt.

## 6. Regelmäßige Prüfung und vernünftige Stoppregel

Eine Qualitätsprüfung muss streng genug für das echte Risiko sein. Sie darf jedoch nicht zu einer endlosen Suche nach theoretischen Mikroproblemen werden, wenn alle strategisch relevanten Grenzen bereits geklärt und die vereinbarten Gates erfüllt sind. Ziel ist nutzbare, verantwortbar geprüfte Software, nicht die größtmögliche Zahl von Reviewrunden.

Der Planner kann regelmäßige Zwischenkontrollen nutzen, um Richtung, Abhängigkeiten und Risiken früh zu erkennen. Solche Kontrollen sind keine vollständigen erneuten strategischen PASS-Zyklen. Ein formaler Review am Kampagnenende bewertet den gesamten Kandidaten und seine Nachweise, nicht bloß das zuletzt bearbeitete kleine Ticket.

Wenn zwei oder mehr Rückläufe dieselbe Fehlklasse betreffen, sollte I3 nicht weiter einzelne Symptome „abbauen“. Er führt eine umfassende technische Härtung und eine unabhängige Überprüfung des betroffenen Subsystems durch. Erst danach ist ein weiterer konsolidierter terminaler Vorschlag sinnvoll. Diese Stoppregel richtet sich gegen ineffizientes Churn, nicht gegen notwendige Tests.

Fortschritt messen Sie am Freischalten einer Fähigkeit, am erfolgreichen Durchlaufen eines relevanten Gates und an real verringerter Gefahr. Die Anzahl von Commits, Agenten und Dokumenten ist nicht entscheidend. Ein einziges behobenes Datenintegritätsproblem kann wertvoller sein als hundert neue Formatchecks.

## 7. Ein überprüfbarer Abschlussdatensatz

Ein kompakter Abschlussbericht für die Beitragsfunktion könnte folgende Inhalte haben:

| Feld | Beispiel einer überprüfbaren Aussage |
| --- | --- |
| Fähigkeit | Beitragszahlung erfassen und historisch wiederfinden |
| Produktgrenze | Nur lokale Vereinsverwaltung, kein externer Zahlungseinzug |
| Kandidat | Exakter Repository-Stand samt Datenbankschema und relevanten Artefakten |
| Unit | Betragsvalidierung, Rundung und Pflichtfelder geprüft |
| Integration | Formular, Service und Datenbank gemeinsam geprüft |
| DB/Currentness | Migration und gespeicherte Zahlungen entsprechen dem aktuellen Kandidaten |
| Semantic | Doppelte Buchung und Mitgliedsdeaktivierung fachlich richtig behandelt |
| Physical | Anwendung unter den vorgesehenen Betriebsbedingungen gestartet |
| Perceptual | Verwaltungskraft konnte den vereinbarten Ablauf verstehen und ausführen |
| Release | Konkretes Paket und Veröffentlichungsberechtigung separat beurteilt |
| Offenes Risiko | Nur wenn tatsächlich vorhanden, mit Auswirkung und Eigentümer |

Die Tabelle sind Beispiele für notwendige Informationen, keine Behauptung, dass der fiktive Verein diese Tests schon durchgeführt hat. In einem realen Bericht müssen die Werte auf tatsächliche Ausgaben und überprüfbare Kennungen zeigen. Eine Rubrik „bestanden“ ohne Quelle ist ein unbelegter Status.

Der Abschluss muss ferner die nächste zulässige Handlung enthalten. Nach der Annahme einer Funktion kann die nächste Fähigkeit eine Beitragsübersicht sein. Falls ein Gate offen bleibt, muss sichtbar sein, wer die Nacharbeit erledigt und welche produktiven Aktionen vorerst nicht erlaubt sind.

## 8. Zurückweisung und Korrektur im bestehenden Auftrag

Ein Reviewer entdeckt, dass die Beitragsfunktion bei einer Datenbankunterbrechung gelegentlich denselben Zahlungseintrag doppelt schreibt. Der geltende Charter verlangt korrekte, einmalige Verbuchung. Der Befund ist damit eindeutig in-scope.

I3 untersucht den vollständigen Buchungspfad: UI-Ereignisse, Retry-Verhalten, Service-Logik, Transaktionen, eindeutige Schlüssel und Fehlerbehandlung. Nach der Korrektur wiederholt er Tests mit Unterbrechungen und identischen Anfragen. Eine unabhängige Prüfung betrachtet anschließend die neu eingeführte Idempotenzmechanik.

Der Planner erhält einen konsolidierten Bericht für den nun aktuellen Kandidaten. Er braucht nicht für jede technische Untersuchung eine neue Kampagne zu autorisieren. Der CLIENT muss auch keine Datenbankstrategie aussuchen. Seine relevante Entscheidung betrifft weiterhin die fachliche Bedeutung einer Zahlung und die Zulässigkeit externer Effekte.

Falls die Untersuchung unerwartet zeigt, dass der Verein jetzt echte Banktransaktionen über eine externe API erwartet, ist das keine reine Reparatur. Diese neue Produktabsicht wird gesondert bestätigt und strategisch bewertet. Nur dann entsteht eine neue Scope-Entscheidung.

## 9. Brauchbare Software und grünes Framework

ArquitecturaRepo kann eigene Strukturtests erfolgreich bestehen, während eine fremde Anwendung fehlerhaft bleibt. Die Werkzeuge prüfen nur, wofür sie gebaut wurden. Ein funktionierender Kampagnencontroller erzeugt noch keine nutzbare Vereinsverwaltung. Ein fertig gestaltetes Handbuch und ein gültiger Release-Hash verbessern die Dokumentation des Starters, aber nicht automatisch die Produkte seiner Nutzer.

Umgekehrt kann eine Anwendung in einer konkreten Demonstration gut aussehen, obwohl ihre Autoritäts- oder Datenbelege unzureichend sind. Beides muss im passenden Verhältnis geprüft werden. Der CLIENT darf die Nutzerqualität beurteilen, während Engineering den technischen Sicherheits- und Integritätsnachweis verantwortet.

Wichtig ist die Fähigkeit, eine ehrliche Grenze zu setzen. „Unter Testdaten erfolgreich, noch nicht für Produktion freigegeben“ ist eine korrekte Aussage. „Der Test ist grün, daher können wir veröffentlichen“ kann falsch sein. Gute Abnahme erhöht Vertrauen gerade dadurch, dass sie Aussagen nur so weit macht wie die Evidenz trägt.

## 10. Wann Arbeit wirklich beendet werden kann

Eine Kampagne kann geschlossen werden, wenn ihre vereinbarte Fähigkeit mit den zutreffenden technischen und menschlichen Nachweisen akzeptiert ist und der aktuelle Zustand sauber hinterlassen wurde. Eine Arbeitssitzung kann auch beendet werden, obwohl die Kampagne noch offen ist, sofern ein sicherer Checkpoint mit konkreter Fortsetzung existiert.

Der CLIENT muss nicht ständig online sein. Fehlt eine neue, wirklich notwendige Produktfreigabe, wird die davon abhängige Handlung angehalten. Andere technisch unabhängige Arbeiten können im zulässigen Umfang fortlaufen. Ein bloßes Ausbleiben der Antwort ist keine neue Produktentscheidung und kein stillschweigender Auftrag, laufende Arbeit zu stoppen.

Abschließend sollte eine frische Sitzung die angenommene Fähigkeit, den Kandidaten, die Prüfungen, offene Risiken und die nächste Route rekonstruieren können. Diese Fähigkeit zur sicheren Fortsetzung ist selbst ein Qualitätsmerkmal des gesamten Entwicklungsprozesses.

**Weiter:** Kapitel 07, durchgearbeitetes Vereinsbeispiel.

## Quellen und Gültigkeit

- [Lebenszyklus und Nachweise einer Fähigkeit](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Review-Freeze und Terminalintegrität](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Kampagnen-Charter](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Execution Team OS](../../../../protocols/EXECUTION_TEAM_OS.md)
- [Release-Kriterien](../../../17_V1_RELEASE_GATES.md)
- [Rekonstruktionsregeln](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md)

Die tabellarischen Belege sind Demonstrationsmuster; echte Abnahme verlangt nachgewiesene Ergebnisse des eigenen Projekts.
