# 01 — Installation und Einrichtung

ArquitecturaRepo · Vollständiges Benutzerhandbuch · Ausgabe v1.4 · Deutsch

> Dieses Kapitel führt durch die Installation des öffentlichen Starters und erklärt die Grenze zur echten Übernahme in ein Projekt. Aktuelle Befehle und Unterstützungsgrenzen stehen in der [v1.4-Anleitung](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md). Eine erfolgreiche Installation bedeutet ausdrücklich nicht, dass die Anwendung verstanden, entwickelt oder abgenommen wurde.

## Kapitelübersicht

1. Die notwendige Arbeitsumgebung
2. Starter, Fork und eigentliche Anwendung
3. Sichere Prüfung vor einer Änderung
4. Passendes Installationsprofil wählen
5. Die Steuerungsebene anlegen
6. Prüfen, ohne einen Erfolg zu erfinden
7. Die erste Bestandsaufnahme
8. Bestehende Projekte behutsam übernehmen
9. Zugangsdaten, Anbieter und Feedback
10. Fehlerdiagnose und Abschlusskontrolle

## 1. Die notwendige Arbeitsumgebung

Die folgenden Beispiele benutzen Windows, PowerShell, Git und Python. Die Architektur ist nicht auf diese Kombination beschränkt. Sie können ein anderes Betriebssystem, einen anderen Git-Dienst oder eine eigene Entwicklungsumgebung verwenden. Wesentlich sind eine erreichbare Quellbasis, nachvollziehbare Versionen, geeignete Dateirechte und die Möglichkeit, die mitgelieferten Prüfwerkzeuge auszuführen.

Für den portablen v1.4-Starter wurde Python 3.12 in der öffentlichen Continuous Integration getestet. Kontrollieren Sie zunächst die tatsächlich aktive Version. In PowerShell können Sie beispielsweise ausführen:

    & "python" --version
    & "py" --version

Falls beide Befehle scheitern, prüfen Sie, ob Python installiert und über den aktuellen Terminalpfad erreichbar ist. Installieren Sie nur aus einer vertrauenswürdigen Quelle. Ein fehlgeschlagener Befehl ist kein Grund, Dateien im Anwendungsprojekt vorschnell zu löschen. Halten Sie die Fehlermeldung und den Exitcode fest und untersuchen Sie die Ursache.

Sie benötigen keine eigene leistungsfähige Grafikkarte, wenn ein ausdrücklich freigegebener externer Programmierdienst die Rechenarbeit übernimmt. Umgekehrt zwingt Sie das Framework zu keinem solchen Dienst. Der lokale Starter selbst setzt keine automatische Modellanmeldung voraus. Lassen Sie die Frage, ob ein KI-Werkzeug später eingesetzt werden soll, zunächst getrennt von der Installation.

Kontrollieren Sie außerdem Speicherplatz und den geplanten Zielort. Quellcode, abgeleitete Artefakte, Cache-Verzeichnisse und zusätzliche Arbeitsbäume können sich unbemerkt vervielfachen. Verwenden Sie nach Möglichkeit einen dauerhaften Checkout pro Repository und räumen Sie temporäre Ausgaben auf, wenn sie nicht mehr als gültiger Nachweis gebraucht werden. Eine Kopie „für alle Fälle“ ist kein belastbarer Grund für zusätzlichen Speicherverbrauch.

## 2. Starter, Fork und eigentliche Anwendung

Das häufigste Missverständnis besteht darin, dass jemand ArquitecturaRepo öffnet und anschließend einen Agenten bittet, dort seine Kundenanwendung zu programmieren. Das Ausgangsrepository enthält aber die allgemeinen Protokolle, Vorlagen und Werkzeuge. Die Anwendung, die gebaut werden soll, hat normalerweise ein eigenes Repository. Die Steuerungsebene wird in diese Anwendung installiert.

| Ort | Zweck | Wichtige Abgrenzung |
| --- | --- | --- |
| ArquitecturaRepo | Öffentlicher Quellstand des Starters mit Protokollen und Tests | Enthält nicht automatisch Ihre Produktanforderungen |
| Eigener Fork, falls benötigt | Angepasste Variante des Starters | Ist noch keine Kundenanwendung |
| Eigenes Anwendungsrepository | Tatsächlicher Code, Daten, Konfiguration und übernommene Steuerungsebene | Darf keine erfundenen Beispielzustände übernehmen |

Eine plausible lokale Ordnung ist etwa:

    C:\Projekte\
        ArquitecturaRepo\
        verein-app\

Die Namen sind Beispiele. Entscheidend ist, dass das Installationswerkzeug im Starter aufgerufen wird und sein Zielparameter eindeutig auf die vorgesehene Anwendung zeigt. Die anschließend erzeugte Ordnerstruktur trägt den Namen .agentic-sdlc/. Sie ist ein organisatorischer Bestandteil der Anwendung, keine zweite Anwendung.

Wenn Sie keine dauerhaften Anpassungen am Starter vornehmen, genügt ein normaler Checkout oder ein geprüftes Release-Archiv. Für eigene Erweiterungen kann ein Fork sinnvoll sein. Kopieren Sie aber niemals den beispielhaften Product State eines synthetischen Projekts als echte Wahrheit in Ihre Anwendung. Solche Dateien enthalten absichtlich erfundene IDs, Anforderungen und Zustände, damit Tests reproduzierbar bleiben.

Beziehen Sie die veröffentlichte Ausgabe vorzugsweise aus dem [v1.4.0-Release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0). Vergleichen Sie ZIP und veröffentlichte SHA-256-Prüfsumme und bewahren Sie die Versionsidentität nachvollziehbar auf. Der Branch main kann nach dem Release weiterentwickelte Dokumentation enthalten. Auch ein vollständig lesbares Handbuch auf main ist nicht rückwirkend Teil des früher gepackten ZIP.

## 3. Sichere Prüfung vor einer Änderung

Öffnen Sie das Terminal zuerst im Starter und vergewissern Sie sich, dass Sie nicht versehentlich in einem anderen Repository stehen. Drei lesende Kontrollen reichen häufig für den Anfang:

    Get-Location
    & "python" --version
    & "git" status --short

Der erste Befehl zeigt Ihren aktuellen Ort. Der zweite prüft die Interpreterverfügbarkeit. Der dritte meldet vorhandene Git-Änderungen. Zeigt Git eine veränderte oder unversionierte Datei an, sollten Sie sie nicht einfach verwerfen, um einen vermeintlich sauberen Zustand herzustellen. Finden Sie zunächst heraus, wer sie erzeugt hat und ob sie zum aktuellen Projekt gehört.

Prüfen Sie anschließend den Zielpfad separat. Ein Agent kann eine andere Arbeitsmappe geöffnet haben als das Terminal. Ein GitHub-Desktopfenster kann den Starter anzeigen, obwohl Sie Ihre Anwendung ändern wollten. Die bloße Anmeldung an einen Dienst sagt nichts darüber aus, ob das richtige Repository, der richtige Branch und die notwendigen Rechte ausgewählt sind.

Wenn die Zielanwendung bereits über Daten, Migrationen, aktive Kampagnen, eine Steuerungsebene oder vorhandene Schutzregeln verfügt, überspringen Sie den normalen Installationsschritt. Verwenden Sie stattdessen die [lesende Prüfung für bereits geregelte Projekte](../../../32_EXISTING_GOVERNED_ATTACHMENT.md). Eine neue Installation darf vorhandene gültige Informationen nicht überschreiben, auch wenn der Zielordner älter aussieht als die aktuelle Version des Starters.

## 4. Passendes Installationsprofil wählen

Die Profile beschreiben Anforderungen des Projekts, keine Rangliste der verwendeten KI-Modelle. Die verbindliche Definition steht in [profiles.json](../../../../profiles/profiles.json). Wählen Sie das einfachste Profil, das die nachgewiesenen Risiken sinnvoll abbildet.

| Profil | Typischer Anlass |
| --- | --- |
| SMALL | Einfaches Projekt mit begrenzter Zustands- und Betriebsgefahr |
| STATEFUL | Dauerhafte Benutzerdaten, Datenbankmigrationen, Backups oder Wiederherstellung |
| ARTIFACT_HEAVY | Viele oder große erzeugte Dateien mit Speicher-, Herkunfts- und Lebenszyklusfragen |
| MULTI_WORKSTREAM | Mehrere getrennt geplante Arbeitsbereiche für ein gemeinsames Produkt |
| MULTI_PRODUCT | Mehrere Produkte mit gemeinsam genutzter Infrastruktur oder Regeln |
| HIGH_CONSEQUENCE | Besonders wichtige Sicherheits-, Datenschutz-, Finanz- oder andere schwer rückgängig zu machende Auswirkungen |

Ein kleines Lernprojekt beginnt oft sinnvoll mit SMALL. Für eine Mitgliederverwaltung, die langfristige Zahlungsdaten führt, ist STATEFUL zu prüfen. Die Anwesenheit einer Datenbank macht einen Master Owner jedoch nicht automatisch erforderlich. Eine besonders anspruchsvolle Bezeichnung erhöht weder die Sicherheit noch die Produktqualität, wenn die dazugehörigen realen Nachweise fehlen.

Notieren Sie die Gründe für das Profil kurz und überprüfbar. Wenn sich der Umfang später verändert, wird die Auswahl anhand der neuen Fakten neu bewertet. Ein Profil berechtigt nicht automatisch zu Produktionsänderungen, Datenverarbeitung oder kostenpflichtigen Diensten.

## 5. Die Steuerungsebene anlegen

Im geprüften v1.4-Starter können Sie für ein neues, noch nicht geregeltes Projekt beispielsweise folgenden PowerShell-Aufruf verwenden:

    & "python" "tools\scaffold_project.py" --target "..\mein-projekt" --profile "SMALL" --product-id "MEIN_PROJEKT" --objective "Anfangsziel; Bestätigung ausstehend" --language "de" --no-feedback-workflow

Die Parameter sind bewusst sichtbar. target bezeichnet das genaue Zielverzeichnis. profile wählt die Kontrollfamilie. product-id ist eine projektspezifische Kennung. objective ist lediglich eine vorläufige Zielbeschreibung, solange die Anforderungen noch nicht bestätigt sind. language de wählt die deutsche installierte Dokumentation und Rückmeldungen.

Für das spätere Beispiel einer Vereinsverwaltung mit langfristigen Mitglieder- und Beitragsdaten könnte die Auswahl anders aussehen:

    & "python" "tools\scaffold_project.py" --target "..\verein-app" --profile "STATEFUL" --product-id "VEREIN_APP" --objective "Mitglieder und Beiträge verwalten" --language "de" --no-feedback-workflow

Die beiden Beispiele sollen nicht nacheinander auf dasselbe Verzeichnis angewendet werden. Entscheiden Sie sich für das tatsächlich passende Profil und prüfen Sie den Pfad vor dem ersten Aufruf. Der Starter soll bestehende Anwendungscodes und Arbeitsabläufe erhalten. Trifft er auf eine vorhandene kanonische Steuerungsebene, muss eine gewöhnliche Neuinstallation verweigert werden.

Ein erster Zustand HOLD / UNTRUSTED_CONTEXT ist beabsichtigt. Er besagt: Die Steuerungsebene wurde erzeugt, kennt aber die aktuellen Anforderungen und technischen Fakten Ihrer Anwendung noch nicht. Die sichere Einrichtung darf keinen erfolgreichen Product State, keine bestätigte Datenbankversion und keine gültige Entwicklungskampagne erfinden.

Die optionale Einstellung --with-runtime ergänzt Referenzmechanik für Kampagnen. Sie startet damit weder einen externen Programmieragenten noch kauft sie API-Leistungen oder bestätigt die Ausführungsfähigkeit einer Desktopanwendung. Solche Behauptungen benötigen eigenständige Berechtigungen und Tests im tatsächlich vorgesehenen Umfeld.

## 6. Prüfen, ohne einen Erfolg zu erfinden

Nach erfolgreicher Einrichtung wechseln Sie in das Zielprojekt. Mit der dort installierten Steuerungsebene führen Sie die im öffentlichen Einstieg beschriebenen Prüfungen aus:

    & "python" -m pip install -r ".agentic-sdlc\requirements-validation.txt"
    & "python" ".agentic-sdlc\tools\project_status.py" --control-root ".agentic-sdlc"
    & "python" ".agentic-sdlc\tools\discover_project.py" --project-root "."
    & "python" ".agentic-sdlc\tools\reconstruct_context.py" --root ".agentic-sdlc"

Die erste Zeile installiert die deklarierte lokale Validierungsabhängigkeit. Die folgenden Befehle berichten erkannten Zustand, untersuchen das Projekt zunächst lesend und prüfen die Wiederherstellbarkeit des Kontexts. Ersetzen Sie diese Befehle nicht durch willkürliche Statusänderungen, wenn eine Prüfung noch HOLD meldet.

Ein erfolgreiches Scaffold hat drei einfache Belege: Der Ordner .agentic-sdlc/ liegt an der beabsichtigten Stelle, die bereits vorhandenen Anwendungsdateien sind erhalten und die Kontrollwerkzeuge lassen sich mit aussagekräftigen Ergebnissen aufrufen. Ein fehlendes Python-Paket wie jsonschema ist zuerst ein lokales Abhängigkeitsproblem. Es ist kein Anlass, eine aktuelle Anforderung oder eine Freigabe zu fälschen.

Der Aufruf discover_project ermittelt eine lesende Ausgangsbeschreibung. Er ist keine vollständige Sicherheitsprüfung Ihrer Datenbank. reconstruct_context soll sichtbar machen, welche Informationen für eine neue Sitzung noch fehlen. Dass diese Prüfung vor der Adoption keine arbeitsfähige Fortsetzung bescheinigt, ist ein korrektes Ergebnis.

Dokumentieren Sie den verwendeten Startersnapshot, die Zielumgebung und wichtige Ausgaben. Fragen Sie nicht nur, ob ein Prozess mit Exitcode null beendet wurde, sondern ob seine Aussage zum erwarteten Gate passt. Strukturvalidierung, fachliche Erfüllung und menschliche Benutzbarkeit sind verschiedene Dinge.

## 7. Die erste Bestandsaufnahme

Bevor die erste ernsthafte Produktfunktion beauftragt wird, braucht das System ein reales Bild der Anwendung. Verwenden Sie den [Installations- und Anpassungsleitfaden](../../../../prompts/INSTALL_THIS_SDLC.md), das [Produktentdeckungsgespräch](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md) und die [Übernahmeregeln](../../../16_TRANSFER_ADOPTION.md). Bei vorhandener Altsoftware ist zusätzlich die [Reankerung](../../../../prompts/REANCHOR_EXISTING_PROJECT.md) relevant.

Der Planner prüft, was schon existiert: Code, Datenmodelle, Schnittstellen, Deployment, relevante Betriebsumgebung und die letzten nachweisbaren Anforderungen. Er klärt mit dem CLIENT, welches Verhalten tatsächlich gewünscht wird. Danach hält er die bestätigten Produktanforderungen, technische Grundlage, Eigentumsverhältnisse, nächsten Lieferabschnitte und ihre Abnahmekriterien fest.

Diese Arbeit darf nicht durch das Kopieren von Beispiel-JSON ersetzt werden. Eine zufällige SHA, ein plausibel klingender Kampagnenname oder eine erfundene Datenbankkennung machen einen Validator vielleicht zufällig zufrieden, aber das Projekt anschließend unzuverlässig. Fehlende Fakten sind offen oder blockiert, bis sie tatsächlich belegt sind.

## 8. Bestehende Projekte behutsam übernehmen

Eine bestehende Anwendung kann eine wertvolle Historie besitzen, selbst wenn ihre Dokumentation unvollständig ist. Bewahren Sie die vorhandenen Dateien, aktiven Branches, Datenbanken und bereits gültigen Steuerungsregeln zunächst unverändert. Führen Sie eine lesende Bestandsaufnahme aus und vergleichen Sie ihre Ergebnisse mit den gewünschten neuen Kontrollen.

Unterscheiden Sie drei Fälle. Bei einem wirklich neuen Projekt kann das normale Scaffold verwendet werden. Bei einer bestehenden, aber noch nicht geregelten Anwendung ist ebenfalls eine vorsichtige Installation möglich, jedoch nur nach Prüfung des Zielordners. Bei einer bereits geregelten Anwendung ist der Attachment-Preflight erforderlich. Er beurteilt Konflikte und Kompatibilität, ohne durch blindes Überschreiben eine bisherige Verantwortungskette zu zerstören.

Auch ältere Starterversionen sind kein Anlass für ein unkontrolliertes Upgrade. Lesen Sie die [Upgrade-Grenzen](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md). Ein öffentlich unterstützter Installationsweg ist nicht automatisch eine geprüfte Migration für jedes Projekt und jeden Host.

## 9. Zugangsdaten, Anbieter und Feedback

Vergeben Sie nur die Rechte, die eine konkrete Handlung benötigt. Eine lesende Erkundung braucht normalerweise keine Berechtigung zum Löschen, Veröffentlichen, Bezahlen oder Ändern von Produktionsdaten. Bewahren Sie Passwörter, API-Schlüssel und private Zertifikate außerhalb öffentlicher Chatverläufe und des Repositorys auf. Stellen Sie sicher, dass eine Verbindung zu GitHub nicht versehentlich einen fremden Fork oder das Starterrepository anstelle Ihrer Anwendung verändert.

Der Starter unterstützt lokale, datensparsame Architektur-Rückmeldungen. In v1.4 ist ein kleiner Metadatenbericht standardmäßig lokal möglich; eine automatische externe Übermittlung an den Maintainer ist damit nicht eingerichtet. Der Parameter --no-feedback-workflow entfernt die periodische GitHub-Actions-Zeitplanung, deaktiviert aber nicht den lokalen Berichtsgenerator. Wenn Sie keinerlei Berichte wollen, setzen Sie enabled=false in .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json und prüfen die [Datenschutzbeschreibung](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md).

Diese Trennung ist absichtlich fein: Ein geplanter Workflow, ein lokal ausführbares Werkzeug und eine externe Übertragung sind unterschiedliche Handlungen. Die Zustimmung zu einer davon darf nicht als pauschale Freigabe für die anderen interpretiert werden.

## 10. Fehlerdiagnose und Abschlusskontrolle

| Beobachtung | Wahrscheinliche Bedeutung | Sichere Maßnahme |
| --- | --- | --- |
| Python wird nicht gefunden | Interpreter fehlt oder Pfad stimmt nicht | Interpreter und Terminal prüfen |
| Zielordner bleibt leer | Befehl scheiterte oder falsches Ziel gewählt | Zielparameter und Ausgabe vergleichen |
| HOLD / UNTRUSTED_CONTEXT | Projektfakten wurden noch nicht bestätigt | Mit lesender Discovery und Adoption fortfahren |
| jsonschema fehlt | Aktive Python-Umgebung hat keine Validierungsabhängigkeit | Deklarierte Requirements installieren |
| Vorhandener Steuerungsordner wird geschützt | Der Installer verweigert ein Überschreiben | Geregeltes Projekt zunächst lesend prüfen |
| Rekonstruktion meldet Widerspruch | Code, Autorität oder Zustand passen nicht zusammen | Ausgaben sichern und Ursache untersuchen |
| Der Agent sieht das falsche Repository | Arbeitsverzeichnis oder Werkzeugkontext ist falsch | Schreibzugriff anhalten und Pfade prüfen |
| Kontrolltests sind grün, die App startet nicht | Es wurde nicht das tatsächliche Produkt getestet | Reale Ausführung und Nutzerreise prüfen |

Wenn ein Fehler wiederkehrt, klassifizieren Sie ihn, bevor Sie etwas erneut installieren: Umgebung, Berechtigung, falscher Pfad, nicht unterstützte Version, fehlende Abhängigkeit, widersprüchliche aktuelle Referenz oder beschädigter Zustand. Beheben Sie die Ursache und bewahren Sie relevante Belege. Ein frischer Clone oder das Löschen des Steuerungsordners ist keine allgemeine Reparaturmethode.

Sie haben dieses Kapitel abgeschlossen, wenn die richtige Installation anhand ihres konkreten Pfades und Versionsstands nachgewiesen ist, vorhandener Anwendungscode unbeschädigt blieb und das System seine noch unbekannten Projektfakten ehrlich anzeigt. Der nächste Schritt ist nicht sofortige Entwicklung, sondern eine belastbare Übernahme des realen Projektzustands.

**Weiter:** Kapitel 02, Planner und Adoption.

## Quellen und Gültigkeit

- [GitHub-Release v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0)
- [Öffentlicher v1.4-Einstieg](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Versionen und Upgrade](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)
- [Fork und Bootstrap](../../../01_FORK_AND_BOOTSTRAP.md)
- [Übernahmevertrag](../../../16_TRANSFER_ADOPTION.md)
- [Prüfung bestehender Steuerung](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Metadatenfeedback und Datenschutz](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md)
- [Scaffold-Quellcode](../../../../tools/scaffold_project.py)

Die Beispiele sind keine Bestätigung für eine konkrete Installation oder für die reale Ausführung eines anderen Produkts.
