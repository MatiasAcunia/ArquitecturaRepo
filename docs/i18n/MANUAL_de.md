# ArquitecturaRepo — Praxishandbuch v1.4.0 (Deutsch)

Dieses Handbuch führt in acht Schritten (00–07) durch die Nutzung von **v1.4.0** im eigenen Projekt. Es ist ein **neuer praxisorientierter Leitfaden**, keine vollständige Übersetzung des archivierten spanischen v1.3-Handbuchs. Verbindliche veröffentlichte Quellen sind das unveränderliche [v1.4.0-Release und seine Dateien](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0); v1.3.0 bleibt als ältere Version verfügbar.

## 00 · Zweck und Grenzen

ArquitecturaRepo ist eine **repositorylokale Steuerungsschicht** für Anforderungen, Entscheidungen, Zuständigkeiten, aktuellen Status, Kampagnen, Nachweise und Wiederaufnahme nach Unterbrechungen. Es ist weder ein automatischer App-Generator noch ein Ersatz für Codex.

- CLIENT bestimmt Produktziele, sensible Freigaben und die menschliche Abnahme.
- I1 koordiniert bei Bedarf mehrere Projekte; I2 Planner plant Fähigkeiten, Schnittstellen und Abnahmekriterien.
- I3 Controller entwickelt, testet, integriert und behebt Fehler innerhalb der genehmigten Kampagne.
- I4 liefert optionale Spezialarbeit; **vier Rollen erfordern nicht vier Agenten**.

Deine Anwendung darf privat bleiben. Der öffentliche Starter benötigt weder den Quellcode noch Datenbankinhalte, Geheimnisse oder Chatverläufe. Externe Modellanbieter und Zugriffsrechte müssen gesondert genehmigt werden; durch die Installation wird nichts davon freigeschaltet.

## 01 · Sichere Installation

Verwende Python 3.12 (in CI getestet). Lade das [portable v1.4.0-ZIP](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/download/v1.4.0/ArquitecturaRepo-v1.4.0-portable.zip) herunter, überprüfe die veröffentlichte `.sha256`-Prüfsumme, entpacke es und öffne ein Terminal **im entpackten Framework-Verzeichnis**. Alternativ kannst du den unveränderlichen Git-Tag `v1.4.0` verwenden.

Bei neuen Anwendungen oder vorhandenem Code **ohne bestehende kanonische Steuerung** beginne mit `SMALL`:

```bash
python "tools/scaffold_project.py" --target "../mein-projekt" --profile SMALL --product-id MEIN_PROJEKT --objective "Anfangsziel noch zu bestätigen" --language de --no-feedback-workflow
```

Windows PowerShell:

```powershell
python "tools\scaffold_project.py" --target "..\mein-projekt" --profile "SMALL" --product-id "MEIN_PROJEKT" --objective "Anfangsziel noch zu bestätigen" --language "de" --no-feedback-workflow
```

Der Installer ergänzt `.agentic-sdlc/`, erhält vorhandenen Anwendungscode und Workflows und verweigert das Überschreiben bestehender Steuerungsdaten. `--no-feedback-workflow` deaktiviert nur den monatlichen Zeitplan, **nicht** den lokalen Berichtsgenerator. Für vollständige Deaktivierung `enabled=false` in `.agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json` setzen. Es wird kein externer Feedbackempfänger mitgeliefert.

Führe dann **im Zielprojekt-Verzeichnis** aus:

```bash
python -m pip install -r ".agentic-sdlc/requirements-validation.txt"
python ".agentic-sdlc/tools/project_status.py" --control-root ".agentic-sdlc"
python ".agentic-sdlc/tools/discover_project.py" --project-root "."
python ".agentic-sdlc/tools/reconstruct_context.py" --root ".agentic-sdlc"
```

In PowerShell stehen die Pfade in Anführungszeichen und verwenden `\`. Der Anfangsstatus `HOLD / UNTRUSTED_CONTEXT` ist **erwartet**: Produktbasis und Befugnisse müssen erst geprüft werden. Bestehende Product-State- oder Controller-Installationen **nicht überschreiben**! Dafür dient die [schreibgeschützte Vorprüfung](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/32_EXISTING_GOVERNED_ATTACHMENT.md). Eine universelle automatische Migration von v1.2/v1.3 existiert nicht.

## 02 · Planner und Übernahme

Untersuche echte Anforderungen, Quellcode, Daten, Schnittstellen, Risiken und technische Abhängigkeiten. CLIENT bestätigt die Produktbasis. I2 erstellt einen **fähigkeitsorientierten** Charter mit Ziel, Grenzen, Verantwortlichen, Abnahmeprüfungen und Gegenbeweisen. Synthetischen Beispiel-Product-State niemals als aktuellen Projektstatus übernehmen.

## 03 · Tagesgeschäft

Maßgeblich sind Git, CURRENT-Daten und reale Nachweise, nicht nur Chat-Zusammenfassungen. I3 übernimmt Umsetzung, Tests, Refactoring, Fehlerbehebung und Wiederaufnahme innerhalb **derselben autorisierten Kampagne**. Nicht jeder Bug braucht einen neuen Plan. Bei Konflikten zwischen Git, SQLite-WAL, Identität und Lease gilt `HOLD`. Native Codex-Desktop/Goals-Aktionen und Drittanbieter werden durch portable CI **nicht** zugesichert.

## 04 · Änderungen anfordern

Beschreibe sichtbares Ergebnis, Einschränkungen und Abnahmetest. Beispiel: „Überfällige Mitgliedsbeiträge anzeigen, vorhandene Zahlungen erhalten; Test mit bezahlten und offenen Monaten“. I2 beurteilt strategische Auswirkungen; I3 bearbeitet interne Änderungen innerhalb des freigegebenen Charters.

## 05 · Fehler und Wiederherstellung

- `UNTRUSTED_CONTEXT`: Projektwahrheit rekonstruieren, Status nicht künstlich auf „grün“ setzen.
- `jsonschema` fehlt: Abhängigkeiten aus `requirements-validation.txt` installieren.
- `EXISTING_CONTROL_PRESERVED`: stoppen, schreibgeschützten Weg verwenden; kein `--force`, keine Löschung.
- Git-, SQLite-WAL- oder Lease-Konflikte: materielle Änderungen bis zur Klärung anhalten.
- Unterbrochene Kampagne: Journal, Laufidentität und Artefakte bewahren und **dieselbe** Kampagne fortsetzen. Aufräumen nur mit geprüfter Zuständigkeit.

Öffentliche Issues enthalten nur reproduzierbare Schritte und bereinigte Logs, keine privaten Namen, Pfade, Zugangsdaten, Projektdaten oder Gespräche.

## 06 · Fähigkeitsabnahme

Unit-, Integrations-, DB/Currentness-, Semantik-, physische, menschlich-perzeptuelle und Release-Prüfung sind **getrennte** Gates. Erfolgreiche Tests allein bedeuten keine Produktabnahme. Version, Eingaben, Belege, Verantwortliche und Entscheidung gehören in die kanonischen Projektdateien. Synthetische CI zertifiziert keine beliebigen Produktivsysteme.

## 07 · Beispiel: Mitgliederverein

1. CLIENT wünscht Mitgliederverwaltung, Beiträge und Übersicht offener Zahlungen.
2. I2 prüft das tatsächliche Datenmodell und die Berechtigungen und grenzt einen kleinen End-to-End-Fall ab.
3. I3 implementiert Mitglied → Beitrag → Rückstandsübersicht und testet die Datenhaltung.
4. Ein Berechnungsfehler wird in **derselben** Kampagne behoben.
5. CLIENT prüft die Oberfläche und akzeptiert oder meldet Mängel; Belege bleiben erhalten.

## Referenzen und Einschränkungen

[Kurzanleitung](README_de.md) · [FAQ](FAQ_de.md) · [Haupt-README](../../README.md) · [Verifizierter Umfang v1.4](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/46_V1_4_PUBLIC_START_AND_SUPPORT.md).

Dieses Handbuch ist keine Sicherheitszertifizierung, unabhängige Usability-Abnahme, native Host-Zusage oder gemessener Beweis für einen Vorteil gegenüber direkter Codex-Nutzung. Die MIT-Lizenz erfasst Fremdmaterial nicht automatisch.
