# Agentic SDLC FAQ (de)

[DE guide](README_de.md) · [Main README](../../README.md)

### 1. Was ist Agentic SDLC?

Eine wiederverwendbare Architektur zur Organisation agentengestützter Softwareentwicklung. Sie ist kein autonomer Generator für beliebige Anwendungen.

### 2. Wie beginne ich?

Forken oder prüfen Sie das Repository, beginnen Sie mit schreibgeschützter Bestandsaufnahme, wählen Sie das kleinste Profil und folgen Sie der Installationsanleitung. Ein neues Scaffold startet in HOLD.

### 3. Kann ich es in ein bestehendes Repo integrieren?

Ja. Rekonstruieren Sie zuerst tatsächlichen Code, Daten und Berechtigungen. Überschreiben Sie keine Anwendungsdateien und übernehmen Sie keine fiktiven Beispieldaten.

### 4. Brauchen vier Rollen vier Modelle?

Nein. CLIENT, Planner I2, Campaign Lead I3 und I4-Spezialisten beschreiben Verantwortlichkeiten, keine feste Prozesszahl.

### 5. Wer genehmigt sensible Änderungen?

Der CLIENT behält Produktentscheidungen, subjektive Abnahme, Veröffentlichung, Kosten und sensible Daten unter Kontrolle. I3 darf keine Freigaben erfinden.

### 6. Sind Goals und Codex Desktop schon integriert?

Noch nicht. v1.2 enthält optionale Goal-/Plan-Prüfungen, doch die echte Host-Integration bei jeder Ausführung muss erst nachgewiesen werden.

### 7. Ist Gemini erforderlich oder standardmäßig kostenpflichtig?

Nein. I4 ist deaktiviert, bis Einwilligung, Schlüssel, Kontingent und Datenschutz geprüft sind. Privater Code wird nicht standardmäßig übertragen.

### 8. Kann das Starter Codex-Chats neu starten oder löschen?

Nicht eigenständig. Codex Daily Control 2.0.2 ist eine separate Referenz; ein sicherer Host-Adapter ist in v1.2 noch nicht abgenommen.

### 9. Welches Feedback ist standardmäßig aktiv?

Ein kleiner monatlicher Metadatenbericht im GitHub-Actions-Artefakt des eigenen Projekts. Er unterstützt Verbesserungen, wird aber nicht automatisch extern gesendet.

### 10. Welche Daten fehlen absichtlich?

Code, Gespräche, Projekt-/Repositorynamen, Pfade, Zugangsdaten, Personenkennungen, Anforderungstext, SHA und beliebiger Freitext.

### 11. Wie ändere ich Sprache oder deaktiviere Feedback?

Verwenden Sie --language auto|en|es|pt|fr|de|it|ja|zh. Zum Abschalten enabled=false oder --no-feedback-workflow. GitHubs README bleibt statisch.

### 12. Was ist getestet und wie melde ich Fehler?

v1.1 ist stabil, v1.2 bleibt ein Kandidat bis zu unabhängigen Praxistests. Erstellen Sie ein Issue mit Reproduktionsschritten und bereinigten Logs. Originalmaterial steht unter MIT.

---

[DE guide](README_de.md)
