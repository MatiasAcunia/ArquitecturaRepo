# 00 — Bevor Sie beginnen

ArquitecturaRepo · Vollständiges Benutzerhandbuch · Ausgabe v1.4 · Deutsch

> Dieses Kapitel erklärt den Zweck, die Zuständigkeiten und die Grenzen des Systems. Es ergänzt die [veröffentlichte Version v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0). Die Beispiele beschreiben Arbeitsweisen, nicht eine bereits abgenommene Anwendung. Maßgeblich für die Installation sind der [aktuelle öffentliche Einstieg](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) und die [Versionshinweise](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md).

## Orientierung

1. Was ArquitecturaRepo tatsächlich liefert
2. Warum die Arbeitsweise anders ist als ein gewöhnlicher Chat
3. Zuständigkeiten und Entscheidungsrechte
4. Verlässliche Informationen und dauerhafte Zustände
5. Die drei Ebenen eines Projekts
6. Ein sinnvoller Einstieg ohne unnötige Komplexität
7. Die acht Kapitel dieses Handbuchs
8. Fragen, die der Auftraggeber beantworten muss
9. Ein zusammenhängendes Beispiel
10. Erfolgskriterien und Grenzen

## 1. Was ArquitecturaRepo tatsächlich liefert

ArquitecturaRepo ist eine portable Ausgangsstruktur für die kontrollierte Entwicklung von Software. Sie enthält dokumentierte Rollen, Entscheidungsregeln, wiederverwendbare Vorlagen, Installationsprofile, prüfbare Datenverträge sowie Python-Werkzeuge für Validierung und Wiederaufnahme. Ein optionaler lokaler Kampagnencontroller kann bestimmte Arbeitszustände verwalten. Diese Teile ergeben gemeinsam einen Entwicklungsrahmen, aber keine fertige Anwendung und keine Garantie für eine autonome Softwarefabrik.

Nach der Installation steht eine organisatorische und technische Steuerungsebene bereit. Sie legt fest, welche Informationen für ein Projekt dauerhaft festgehalten werden müssen, wie sich eine neue Sitzung orientiert und wann ein Ergebnis als nachgewiesen gelten darf. Das konkrete Produkt muss weiterhin verstanden, entworfen, implementiert, getestet und von den zuständigen Personen akzeptiert werden. Die Installation eines Frameworks ersetzt keine dieser Arbeiten.

Die Unterscheidung ist wichtig: Ein erfolgreicher Test des Starters beweist, dass ein Mechanismus des Starters unter den getesteten Bedingungen funktioniert. Er beweist nicht, dass eine damit entwickelte Kundenanwendung korrekt, sicher oder angenehm zu bedienen ist. Ebenso ist ein synthetisches Referenzprojekt ein technischer Prüfstein, kein realer Nutzerbeleg. Wenn ein tatsächlicher Nachweis fehlt, muss der Zustand als unbekannt oder blockiert erscheinen.

Die öffentliche Version v1.4.0 wurde als GitHub-Release mit einem portablen ZIP, Prüfsumme und Manifest bereitgestellt. Die veränderliche Hauptentwicklungszweig kann spätere Korrekturen und diese ausführlichen Handbücher enthalten. Eine Datei auf main ist deshalb nicht automatisch Teil des unveränderlich benannten Release-Pakets. Vergleichen Sie beim Installieren die genaue Version, die erwartete SHA-256-Prüfsumme und die tatsächlich verwendeten Dateien.

Das System kann ohne bezahlte KI-Dienste eingeführt werden. Es verlangt weder einen bestimmten Modellanbieter noch einen vorgeschriebenen Programmieragenten. Die Namen CLIENT, Planner, Controller und Spezialist bezeichnen Entscheidungsbefugnisse und Verantwortlichkeiten. Ob diese Funktionen durch Menschen, Werkzeuge oder ausdrücklich genehmigte Agenten wahrgenommen werden, ist eine eigene Entscheidung des jeweiligen Projekts.

## 2. Warum die Arbeitsweise anders ist als ein gewöhnlicher Chat

Ein Chat kann schnelle Ergebnisse liefern. Man beschreibt eine Funktion, erhält Code, testet ihn und bittet um Korrekturen. Für ein kleines Experiment ist das oft völlig ausreichend. Schwierigkeiten entstehen, wenn Anforderungen im Verlauf vieler Nachrichten geändert werden, mehrere Bearbeiter denselben Stand unterschiedlich verstehen oder eine neue Sitzung den früheren Kontext nicht mehr kennt. Dann muss der Auftraggeber wiederholt erklären, was bereits beschlossen wurde und welcher Code tatsächlich maßgeblich ist.

ArquitecturaRepo versucht dieses Problem durch rekonstruierbaren Zustand zu reduzieren. Die aktuelle Anforderung, die bestätigte technische Grundlage, die gültige Arbeitsfreigabe, die Identität des Kandidaten und seine Nachweise liegen in nachvollziehbaren Repository-Oberflächen. Ein neuer Bearbeiter soll sich daran orientieren können, ohne ein langes Gespräch auswendig zu kennen. Der Nutzen entsteht nicht aus mehr Dokumentation an sich, sondern daraus, dass Entscheidungen und Beweise auffindbar bleiben.

Das Framework macht gewöhnliche Programmierarbeit nicht automatisch schneller. Für eine winzige Einmalaufgabe kann die Einrichtung mehr Aufwand verursachen als die Aufgabe selbst. Für mehrwöchige Projekte, wiederkehrende Übergaben, mehrere technische Zuständigkeiten oder risikoreiche Änderungen kann eine klare Arbeitsführung dagegen Fehlannahmen, doppelte Arbeit und teure Wiederherstellung vermeiden. Ob das gelingt, muss am Ergebnis gemessen werden.

Ein gutes Vergleichsexperiment verwendet dieselbe kleine Produktaufgabe zweimal: einmal mit einem ad-hoc Chat, einmal mit klarer Ausgangslage, Zuständigkeiten und Übergabe. Vergleichen Sie nicht nur die Geschwindigkeit des ersten Codes, sondern auch die Korrektheit nach einer Anforderungsänderung, die Wiederaufnahme durch eine neue Sitzung und den Aufwand für eine begründete Freigabe. Beide Ansätze können sinnvoll sein; der Kontext entscheidet.

## 3. Zuständigkeiten und Entscheidungsrechte

Der CLIENT ist der Auftraggeber und Eigentümer der Produktabsicht. Diese Person entscheidet, welches Problem gelöst werden soll, welches Verhalten gewünscht ist, welche Nutzer betroffen sind und welche Qualität sich richtig anfühlt. Ausgaben, externe Veröffentlichung, Nutzung personenbezogener Daten und andere vorbehaltene Entscheidungen bleiben ebenfalls bei der zuständigen Person. Sie soll nicht nebenbei Merge-Konflikte beheben oder unklare Testprotokolle entziffern müssen.

Die interne Struktur kennt vier Rollenklassen, ohne vier unabhängige Programme zu verlangen:

| Rolle | Kernverantwortung | Typische Grenze |
| --- | --- | --- |
| I1 Master Owner, bei Bedarf | Gemeinsame Steuerung mehrerer Projekte, Kapazität und systemische Konsistenz | Nicht jede kleine technische Aufgabe selbst planen |
| I2 Planner | Anforderungen interpretieren, Architektur und Lieferumfang bestimmen, strategische Annahme prüfen | Nicht jeden Programmierfehler als neue Planungsschleife behandeln |
| I3 Execution Controller | Umsetzung, Debugging, Wiederholungen, Tests, Integration, Wiederherstellung und prüfbare Kandidaten | Keine neue Produktabsicht erfinden oder eigene Arbeit endgültig genehmigen |
| I4 Fachkraft oder Reviewer | Abgegrenzte Implementierung, Recherche, Tests oder unabhängige Prüfung | Keine übergeordneten Freigaben ersetzen |

In einem kleinen Projekt können mehrere Funktionen von derselben technischen Person übernommen werden. Entscheidend ist, dass die Befugnisse in jeder Situation klar bleiben. Eine unabhängige Prüfung erfordert jedoch tatsächlich einen Blick außerhalb der eigenen Implementierungsperspektive. Ein zusätzlicher Chat mit neuem Namen ist nicht automatisch eine unabhängige Prüfung.

Der Planner soll die ganze gewünschte Fähigkeit verstehen und einen sinnvollen Auftrag formulieren. Ist der technische Auftrag freigegeben, führt I3 die alltägliche Arbeit fort: Fehler analysieren, innerhalb des Auftrags korrigieren, Regressionen testen, Zwischenstände konsolidieren und eine überprüfbare Endfassung vorlegen. Ein fehlgeschlagener Unit-Test löst normalerweise keine neue Kampagne und keine neue strategische Grundsatzdiskussion aus.

Bei einer echten Produktänderung kehrt die Entscheidung dagegen zum CLIENT und, soweit strategisch nötig, zum Planner zurück. Ein Beispiel: Die Forderung, eine lokale Mitgliederverwaltung künftig als öffentlich erreichbaren Internetdienst zu betreiben, ändert Zugriffskontrolle, Betrieb, Datenschutz und wahrscheinlich die technische Architektur. Das ist keine gewöhnliche Fehlerkorrektur.

## 4. Verlässliche Informationen und dauerhafte Zustände

Gespräche sind nützlich für Erklärungen und Entscheidungen, aber ein Chatprotokoll ist kein zuverlässiges Inventar des aktuellen Codes. Entscheidend sind die tatsächlich vorhandenen Dateien, der konkrete Git-Stand, die relevante Datenbank, vorhandene Artefakte und gültige Zustandsnachweise. Danach kommen die ausdrücklich bestätigten Anforderungen und die aktuelle Arbeitsfreigabe. Ältere Zusammenfassungen liefern Kontext, ersetzen jedoch keine Überprüfung.

Dabei gilt eine wichtige Ausnahme: Die neueste ausdrückliche Produktentscheidung des CLIENT kann ältere Anforderungen aufheben. Diese Entscheidung muss dann sauber in die aktuelle Produktbeschreibung übernommen werden. Ein technisches System darf nicht stillschweigend an einer früheren Präferenz festhalten, nur weil sie bereits in einem Dokument steht. Umgekehrt darf eine KI nicht aus einem späteren eigenen Bericht eine neue Freigabe konstruieren.

Eine neue Arbeitssitzung beginnt mit einem Misstrauensvorbehalt gegenüber ihrem eigenen Kontext. Der Bearbeiter ermittelt, welche Repository-Version gilt, welches Produkt gemeint ist, welche Anforderungen bestätigt wurden und welche Kampagne ausgeführt werden darf. Kann ein für die nächste Änderung wesentliches Detail nicht nachgewiesen werden, wird die abhängige Änderung angehalten. Unabhängige, lesende Untersuchungen dürfen fortgesetzt werden.

Der erzeugte Steuerungsordner heißt normalerweise .agentic-sdlc/. Ein Status wie HOLD oder UNTRUSTED_CONTEXT direkt nach der Installation bedeutet nicht, dass etwas kaputt ist. Er verhindert lediglich, dass nicht überprüfte Beispielwerte automatisch zu gültigen Projektentscheidungen werden. Erst eine saubere Bestandsaufnahme und Adoption machen daraus ein projektspezifisches System.

## 5. Die drei Ebenen eines Projekts

Für den Einstieg helfen drei Ebenen. L0 enthält belegbare Aussagen und Entscheidungen des Auftraggebers einschließlich späterer Klarstellungen. L1 hält die bestätigte Interpretation als aktuelle Anforderungen, Produktmodell und Product State fest. L2 enthält technische Umsetzung, Quellcode, Datenbanken, Kampagnen, Testergebnisse und Laufzeitnachweise.

Die Ebenen erklären, weshalb ein schönes Konzept noch keine fertige Funktion ist. Eine L1-Anforderung kann gut beschrieben und freigegeben sein, obwohl die entsprechende L2-Implementierung fehlt. Ebenso kann ein Entwickler eine technische Funktion fertigstellen, die nicht zur bestätigten L0-Produktabsicht passt. Ein grüner Test auf L2 repariert diesen Bedeutungsfehler nicht.

Verwechseln Sie auch die Worte Zustand und Wahrheit nicht. Eine Datei namens CURRENT kann veraltet sein, wenn sie auf den falschen Git-Stand oder eine frühere Datenbank verweist. „Aktuell“ ist eine überprüfbare Beziehung zwischen Referenzen und realen Artefakten. Wenn diese Beziehung gebrochen ist, muss sie rekonstruiert werden, bevor eine risikoabhängige Freigabe erfolgt.

## 6. Ein sinnvoller Einstieg ohne unnötige Komplexität

Wählen Sie das kleinste geeignete Profil. Für ein einfaches Lernprojekt genügt häufig SMALL. Beginnen Sie mit einer lesenden Bestandsaufnahme und installieren Sie die Steuerungsebene zunächst nur in einem dafür geeigneten Zielprojekt. Ein bereits streng geregeltes Projekt braucht vor jeder Änderung eine eigene Attachment-Prüfung, weil vorhandene Verantwortlichkeiten nicht automatisch überschrieben werden dürfen.

Vor dem ersten größeren Auftrag sammeln Sie einen kurzen Produktsteckbrief: Zielgruppe, Hauptproblem, wichtigste Nutzerreise, benötigte Daten, Betriebsumgebung, Grenzen, geplanten Termin und offene Fragen. Anschließend rekonstruiert die technische Rolle den bestehenden Quellstand, legt eine nachvollziehbare technische Grundlage fest und plant einen kleinen, in sich prüfbaren Lieferabschnitt.

Für diese Einführung müssen Sie keine acht Kapitel auswendig lernen. Das erste echte Erfolgskriterium lautet: Eine neue Sitzung kann die Ausgangslage und die nächste zulässige Handlung aus dem Repository nachvollziehen. Wenn dies nicht möglich ist, sollte nicht einfach mehr Code produziert werden.

## 7. Die acht Kapitel dieses Handbuchs

| Kapitel | Gegenstand | Praktisches Ergebnis |
| --- | --- | --- |
| 00 | Einführung und Entscheidungsrechte | Sie kennen Zweck und Grenzen. |
| 01 | Installation | Das richtige Paket ist überprüft und sicher eingerichtet. |
| 02 | Planner und Adoption | Anforderungen und Ausgangszustand sind nachvollziehbar. |
| 03 | Täglicher Betrieb | Die Umsetzung bleibt innerhalb einer gültigen Arbeitsfreigabe. |
| 04 | Änderungswünsche | Neue Produktabsichten werden präzise und ohne technische Mikromanagementpflicht formuliert. |
| 05 | Fehler und Wiederherstellung | Belege bleiben erhalten, Risiken werden eingegrenzt und die Fortsetzung ist sicher. |
| 06 | Abschluss von Fähigkeiten | Tests, Integrationsnachweise und menschliche Annahme werden getrennt geprüft. |
| 07 | Durchgearbeitetes Vereinsbeispiel | Der ganze Weg ist an einer konkreten Funktion sichtbar. |

Die acht [kurzen mehrsprachigen Anleitungen](../../../i18n/README_de.md) und die zugehörigen FAQs erleichtern den Einstieg. Sie sind keine Ersatzfassung dieses ausführlichen Buches. Das historische spanische Handbuch v1.3 wird aus Gründen der Nachvollziehbarkeit separat aufbewahrt. Bei widersprüchlichen Versionsangaben gilt der tatsächlich installierte Stand samt zugehöriger Dokumentation.

## 8. Fragen, die der Auftraggeber beantworten muss

Beschreiben Sie zunächst, was sich aus Sicht eines Nutzers ändern soll. „Mitglieder verwalten“ ist ein Ausgangspunkt, aber noch keine ausreichende Entscheidung. Können Mitglieder deaktiviert werden? Wird ihre Zahlungshistorie weiter benötigt? Wer darf sensible Informationen sehen? Soll das System nur auf einem Rechner laufen oder später von mehreren Orten erreichbar sein? Die Antworten sind Produktentscheidungen.

Die technischen Mittel müssen Sie meist nicht vorgeben. Ob für eine kleine Offline-Anwendung SQLite oder für einen Mehrbenutzerdienst PostgreSQL sinnvoller ist, soll die technische Planung anhand echter Anforderungen begründen. Sie können eine Technologie als ausdrückliche Randbedingung vorgeben, müssen aber nicht die Entwurfsarbeit der Entwickler übernehmen.

Wenn Sie eine Antwort noch nicht kennen, schreiben Sie „offen“. Der Planner ermittelt die Folgen und fragt nur nach Entscheidungen, die das Ergebnis tatsächlich verändern. Aus einer ungeklärten Frage darf keine scheinbar bestätigte Regel werden. Das schützt Sie zugleich vor endlosen Rückfragen über technische Einzelheiten.

## 9. Ein zusammenhängendes Beispiel

Ein lokaler Sportverein möchte seine Mitglieder und Beiträge verwalten. Die Verwaltungsmitarbeiterin braucht eine übersichtliche Suchfunktion, die Anmeldung neuer Mitglieder und den Verlauf bezahlter Beiträge. Der CLIENT bestätigt, dass die erste Version keine Online-Zahlungen anbietet und dass die Daten auf einem lokalen Rechner verbleiben. Damit sind bereits mehrere wichtige Grenzen geklärt.

Der Planner prüft zunächst, ob eine Anwendung existiert und welche Daten bereits gespeichert werden. Anschließend beschreibt er eine erste Fähigkeit, beispielsweise die sichere Aufnahme eines Mitglieds mit Pflichtfeldprüfung und eindeutiger Identität. Die Anforderungen werden vom CLIENT bestätigt, die technische Grundlage und die Prüfbedingungen festgehalten und der Entwicklungsauftrag freigegeben.

I3 organisiert danach Implementierung, Tests und gegebenenfalls eine unabhängige Prüfung. Ein Test findet einen Fehler bei doppelt angelegten Mitgliedern. I3 behebt ihn innerhalb desselben Auftrags und weist die Korrektur erneut nach. Erst ein konkreter, überprüfter Kandidat wird zur strategischen und menschlichen Annahme vorgelegt. Der Auftraggeber prüft, ob die Oberfläche verständlich ist und der gewünschte Arbeitsablauf tatsächlich funktioniert.

Angenommen, der Verein verlangt später Zugriff über das Internet. Die frühere Entscheidung „nur lokal“ wird nicht heimlich ersetzt. Die Änderung benötigt neue Produktfreigabe und eine Bewertung der Auswirkungen auf Authentifizierung, Hosting, Backups, Datenschutz und Betrieb. Die bereits bewährte lokale Funktion kann erhalten bleiben, aber die Freigabe ihrer Internetnutzung folgt anderen Gates.

## 10. Erfolgskriterien und Grenzen

Nach zwei oder drei Entwicklungsabschnitten sollten Sie einen neuen Bearbeiter bitten können, ohne alte Chats zu lesen folgende Fragen zu beantworten: Welches Produkt wird gebaut? Welche Anforderungen gelten? Welche Fähigkeit funktioniert bereits? Wo liegt ihr überprüfbarer Kandidat? Welche Risiken sind noch offen? Welche nächste Handlung ist tatsächlich erlaubt?

Ein gutes Ergebnis ist eine nutzbare Fähigkeit mit glaubwürdigen Nachweisen und klarer Fortsetzung. Viele Commits, hübsche Berichte, lange Laufzeiten und zusätzliche Agenten sind höchstens Mittel zum Zweck. Wenn sich damit weder nutzbare Software noch nachweisbare Risikoreduktion verbinden lassen, muss die Arbeitsweise überprüft werden.

Das Framework kann Fehler sichtbar und Übergaben zuverlässiger machen. Es kann nicht garantieren, dass eine Software ohne fachliche Entscheidungen, Datenschutzprüfung, echte Integration oder menschliche Qualitätseinschätzung fertig wird. Diese Grenzen gehören zur ehrlichen Produktbeschreibung und müssen auch in einer überzeugend gestalteten Dokumentation deutlich bleiben.

**Weiter:** Kapitel 01, Installation.

## Quellen und Gültigkeit

- [Veröffentlichte Version v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0)
- [Öffentlicher Einstieg und Support](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Versionshinweise und Upgrade-Grenzen](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)
- [Architekturübersicht](../../../00_ARCHITECTURE_OVERVIEW.md)
- [Verantwortungsmodell](../../../../protocols/AUTHORITY_MODEL.md)
- [MIT-Lizenz](../../../../LICENSE)

Diese Hinweise beschreiben den Starter. Eine reale Anwendung erfordert eigene Nachweise und Freigaben.
