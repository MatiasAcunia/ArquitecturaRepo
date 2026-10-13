# Agentic SDLC — Erste Schritte

Eine wiederverwendbare, repositorybasierte Architektur für Softwareentwicklung mit Agenten. Sie bietet Rollen, dauerhaften Zustand, Planung, Wiederaufnahme und Prüfungen. Sie entwickelt nicht automatisch jede Software und ersetzt keine Produktentscheidungen.

## In einem Projekt installieren

Wählen Sie das kleinste passende Profil. Beginnen Sie mit schreibgeschützter Bestandsaufnahme und übernehmen Sie keinen Product State aus Beispielen. Neue Installationen starten mit HOLD / UNTRUSTED_CONTEXT.

```bash
python tools/scaffold_project.py --target "../my-project" --profile SMALL --product-id EXAMPLE --language auto
```

## Rollen und Befugnisse

Der CLIENT entscheidet über Produkt und sensible Freigaben; I2 verantwortet Strategie und Abnahme; I3 führt Entwicklung und Wiederherstellung innerhalb der Kampagne aus; I4 unterstützt optional begrenzt und unabhängig. Vier Rollen bedeuten nicht vier Prozesse.

## Datenschutz und monatliches Feedback

Neue Installationen erzeugen standardmäßig einmal monatlich einen kleinen Metadatenbericht als GitHub-Actions-Artefakt im eigenen Projekt. Das hilft, die Starter-Struktur zu verbessern und Fehler zu ordnen. Der Bericht geht nicht automatisch an den Maintainer. Er enthält weder Code, Gespräche, Projektnamen, Pfade, Kennungen noch Zugangsdaten.

Zum Deaktivieren enabled=false in .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json setzen, .github/workflows/agentic-sdlc-feedback.yml löschen oder mit --no-feedback-workflow installieren.

## Sicherheit und Versionen

Stabil ist Version 1.1.0. Version 1.2 ist ein Testkandidat: Codex Desktop Goal, Gemini, externe Effekte und Multiprojekt-Aufgaben benötigen noch physische Tests. Grüne CI ist keine Produktabnahme.

## Sprachen

Das Installationswerkzeug erkennt die Systemsprache oder akzeptiert --language de. Die Dokumentation funktioniert offline. GitHub zeigt ein statisches Haupt-README; wählen Sie die Sprache über die Links.

[FAQ](FAQ_de.md) · [GitHub README](../../README.md)
