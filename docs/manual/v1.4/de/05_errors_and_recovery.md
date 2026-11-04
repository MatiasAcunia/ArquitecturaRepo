# 05 — Fehler, Zwischenfälle und sichere Wiederherstellung

ArquitecturaRepo · Vollständiges Benutzerhandbuch · Ausgabe v1.4 · Deutsch

> Fehler sind im Entwicklungsprozess normal. Entscheidend ist, dass bei ihrer Behandlung keine aktuellen Quellen, Daten oder Entscheidungsrechte verloren gehen. Dieses Kapitel ergänzt die [Rekonstruktionsregeln](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md), das [Recovery-Protokoll](../../../12_TRANSACTION_RECOVERY.md) und die [Sicherheitsgrenzen](../../../../protocols/SECURITY_PRIVACY_RIGHTS_AND_EXTERNAL_ACTIONS.md).

## Kapitelübersicht

1. Beweise vor Maßnahmen sichern
2. Umgebungs- und Kontoprobleme
3. Fehler der installierten Steuerungsebene
4. Git ist keine allgemeine Rückgängig-Taste
5. Wiederkehrende Fehler systemisch behandeln
6. Sicherheit, Datenschutz und Rechte Dritter
7. Nachweisbare Rückkehr zum Betrieb
8. Drei vollständige Wiederherstellungsfälle
9. Entscheidungsmatrix für sensible Operationen
10. Was grüne Validierung nicht aussagt
11. Feedback und Telemetrie des Starters

## 1. Beweise vor Maßnahmen sichern

Die erste Reaktion auf einen Fehler sollte nicht das Löschen oder Neuinstallieren sein. Klären Sie, was tatsächlich fehlgeschlagen ist und welche Informationen für die Diagnose benötigt werden. Notieren Sie die genaue Fehlermeldung, den ausführenden Befehl, den relevanten Pfad, den aktuellen Git-Stand, den beteiligten Datenbankzustand und den Zeitpunkt. Bewahren Sie ungesicherte Änderungen auf.

Je nach Risiko ist die richtige Sofortmaßnahme eine begrenzte Pause. Wenn der Fehler nur ein lokaler fehlender Testimport ist, dürfen unabhängige sichere Arbeiten weiterlaufen. Wenn die Datenbankmigration möglicherweise echte Mitgliedsdaten verändert hat, müssen weitere schreibende Datenbankaktionen angehalten werden, bis die Situation verstanden ist. Der Umfang des HOLD folgt der betroffenen Ressource und nicht einer pauschalen Angst vor jedem Warnsignal.

Vermeiden Sie Aktionen, die die Ursache verschleiern. Ein erzwungener Reset, eine unkontrollierte Neuinstallation, das Löschen aller Caches oder das Ausführen einer Migration ein zweites Mal kann wertvolle Belege zerstören. Bei Datenbanken kann eine Wiederholung sogar denselben wirtschaftlichen Vorgang doppelt verbuchen.

Das Prinzip lautet: Zuerst beobachtbaren Zustand sichern, dann den Fehler eingrenzen, dann eine reversible oder ausdrücklich autorisierte Reparatur durchführen, anschließend den konkreten Effekt nachweisen. Ein plausibler Erklärtext ersetzt dabei weder einen Integritätstest noch die Sichtung des realen Produkts.

## 2. Umgebungs- und Kontoprobleme

Nicht jeder Fehler liegt im Projektcode. Python kann im falschen virtuellen Environment laufen; eine Abhängigkeit kann fehlen; das Terminal kann sich in einem anderen Arbeitsverzeichnis befinden; eine Anmeldung kann abgelaufen sein. Beginnen Sie bei der tatsächlichen Umgebung und vergleichen Sie erwartete mit beobachteten Werten.

Falls ein Befehl nicht gefunden wird, prüfen Sie den Interpreterpfad und die Version, bevor Sie eine neue Installation starten. Wenn Git kein Repository erkennt, prüfen Sie das Verzeichnis. Wenn ein Agent angeblich keine Dateien sieht, kontrollieren Sie dessen Workspace statt ihm sofort weitere globale Rechte zu geben.

Ein Zugriffsfehler ist keine Einladung, Berechtigungsgrenzen zu umgehen. Wenn ein Dienst ausdrücklich eine neue Anmeldung oder einen gesonderten Zugriff verlangt, muss diese Autorität beim zuständigen Konto eingeholt werden. Keine technischen Tricks und keine ungeprüfte Wiederverwendung fremder Geheimnisse sind angemessene Reparaturen.

Ein externer Anbieter kann außerdem vorübergehend nicht erreichbar sein. Unterscheiden Sie Netzwerkausfall, Tokenproblem, API-Änderung, Quota, Kostenlimit und Programmfehler. Ein Test in der lokalen isolierten Umgebung kann weiter zulässig sein, obwohl produktive externe Aufrufe gesperrt bleiben.

## 3. Fehler der installierten Steuerungsebene

Die Steuerungsebene .agentic-sdlc/ enthält Verträge und aktuelle Projektbezüge. Schlägt ihre Prüfung fehl, darf man nicht einfach ein fehlendes Feld mit einem erfundenen Wert füllen. Ein Schemafehler, eine widersprüchliche Identität und eine nicht aktuelle Datenbankreferenz sind unterschiedliche Fälle und brauchen unterschiedliche Lösungen.

Ein reiner Formatfehler kann nach Sichtung der beabsichtigten Regel lokal korrigiert werden. Eine unbekannte Autorität erfordert hingegen Rekonstruktion, nicht kosmetische JSON-Bearbeitung. Wenn eine frühere Kampagne behauptet, sie sei abgeschlossen, ihre Quell- oder Review-Referenzen aber fehlen, bleibt die Abnahme unbewiesen. Der Controller kann den erforderlichen Nachweis nachholen oder den Zustand ehrlich als offen kennzeichnen.

Die Werkzeuge [project_status.py](../../../../tools/project_status.py), [validate_project.py](../../../../tools/validate_project.py) und [reconstruct_context.py](../../../../tools/reconstruct_context.py) helfen, verschiedene Fehlklassen sichtbar zu machen. Ihre Ausgaben müssen im richtigen Projekt und mit der tatsächlich installierten Version interpretiert werden. Ein grüner Strukturtest beweist nicht, dass die gespeicherten Informationen zur wirklichen Anwendung passen.

Besonders wichtig ist die Regel über aktuelle Quellen: Eine Datei kann formal korrekt und dennoch veraltet sein. Wenn sie auf einen früheren Git-Stand, eine nicht mehr gültige Datenbank oder einen überschriebenen Review verweist, muss diese Referenz geprüft und gegebenenfalls ungültig erklärt werden.

## 4. Git ist keine allgemeine Rückgängig-Taste

Git kann bekannte Quelländerungen zeigen und frühere Versionen wiederherstellbar machen. Es verwaltet jedoch nicht automatisch alle externen Effekte. Eine Datei kann zurückgesetzt werden, obwohl eine Datenbankmigration weiterhin wirksam ist. Ein Commit kann wieder entfernt werden, während eine bereits gesendete E-Mail oder eine Zahlung nicht rückgängig gemacht werden kann.

Vor einem Git-Eingriff bestimmen Sie den exakten Zielstand und die betroffenen Änderungen. Wenn die Arbeitskopie ungesicherte Arbeit anderer enthält, dürfen diese Dateien nicht kommentarlos verworfen werden. Ermitteln Sie zuerst ihre Eigentümerschaft. In einem gemeinsam genutzten Repository ist die sichere Wiederherstellung häufig eine gezielte Reparatur oder ein kontrollierter Revert statt eines globalen Resets.

Unterscheiden Sie zudem Git-Autor und reale Ausführungsidentität. Dass ein Commit unter einem bestimmten Namen gespeichert wurde, beweist nicht, welcher Agent die Arbeit tatsächlich ausgeführt oder welche Kampagne sie autorisiert hat. Für sicherheitsrelevante Aktionen braucht es zusätzliche gültige Autoritäts- und Ausführungsbelege.

Temporäre Worktrees können bei echten unabhängigen Arbeiten sinnvoll sein. Bleiben sie jedoch nach Abschluss bestehen, erzeugen sie veraltete Branches und Speicherverbrauch. Entfernen Sie nur jene temporären Arbeitsflächen, deren Zweck und Eigentümerschaft sicher geklärt sind, und erhalten Sie kanonische Artefakte und aktive Zwischenstände.

## 5. Wiederkehrende Fehler systemisch behandeln

Ein einzelner fehlgeschlagener Test rechtfertigt keine neue strategische Kampagne. I3 untersucht, korrigiert und wiederholt ihn innerhalb des gültigen Charters. Wenn derselbe Fehlertyp aber mehrfach zurückkommt, ist es ein Zeichen dafür, dass die bisherige Diagnose zu eng war.

Nehmen wir eine Mitgliedersuche, bei der nach jeder Korrektur andere Umlaute oder Namensformen scheitern. Statt nacheinander zehn neue Spezialfälle einzubauen, muss I3 die Ursache im ganzen Suchpfad untersuchen: Datenspeicherung, Kodierung, Normalisierung, Vergleichsregeln, Index, API und Darstellung. Eine unabhängige Prüfung sollte dabei bewusst gegen die neue Lösung argumentieren und ungetestete Grenzfälle suchen.

Dies ist eine technische Vertiefung, keine neue Produktdefinition. Erst wenn die Ursache eine bisher unbekannte materielle Produkt- oder Sicherheitsentscheidung erzwingt, wird der Planner erneut eingeschaltet. Reine Implementierungsfehler bleiben in der operativen Verantwortung. Dadurch entstehen weniger unnötige Freigabeschleifen, aber die Qualitätsanforderungen bleiben erhalten.

Auch die Tests selbst können falsch sein. Ein Evaluator, der ein unzulässiges Ergebnis akzeptiert, braucht Reparatur. Ein Evaluator, der eine vollständig erfüllte Fähigkeit wegen einer irrelevant gewordenen Formalie blockiert, ebenso. Die Anpassung muss begründet werden, darf aber nicht heimlich einen fachlich notwendigen Gate entfernen.

## 6. Sicherheit, Datenschutz und Rechte Dritter

Bei einem Sicherheitsvorfall begrenzen Sie den betroffenen Zugriff und bewahren die relevanten Belege, soweit rechtlich und organisatorisch zulässig. Verschicken Sie keine Geheimnisse in einen öffentlichen Fehlerbericht. Maskieren Sie sensible Werte in Logs und geben Sie nur die für die Diagnose erforderlichen Informationen weiter.

Wenn die Vereinsanwendung echte Kontakt- und Zahlungsdaten enthält, testen Sie Fehler möglichst mit synthetischen oder geeigneten anonymisierten Daten. Die Nutzung realer personenbezogener Daten in einem externen KI-Dienst erfordert eine eigene rechtliche und produktseitige Prüfung. Die bloße Verfügbarkeit einer API ist keine entsprechende Freigabe.

Bei externen Aktionen muss man zwischen reversibler Simulation und realer Wirkung unterscheiden. Ein Test, der eine E-Mail vorbereitet, ist nicht dasselbe wie ihr Versand. Das Erzeugen eines Rechnungsentwurfs ist nicht die Belastung eines Zahlungsmittels. Eine lokale Bildvorschau ist nicht automatisch die öffentliche Veröffentlichung eines fremden Werkes.

Bewerten Sie Lizenzen und Nutzungsrechte angemessen. Ein öffentliches Framework mit MIT-Lizenz kann Drittbibliotheken, Bilder oder Dienste verwenden, deren Bedingungen anders sind. Weder die Nennung eines Links noch ein bestandener Unit-Test ersetzt die Beachtung dieser Bedingungen.

## 7. Nachweisbare Rückkehr zum Betrieb

Eine Wiederherstellung ist erst abgeschlossen, wenn der relevante Zustand wieder sicher benutzt werden kann. Dies verlangt mehr als das Verschwinden einer Fehlermeldung. Zeigen Sie den korrigierten Kandidaten, die genutzte Sicherung oder Transaktionsquittung, die relevanten bestandenen Prüfungen und die aktuelle Einschränkung.

Nach einer Datenbankkorrektur kontrollieren Sie beispielsweise nicht nur, dass die Anwendung startet. Prüfen Sie, ob alle erwarteten Mitglieder vorhanden sind, Zahlungen nicht doppelt gezählt werden, Berechtigungen weiterhin greifen und ein erneuter Wiederanlauf dieselbe korrekte Wirkung besitzt. Nach einem UI-Fehler kann eine tatsächliche Bedienprobe erforderlich sein.

Der gültige Zustand wird auf der passenden kanonischen Oberfläche festgehalten. Ein alter Fehlerbericht bleibt historische Evidenz, darf aber nicht weiterhin wie der aktuelle Status aussehen. Ebenso darf eine als „recovered“ markierte Kampagne keinen neuen unbestätigten Produktionsstand verbergen.

Wenn die Wiederherstellung nicht sicher abgeschlossen werden kann, dokumentieren Sie präzise, was fehlt. Bleibt beispielsweise unklar, ob eine Zahlung schon extern ausgeführt wurde, dürfen Sie sie nicht erneut auslösen. Die nächste sichere Handlung ist dann ein lesender Nachweis oder eine ausdrücklich koordinierte Prüfung.

## 8. Drei vollständige Wiederherstellungsfälle

**Fall A: Fehlende Python-Abhängigkeit.** Nach dem Scaffold schlägt die Validierung wegen eines fehlenden Moduls fehl. Der Entwickler prüft den aktiven Interpreter, die deklarierte Requirements-Datei und den Installationsstatus. Er installiert die dokumentierten Abhängigkeiten im richtigen Environment und wiederholt denselben Prüfpfad. Projektanforderungen, Product State und Kampagnen werden nicht verändert. Das Ergebnis ist eine reparierte lokale Umgebung, keine neue Produktfreigabe.

**Fall B: Unterbrochene Datenbankmigration.** Eine Testmigration wurde während der Ausführung beendet. I3 stoppt weitere schreibende Zugriffe und prüft Migrationsjournal, Transaktionsstatus, Datenbankschema und verfügbare Sicherung. Anhand dieser Belege entscheidet er, ob die Migration sicher wiederholt, vervollständigt oder zurückgenommen werden kann. Eine zweite Ausführung ohne Kenntnis der ersten Wirkung ist unzulässig. Erst danach werden Datenintegrität, Startverhalten und relevante Regressionen nachgewiesen.

**Fall C: Veralteter Agentenbericht.** Ein früherer Bericht nennt die Mitgliedersuche „abgenommen“. Seitdem wurde der Code jedoch geändert, und der neue Stand ist nicht gegen dieselben Voraussetzungen geprüft. Der Planner hält die frühere Abnahme als historischen Beleg fest, erkennt aber fehlende Currentness. I3 prüft den tatsächlich aktuellen Kandidaten erneut und liefert einen frischen, exakt gebundenen Bericht. Der CLIENT prüft die sichtbare Nutzung, wenn das vereinbarte Gate dies verlangt.

Die drei Fälle zeigen unterschiedliche Ebenen: Infrastruktur, persistenter Zustand und Nachweisbindung. Ein einziges pauschales „alles neu starten“ löst diese Probleme nicht zuverlässig. Gute Wiederherstellung reagiert auf den tatsächlichen Wirkungsbereich.

## 9. Entscheidungsmatrix für sensible Operationen

| Geplante Handlung | Übliche technische Route | Zusätzliche Grenze |
| --- | --- | --- |
| Logdatei lesen | Lesende Diagnose | Geheimnisse nicht unnötig ausgeben |
| Unit-Test lokal wiederholen | I3 innerhalb des Charters | Geprüften Kandidaten festhalten |
| Testdatenbank aus Backup wiederherstellen | I3 nach Zustandsprüfung | Ziel und Wiederholbarkeit eindeutig |
| Produktionsdatenbank zurücksetzen | Explizite autorisierte Recovery | Datenverlust, Rechte und Sicherungen prüfen |
| Externe Zahlung erneut senden | Nicht allein aus einem Fehlerbericht | Vorherige Wirkung und CLIENT-Freigabe klären |
| Fremde Bilder öffentlich nutzen | Rechtliche und produktspezifische Prüfung | Lizenz und Nutzungsumfang beachten |
| Laufenden Charter umbenennen | Keine gültige Reparatur | Identität und tatsächliche Autorität rekonstruieren |
| Bereits bestätigte Anforderung ändern | CLIENT und strategischer Eigentümer | Supersession dokumentieren |

Diese Matrix ist eine Orientierung. Sie ersetzt keine konkrete Projektpolitik und keine notwendige Rechts- oder Sicherheitsbewertung. Sie hilft aber, alltägliche technische Korrekturen von materiellen externen Eingriffen zu unterscheiden.

## 10. Was grüne Validierung nicht aussagt

Ein erfolgreicher Test der Steuerungsebene zeigt ihre formale Funktionsfähigkeit innerhalb der geprüften Umgebung. Er zeigt nicht, dass alle Anwendungsfunktionen integriert, alle Daten migrationssicher, alle Rechte korrekt konfiguriert oder alle Oberflächen benutzbar sind. Auch ein erfolgreich erzeugtes PDF oder ein gültiges Manifest beweist nicht, dass ein völlig anderes Produkt richtig arbeitet.

Halten Sie Gates getrennt. Unit prüft kleine technische Einheiten; Integration prüft Zusammenspiel; DB/Currentness prüft aktuelle Zustandsbezüge; semantische Prüfung testet die richtige Bedeutung und Generalisierbarkeit; Physical prüft tatsächliche Ausführung; Perceptual prüft die menschliche Wirkung; Release bewertet die Freigabe des konkreten Pakets. Fehlende Gates dürfen nicht durch ein benachbartes PASS ersetzt werden.

Nicht jede Fähigkeit benötigt jeden denkbaren Gate in maximaler Tiefe. Die Auswahl muss zu Risiko und Nutzung passen. Wer aber ausgerechnet einen relevanten Gate auslässt, muss die entsprechende Unsicherheit offen lassen. So bleibt der Nachweis ehrlich und verhältnismäßig.

## 11. Feedback und Telemetrie des Starters

Die v1.4-Installation kann standardmäßig einen lokalen Metadatenbericht für Architekturfeedback vorbereiten. Dieser Bericht ist nicht die vollständige Quellcodeübertragung an einen Maintainer. Der periodische Workflow ist von der lokalen Berichtserstellung getrennt, und eine externe Sammlung wird dadurch nicht automatisch eingerichtet.

Falls keinerlei Berichtserstellung gewünscht wird, setzen Sie in der installierten Datei .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json den Wert enabled auf false. Der Parameter --no-feedback-workflow deaktiviert lediglich die Zeitplanung. Lesen Sie die [Datenschutzregel](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md), bevor Sie die Einstellung ändern.

Bei einem vermeintlichen Telemetrieproblem prüfen Sie zunächst den tatsächlichen Ausführungspfad und den Inhalt des erzeugten lokalen Berichts. Eine geplante GitHub-Actions-Ausführung im eigenen Repository ist nicht dasselbe wie eine Übermittlung an einen fremden Server. Behaupten Sie weder eine externe Datenübertragung noch deren Abwesenheit, ohne den realen Pfad zu untersuchen.

Eine sichere Incident-Kultur schützt Daten und Belege, ohne jeden Alltagsschritt durch formale Eskalationen zu blockieren. Sie erkennt den ursächlichen Eigentümer, repariert dessen System und lässt eine neue Sitzung die echte Fortsetzung rekonstruieren.

**Weiter:** Kapitel 06, Fähigkeiten abschließen.

## Quellen und Gültigkeit

- [Currentness und Rekonstruktion](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md)
- [Transaktionswiederherstellung](../../../12_TRANSACTION_RECOVERY.md)
- [Sicherheit und externe Aktionen](../../../../protocols/SECURITY_PRIVACY_RIGHTS_AND_EXTERNAL_ACTIONS.md)
- [Repository- und Worktree-Hygiene](../../../../protocols/REPOSITORY_EFFICIENCY_AND_WORKSPACE_HYGIENE.md)
- [Review- und Terminalintegrität](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Architekturfeedback und Datenschutz](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md)
- [Zustandsprüfung](../../../../tools/project_status.py)

Die Beispiele verwenden fiktive Vereinsdaten und begründen keine Schreibberechtigung für produktive Systeme.
