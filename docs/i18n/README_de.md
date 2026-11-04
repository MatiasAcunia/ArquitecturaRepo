# Agentic SDLC — Erste Schritte

[Kurzleitfaden v1.4](MINI_GUIDE_de.md) · [FAQ](FAQ_de.md)

Das [vollständige deutsche v1.4-Handbuch mit acht Kapiteln](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/v1.4/de/README.md) liegt im Quellrepository, zusammen mit seinem [58-seitigen PDF](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/output/pdf/ArquitecturaRepo_Vollstaendiges_Benutzerhandbuch_v1.4_DE.pdf). Das [historische spanische v1.3-Handbuch](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/ES/README.md) bleibt getrennt erhalten. Das v1.4.0-Release-ZIP wurde vor diesen Büchern veröffentlicht und enthält sie nicht. Diese Einstiegsseite, der Kurzleitfaden und die FAQ bleiben bewusst kompakt; aktuelle Befehle stehen in der [v1.4-Installationsanleitung](../46_V1_4_PUBLIC_START_AND_SUPPORT.md).

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

Für die vollständige Deaktivierung aller Berichte enabled=false in .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json setzen. Das Entfernen von .github/workflows/agentic-sdlc-feedback.yml oder --no-feedback-workflow deaktiviert nur die Zeitplanung, nicht den lokalen Berichtsgenerator.

## Sicherheit und Versionen

**v1.4.0 ist veröffentlicht**: Das [versionierte GitHub Release enthält ein portables ZIP und eine SHA-256-Prüfsumme](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0). Prüfe heruntergeladene Dateien vor der Installation; der veränderliche Branch `main` kann spätere Dokumentationsänderungen enthalten und ist nicht das Release-Artefakt. Das vorherige v1.3.0 Release bleibt verfügbar. Für neue oder bisher ungeregelte Projekte gilt die [v1.4-Einstiegsanleitung](../46_V1_4_PUBLIC_START_AND_SUPPORT.md); bereits geregelte Projekte benötigen zunächst eine [schreibgeschützte Prüfung](../32_EXISTING_GOVERNED_ATTACHMENT.md), keine automatische Überschreibung. Portable CI bestätigt weder native Codex-Desktop-Ausführung noch externe KI-Anbieter oder reale externe Aktionen.

## Sprachen

Das Installationswerkzeug erkennt die Systemsprache oder akzeptiert --language de. Die Dokumentation funktioniert offline. GitHub zeigt ein statisches Haupt-README; wählen Sie die Sprache über die Links.

[Kurzleitfaden v1.4](MINI_GUIDE_de.md) · [FAQ](FAQ_de.md) · [GitHub README](../../README.md)
