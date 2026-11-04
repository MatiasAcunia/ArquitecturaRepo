# 07 — Durchgearbeitetes Beispiel: Vereinsverwaltung

ArquitecturaRepo · Vollständiges Benutzerhandbuch · Ausgabe v1.4 · Deutsch

> Dieses letzte Kapitel führt eine fiktive Anwendung vom ersten Wunsch bis zur nachvollziehbaren Annahme. Alle Namen, Daten und Ergebnisse sind didaktische Beispiele, keine behauptete Ausführung. Die [Referenzanwendung](../../../15_STATEFUL_REFERENCE_AND_TRANSFER.md) belegt ausgewählte Mechanismen des Starters und ist nicht mit einer echten Produktfreigabe gleichzusetzen.

## Der Weg durch das Beispiel

1. Das Produkt und seine tatsächlichen Nutzer
2. Fragen, die die Lösung verändern
3. Den Starter sicher installieren
4. Erste Fähigkeit: Mitglieder verwalten
5. Vom Planner zur ausführbaren Kampagne
6. Fachliche und technische Tests
7. Zweite Fähigkeit: Vereinsbeiträge
8. Das Gesamtprodukt bewerten
9. Erster Entwicklungszyklus mit fiktiven Daten
10. Einen Befund an die richtige Rolle routen
11. Zweiter Zyklus mit klaren Abhängigkeiten
12. Übung: Fortsetzung in einem neuen Kontext

## 1. Das Produkt und seine tatsächlichen Nutzer

Stellen Sie sich einen örtlichen Sportverein mit einer Verwaltungskraft und einigen hundert Mitgliedern vor. Bislang führt die Verwaltung ihre Mitglieder und Beitragszahlungen in Tabellen. Unterschiedliche Dateiversionen verursachen gelegentlich doppelte Einträge. Der Vorstand möchte wissen, welche Beiträge bezahlt wurden; die Verwaltung benötigt vor allem eine einfache Erfassung und eine schnelle Suche.

Der Auftraggeber formuliert den Zweck: „Wir möchten Mitglieder zuverlässig verwalten und sehen, welche Beiträge offen sind. Die erste Version läuft auf einem vorhandenen Vereinsrechner. Sie soll leicht verständlich sein. Externe Zahlungsanbieter brauchen wir noch nicht.“

Damit sind erste Grenzen gesetzt. Der Nutzen besteht nicht darin, möglichst viele APIs oder KI-Agenten einzusetzen. Er besteht in einem korrekten, benutzbaren Arbeitsablauf für die Verwaltung und in einer nachvollziehbaren Auswertung für den Vorstand. Das konkrete Datenmodell, die Programmiersprache und die Testorganisation bleiben technische Entscheidungen.

Der Auftraggeber darf außerdem entscheiden, welche Daten gespeichert werden. Namen und Kontaktinformationen sind potenziell personenbezogen. Es muss geklärt werden, wer sie lesen darf, ob sie länger aufbewahrt werden und wie die Anwendung gesichert wird. Die fiktiven Beispieldaten, die wir hier verwenden, enthalten keine realen Vereinsmitglieder.

Ein Liefertermin könnte vereinbart werden, doch er ersetzt keine Definition des ersten brauchbaren Ergebnisses. Für den Verein ist eine funktionierende Mitgliedererfassung mit Suche nützlicher als ein technisch beeindruckendes Dashboard ohne verlässliche Datengrundlage.

## 2. Fragen, die die Lösung verändern

Der Planner führt ein kurzes Produktgespräch. Er fragt nicht nach dem bevorzugten Datenbankindex. Er will wissen, was fachlich geschieht:

- Welche Daten sind beim Anlegen eines Mitglieds zwingend notwendig?
- Können zwei Mitglieder denselben Namen haben?
- Was bedeutet „deaktiviert“ für historische Beiträge und Aktivitäten?
- Wer darf Mitgliedsdaten ändern und wer darf nur Berichte sehen?
- Soll die Anwendung ohne Netzwerkzugang funktionieren?
- Was passiert, wenn eine Beitragszahlung versehentlich zweimal eingegeben wird?
- Wie lange darf die Wiederherstellung nach einem Rechnerausfall dauern?
- Welche Funktionen sind für die erste Vorführung unverzichtbar?

Angenommen, der CLIENT bestätigt: Eine Verwaltungskraft arbeitet lokal, Mitglieder benötigen eine stabile interne Identität, Zahlungen bleiben nach Deaktivierung nachvollziehbar, und die erste Version hat keine Onlinezahlung. Die Anwendung muss verständliche Fehlermeldungen zeigen und vor doppelten Mitgliedern warnen. Über ein konkretes Backup-Intervall entscheidet der CLIENT noch nicht; der Punkt bleibt offen.

Diese Antworten werden als aktuelle Anforderungen dokumentiert. Die technische Rolle darf zusätzliche Folgen erklären: Eine stabile ID verhindert, dass Namensänderungen die Zahlungsverknüpfung zerstören; eine Historie verlangt ein geeignetes Persistenzmodell; fehlender Netzwerkzugang begünstigt lokale Speicherung. Die Entscheidung über Tabellen, Frameworks und Sicherungsmechanismen trifft Engineering.

Der Planner achtet darauf, die Beispielantworten nicht als reale Kundenfreigaben zu behandeln. In einer echten Installation müssen sie vom tatsächlichen CLIENT kommen und auf den aktuell gültigen Zustand angewendet werden.

## 3. Den Starter sicher installieren

Das Team besitzt bereits ein separates Anwendungsrepository verein-app. Der öffentliche Starter ArquitecturaRepo wurde als v1.4.0-Release bezogen und gegen die veröffentlichte Prüfsumme kontrolliert. Beide Verzeichnisse bleiben getrennt. Die Installation wird nicht im Starter selbst ausgeführt, um dort Vereinsfunktionen zu entwickeln.

Für ein neues, noch nicht geregeltes Projekt mit dauerhaften Mitglieds- und Zahlungsdaten entscheidet das Team sich begründet für STATEFUL. Im geprüften Starter könnte der Befehl lauten:

    & "python" "tools\scaffold_project.py" --target "..\verein-app" --profile "STATEFUL" --product-id "VEREIN_APP" --objective "Lokale Mitglieder- und Beitragsverwaltung" --language "de" --no-feedback-workflow

Danach liegen die generierten Kontrollunterlagen in verein-app/.agentic-sdlc/. Die anfängliche Anzeige HOLD / UNTRUSTED_CONTEXT ist richtig. Der Starter kennt noch keinen echten Datenbankstand, keinen angenommenen Charter und keine bestätigte Produktbeschreibung. Ein Assistent darf diese Informationen nicht aus dem Beispiel übernehmen.

Im Zielprojekt werden die vorgesehenen Anforderungen installiert und der lesende Prüfpfad ausgeführt:

    & "python" -m pip install -r ".agentic-sdlc\requirements-validation.txt"
    & "python" ".agentic-sdlc\tools\project_status.py" --control-root ".agentic-sdlc"
    & "python" ".agentic-sdlc\tools\discover_project.py" --project-root "."
    & "python" ".agentic-sdlc\tools\reconstruct_context.py" --root ".agentic-sdlc"

Stellen Sie sich vor, dass die Strukturprüfung gelingt, die Rekonstruktion aber noch gültige Anforderungen vermisst. Das ist kein Widerspruch: Die Ordner sind vorhanden, doch die echte Projektübernahme steht noch aus. Der Planner führt nun Discovery durch, verifiziert den Code und die Betriebsumgebung und holt die notwendige Produktbestätigung ein.

Wäre verein-app bereits von einem anderen System mit gültigen Steuerungsregeln verwaltet, wäre das obige Scaffold nicht die richtige Route. Dann müsste die [bestehende Governance lesend geprüft](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) werden, bevor man etwas verändert.

## 4. Erste Fähigkeit: Mitglieder verwalten

Der Planner wählt eine überschaubare, aber nutzbare erste Fähigkeit: „Mitglied anlegen, später anhand einer stabilen Kennung wiederfinden, wichtige Daten ändern und eine Person deaktivieren, ohne ihre historische Identität zu verlieren.“ Dieser Umfang umfasst mehr als das bloße Erstellen eines Formulars.

Die fachlichen Bedingungen könnten so aussehen:

| Vorgang | Beobachtbarer Erfolg | Wichtiger Grenzfall |
| --- | --- | --- |
| Anlegen | Neues Mitglied erhält eine stabile ID und ist wiederfindbar | Fehlende Pflichtdaten |
| Suchen | Berechtigte Verwaltung findet nach Name oder ID | Gleicher Name bei verschiedenen Personen |
| Bearbeiten | Änderungen sind nach erneutem Öffnen vorhanden | Gleichzeitige Änderung, soweit im Scope |
| Deaktivieren | Status wechselt ohne Löschung der Zahlungsbezüge | Versuch, historische Belege zu entfernen |
| Fehleranzeige | Nutzer versteht, was er korrigieren muss | Doppelte Eingabe oder Speicherausfall |

Noch ist kein Test bestanden. Die Tabelle beschreibt, was nachgewiesen werden soll. Engineering bestimmt nun die technische Basis und erstellt einen kurzen Lieferplan. Beispielsweise werden zuerst Stammdaten und Persistenz, danach die Suchoberfläche und zum Schluss Deaktivierung samt Regressionen integriert. Diese Reihenfolge kann sich nach echter Codeinspektion ändern.

Der CLIENT bestätigt die fachliche Bedeutung und den sichtbaren Qualitätsanspruch. Er muss nicht entscheiden, wie Datenbanktransaktionen implementiert werden. Wenn die technische Rolle ein Risiko identifiziert, etwa den möglichen Verlust von Mitgliederdaten bei Stromausfall, erklärt sie die Produktfolge und verlangt nur die dafür notwendige fachliche Entscheidung.

## 5. Vom Planner zur ausführbaren Kampagne

Der Planner führt seine strategische Hauptbetrachtung durch: Ziel, Nutzerfluss, Daten, Schnittstellen, Sicherheitsrisiken, Fehlerfälle, Wiederherstellung, Abhängigkeiten und notwendige Gates. Eine separate adversariale Betrachtung sucht nach falschen Annahmen. Erst danach entsteht der Capability-Charter, der die erste Mitgliederfähigkeit beschreibt.

Der Charter enthält das erwartete Ergebnis, die Ausgangsquellen, den zulässigen Umfang, seine Schnittstellen, die Verantwortung von I3 und die Abnahmebedingungen. Er muss nicht jede interne Funktion und jeden Git-Commit vorgeben. Mit seiner Freigabe übernimmt der Controller die operative Umsetzung.

Eine kompakte Übergabe könnte so formuliert sein:

> Ziel: Die bestätigte lokale Mitgliederverwaltung end-to-end nutzbar machen. Ausgangsquellen: aktueller geprüfter Anwendungsstand, Product State und bestätigte Anforderungen. Grenzen: keine externen Provider, keine realen Daten versenden, kein öffentliches Deployment, keine Onlinezahlung. Nachweise: Unit, Integration, DB/Currentness, fachliche Grenzfälle, reale lokale Bedienprobe und vereinbarte menschliche Qualität. Abschluss: exakten Kandidaten, Fehler, Tests und offene Risiken vorlegen.

Dies ist keine Einladung zur unbegrenzten autonomen Ausführung. Die Ausführung muss in der tatsächlich autorisierten Umgebung mit den passenden Rechten erfolgen. Ein optionaler lokaler Controller kann Zustände verwalten, aber seine Existenz bedeutet nicht, dass ein externer Agent bereits gestartet wurde.

## 6. Fachliche und technische Tests

Die Implementierung kann aus einer Datenhaltung, einem Service und einer Oberfläche bestehen. Es ist nicht notwendig, eine bestimmte Architektur zu erzwingen, solange sie die bestätigten Anforderungen zuverlässig erfüllt und angemessene technische Qualität bietet. Die ersten Unit-Tests prüfen etwa Pflichtfelder, Identitätsregeln und Statuswechsel.

Integrationstests prüfen anschließend den vollständigen Weg vom Formulareintrag bis zur gespeicherten und erneut gelesenen Person. Ein separat geprüfter Datenbankstand muss zu den tatsächlich verwendeten Migrationen passen. Semantic-Tests verwenden unterschiedliche Namen, leere Felder, Sonderzeichen und doppelte Personen, um fachliche Generalisierbarkeit zu untersuchen.

Physical bedeutet: Die Anwendung wird unter den vorgesehenen Bedingungen tatsächlich gestartet und bedient. Wenn ein automatisierter Test nur einzelne Funktionen importiert, ersetzt er diesen Schritt nicht. Perceptual bedeutet: Ein vorgesehener Nutzer versteht, welche Eingabe erwartet wird, was ein Fehler bedeutet und wie er einen Datensatz wiederfindet. Diese Prüfung kann nicht durch einen bloßen Quellcodekommentar ersetzt werden.

Angenommen, die Speichertests bestehen, aber die Oberfläche zeigt nach dem Anlegen keine Bestätigung. Das kann ein echtes Benutzbarkeitsproblem sein. I3 korrigiert es im laufenden Charter, wenn eine verständliche Rückmeldung bereits Bestandteil der Abnahme war. Eine zusätzliche neue Kampagne würde nichts verbessern.

Die Tests und die menschliche Prüfung müssen den exakten Kandidaten betreffen. Wird danach wichtiges Verhalten verändert, sind die betroffenen Nachweise zu erneuern. Ein Bericht über einen älteren Stand ist nicht automatisch ein gültiges Review für die aktuelle Version.

## 7. Zweite Fähigkeit: Vereinsbeiträge

Erst wenn die Mitgliederidentität verlässlich ist, wird die nächste Fähigkeit sinnvoll: Beiträge erfassen und den Verlauf anzeigen. Diese Fähigkeit hängt von bestehenden Mitgliedern, ihrer stabilen ID und den Regeln für deaktivierte Personen ab. Die Reihenfolge schützt vor einer losgelösten Zahlungstabelle ohne zuverlässige Verknüpfung.

Der CLIENT entscheidet, was als Beitrag gilt, ob Teilzahlungen möglich sind, welche Beträge erwartet werden und wer Korrekturen vornehmen darf. Das Team erklärt die Folgen für Datenmodell und Auswertungen. Externe Bezahlvorgänge bleiben ausdrücklich außerhalb des ersten Umfangs. Ein lokal erfasster Beitrag ist kein Beweis für eine echte Banktransaktion.

Ein wichtiges Risiko ist doppelte Verbuchung. Wenn die Verwaltungskraft auf „Speichern“ doppelt klickt oder eine Netzwerkstörung später einmal zu einem Retry führt, darf aus einer fachlich einmaligen Zahlung nicht unbemerkt eine doppelte Buchung werden. Engineering gestaltet dafür geeignete Identitäten, Transaktionen und Testfälle.

Auch die Historie muss erhalten bleiben. Wenn ein Mitglied deaktiviert wird, sollen seine bisherigen Beiträge nicht verschwinden. Eine Namensänderung darf historische Buchungen nicht einer anderen Person zuordnen. Der zweite Charter baut also auf nachgewiesenen Eigenschaften des ersten auf; er erfindet deren Abnahme nicht neu.

## 8. Das Gesamtprodukt bewerten

Nach zwei Fähigkeiten soll die Verwaltung einen vollständigen Ablauf demonstrieren können: ein Mitglied anlegen, die Person suchen, einen Beitrag erfassen, eine vergangene Zahlung wiederfinden und eine Person deaktivieren, ohne ihre Historie zu verlieren. Diese zusammenhängende Probe ist wertvoller als zwei isolierte grüne Modulberichte.

Der Planner fragt nach den übergreifenden Risiken: Stimmen Datenmodell und Oberfläche überein? Verhindern Berechtigungen unzulässige Änderungen? Sind Daten nach einem Neustart noch vorhanden? Ist die Wiederherstellung getestet, soweit sie vereinbart wurde? Kann der CLIENT seine häufigsten Aufgaben tatsächlich ausführen?

Eine gute Bewertung erkennt ebenfalls Grenzen. Ein lokaler, kleiner Vereinsbetrieb ist keine automatische Freigabe für tausende gleichzeitige Internetnutzer. Ein Test mit synthetischen Zahlungsdaten ist keine Abnahme eines externen Finanzdienstes. Die erreichte Fähigkeit darf genau beschrieben werden, ohne ihre Gültigkeit zu überdehnen.

Der Erfolg besteht in einer praktisch verwendbaren Grundlage und einem vertrauenswürdigen nächsten Schritt. Mehr Dokumente oder zusätzliche Agenten sind nur dann sinnvoll, wenn sie diese Ziele unterstützen.

## 9. Erster Entwicklungszyklus mit fiktiven Daten

Für einen realitätsnahen Probezyklus legen Sie synthetische Mitglieder an: Person A mit aktivem Status, Person B mit gleichem Nachnamen, Person C mit späterer Deaktivierung. Führen Sie erfolgreiche und ungültige Eingaben aus. Testen Sie bewusst Sonderzeichen im Namen, fehlende Pflichtwerte und eine Korrektur der Kontaktadresse.

Danach schließen Sie die Anwendung vollständig und öffnen sie erneut. Prüfen Sie, ob die Daten erhalten bleiben. Wenn das Projekt eine Datenbanksicherung vorsieht, verwenden Sie einen definierten isolierten Wiederherstellungsfall. Dokumentieren Sie den tatsächlich geprüften Code- und Datenstand und kennzeichnen Sie offen, was noch nicht ausgeführt wurde.

Ein Fehler bei der Suche nach Person B wird zunächst technisch diagnostiziert. Eine falsche Sortierung, eine nicht behandelte Kodierung oder eine fehlerhafte Abfrage kann die Ursache sein. I3 repariert sie innerhalb des bestehenden Charters und führt die relevanten Regressionen erneut aus.

Vor einer positiven Abnahme zeigt die Verwaltungskraft in einer echten Bedienprobe, ob sie die vorgesehenen Schritte ohne Spezialwissen versteht. Ist die Oberfläche verwirrend, kann die Anforderung fachlich unzureichend erfüllt sein, obwohl alle Tabellen korrekt sind.

## 10. Einen Befund an die richtige Rolle routen

Stellen Sie sich drei unterschiedliche Befunde vor. Erstens: „Das Speichern schlägt bei Umlauten fehl.“ Dies ist gewöhnlich ein technischer Defekt; I3 untersucht und behebt ihn. Zweitens: „Wir brauchen doch Selbstregistrierung über das Internet.“ Dies ist eine neue Produktabsicht mit Sicherheitsfolgen; der CLIENT bestätigt sie und der Planner bewertet den neuen Umfang. Drittens: „Wir wissen nicht, ob die Datenbank bereits eine Zahlung verbucht hat.“ Dies ist eine Currentness- und mögliche Idempotenzfrage; weitere schreibende Aktionen bleiben bis zur Rekonstruktion gesperrt.

Die richtige Route hängt also nicht allein davon ab, ob der Bericht alarmierend klingt. Sie hängt von Ursache, betroffenem Gate, bestehender Autorisierung und materiellen Folgen ab. Das System soll den CLIENT vor technischer Mikromanagementarbeit schützen, ohne ihn aus echten Produktentscheidungen auszuschließen.

Wenn ein technischer Defekt zum dritten Mal auftritt, wird die bisherige Symptombekämpfung hinterfragt. I3 prüft das ganze betroffene Subsystem und fordert eine unabhängige Überprüfung. Ein neuer Planner-Zyklus allein wegen wiederkehrender Implementierungsfehler würde die falsche Verantwortung belasten.

## 11. Zweiter Zyklus mit klaren Abhängigkeiten

Die Beitragsfunktion verwendet die zuvor angenommene Mitgliederidentität. Bevor I3 eine neue Zahlung schreibt, prüft er, dass diese Identität im tatsächlich aktuellen Kandidaten vorhanden und gültig ist. Falls die erste Fähigkeit seit ihrer Annahme verändert wurde, kann eine erneute Integrationsprüfung nötig sein.

Ein fiktiver Beitrag von 25 Einheiten wird für Person A erfasst. Anschließend liest die Anwendung den Datensatz wieder. Der Test wiederholt denselben fachlichen Speichervorgang und kontrolliert, dass keine doppelte Buchung entsteht. Für Person C wird die Deaktivierung geprüft: Historische Zahlungen bleiben auffindbar, während neue Vorgänge nach der bestätigten Regel eingeschränkt werden.

Der Controller legt einen konkreten Kandidaten und seine Nachweise vor. Ein Reviewer untersucht Grenzfälle, Datenintegrität und Fehlerbehandlung. Der CLIENT beurteilt die Verständlichkeit des Gesamtablaufs. Falls das Ergebnis die vereinbarten Bedingungen erfüllt, wird die Fähigkeit nachvollziehbar angenommen. Falls nicht, werden konkrete Fehler innerhalb des bestehenden Charters korrigiert.

Die nächste Fähigkeit könnte ein monatlicher Beitragsbericht sein. Sie wird erst sinnvoll geplant, wenn die tatsächliche Bedeutung von „bezahlt“, „offen“ und „überfällig“ bestätigt ist. Ein technischer Bericht ohne diese Fachregeln könnte mathematisch perfekt und für den Verein trotzdem nutzlos sein.

## 12. Übung: Fortsetzung in einem neuen Kontext

Für den Abschluss dieses Handbuchs legen Sie das ursprüngliche Gespräch beiseite. Bitten Sie eine neue Person oder Sitzung, ausschließlich anhand des aktuellen Anwendungsrepositorys folgende Fragen zu beantworten:

1. Wer benutzt die Anwendung, und welche Probleme soll sie zuerst lösen?
2. Welche Produktentscheidungen wurden ausdrücklich bestätigt?
3. Welcher reale Git- und Datenbankstand ist aktuell?
4. Welche Mitglieder- und Beitragsfunktionen sind angenommen?
5. Welche Tests, Reviews und echten Bedienproben belegen diese Annahme?
6. Welche Risiken, offenen Fragen und externen Freigaben fehlen?
7. Welche Kampagne ist noch aktiv, und wer darf sie fortsetzen?
8. Was darf die neue Sitzung als Nächstes tun, ohne nach der gesamten alten Chatgeschichte zu fragen?

Kann die Sitzung diese Punkte rekonstruieren, besitzt das Projekt einen belastbaren Übergang. Kann sie es nicht, ist die konkrete Lücke zu beheben: fehlende Anforderung, unklare Datenbankreferenz, nicht aktueller Review oder fehlende Ownership. Eine neue schöne Zusammenfassung ohne gültige Quellen würde das Grundproblem nicht lösen.

Der letzte praktische Test ist immer die reale Nutzbarkeit. Wenn die Verwaltung eine Person und ihre Beiträge zuverlässig verwalten kann, die Risiken kontrolliert und die Fortsetzung nachvollziehbar ist, hat das Framework seinen Zweck erfüllt. Es ist kein Selbstzweck und kein Ersatz für gute Softwareentwicklung.

## Weiterführende Quellen

- [Referenzprojekt und Transfer](../../../15_STATEFUL_REFERENCE_AND_TRANSFER.md)
- [Öffentliche v1.4-Installation](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Bestehende Projekte prüfen](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Produktentdeckung](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Adoption](../../../16_TRANSFER_ADOPTION.md)
- [Charter-Standard](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Capability-Gates und Evidenz](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Rekonstruktion aktueller Zustände](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md)

Das Vereinsbeispiel ist ein didaktisches Szenario. Seine vorgeschlagenen Anforderungen, Tests und Annahmen sind keine Aussage über den tatsächlichen Zustand eines existierenden Vereins.
