# Agentic SDLC FAQ (de)

[DE guide](README_de.md) · [Praxishandbuch v1.4](MANUAL_de.md) · [Main README](../../README.md)

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

Nicht automatisch. v1.4 enthält portable Goal-/Plan- und Berechtigungsprüfungen; die native Codex-Desktop/Goals-Integration pro Ausführung erfordert weiterhin gesonderte physische Nachweise.

### 7. Ist Gemini erforderlich oder standardmäßig kostenpflichtig?

Nein. I4 ist deaktiviert, bis Einwilligung, Schlüssel, Kontingent und Datenschutz geprüft sind. Privater Code wird nicht standardmäßig übertragen.

### 8. Kann das Starter Codex-Chats neu starten oder löschen?

Nein. Der Starter startet, verwaltet oder löscht keine nativen Codex-Chats. Host-Adapter benötigen gesonderte Autorisierung und Nachweise; v1.4 zertifiziert keinen nativen Chat-Lebenszyklus.

### 9. Welches Feedback ist standardmäßig aktiv?

Ein kleiner monatlicher Metadatenbericht im GitHub-Actions-Artefakt des eigenen Projekts. Er unterstützt Verbesserungen, wird aber nicht automatisch extern gesendet.

### 10. Welche Daten fehlen absichtlich?

Code, Gespräche, Projekt-/Repositorynamen, Pfade, Zugangsdaten, Personenkennungen, Anforderungstext, SHA und beliebiger Freitext.

### 11. Wie ändere ich Sprache oder deaktiviere Feedback?

Verwenden Sie --language auto|en|es|pt|fr|de|it|ja|zh. Für die vollständige Abschaltung aller Berichte enabled=false setzen; --no-feedback-workflow deaktiviert nur die Zeitplanung. GitHubs README bleibt statisch.

### 12. Was ist getestet und wie melde ich Fehler?

Der Quellcode hat Version 1.4.0, gilt aber erst nach Veröffentlichung und Prüfung des [unveränderlichen v1.4.0 Tags, ZIPs und der Prüfsumme](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0) als Release; v1.3.0 bleibt verfügbar. Portable Linux/Windows-Tests bestätigen weder native Agenten-Hosts noch die Benutzbarkeit durch Dritte. Erstellen Sie ein Issue mit Reproduktionsschritten und bereinigten Logs. Originalmaterial steht unter MIT.

### 13. Lassen sich asynchroner Betrieb, Teamarbeit und KI ohne Programmierung kombinieren?

Ja, als Konfigurationsdimensionen. Tatsächliche Ausführung benötigt einen geprüften Host, Berechtigungen, Wiederherstellung und entsprechende Freigaben. SMALL bleibt einfach. I2 führt Anforderungen und Stack im kanonischen Repository; unnötige Commits und Branches sind verboten. Externes anonymes Feedback bleibt ohne verifizierten Empfänger unmöglich und abschaltbar.

---

[DE guide](README_de.md) · [Praxishandbuch v1.4](MANUAL_de.md)
