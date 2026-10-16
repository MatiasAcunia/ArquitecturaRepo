# Agenten-Kontinuitätsbrücke — Agent Continuity Bridge 0.2.1

## Zweck

ArquitecturaRepo verwaltet Entwicklungsbefugnisse, Pläne und Abnahme. Dieses optionale Modul trennt die Anbindung an einen externen, separat versionierten Kontinuitätscontroller. Es ist weder KI-Modell noch zusätzlicher Kampagnenverantwortlicher. Der portable Kern funktioniert ohne es.

## Derzeit geprüfte Funktionen

Offline-Prüfung eines separat bereitgestellten Codex-Daily-Control-3.1-ZIPs: sichere Pfade, Inventar, SHA-256, Version und Konfigurationskonsistenz; registriert den Paket-Hash in einem vorhandenen Projekt, prüft Aktualität und entfernt die eigene Registrierung sicher. Keine privaten Konfigurationen, Zugangsdaten oder Goal-IDs enthalten.

## Voraussetzungen und Anbindung

Python 3.10+; vorhandenes ArquitecturaRepo-Projekt mit .agentic-sdlc; extern beschafftes 3.1-ZIP. Der echte native Controller benötigt Windows, PowerShell 5.1, kompatibles Codex Desktop sowie separat konfiguriertes Git, SQLite und ggf. Drive/rclone. Die Brücke installiert diese Komponenten nicht.

## Sicherheit und Grenzen

3.1 ist ein Release-Kandidat ohne physische Windows-Abnahme. Native Abschlüsse, Desktop-Übergabe, Quoten-Wiederaufnahme und Remote-Lieferung bleiben hier deaktiviert/unverifiziert.

## CLI

```bash
python "bridge.py" inspect --package "CONTROLLER_3_1.zip"
python "bridge.py" install --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" status --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" uninstall --project "MY_PROJECT"
```


Installation in ein bestehendes Projekt: `python install_into_project.py --project "PROJEKT"`. Verwenden Sie `.agentic-sdlc/extensions/agent-continuity-bridge/pluginctl.py`. Vor `--remove` die Controllerregistrierung entfernen. Keine nativen Aktionen werden ausgeführt.
