# 02 — Planner und Projektübernahme

ArquitecturaRepo · Vollständiges Benutzerhandbuch · Ausgabe v1.4 · Deutsch

> Nach der Installation besitzt das Projekt eine Steuerungsebene, aber noch keinen automatisch gültigen Produktzustand. Dieses Kapitel beschreibt die Entdeckung, Bestätigung und Adoption. Maßgeblich sind die [Produktentdeckungsregeln](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md) und der [Adoptionsvertrag](../../../16_TRANSFER_ADOPTION.md).

## In diesem Kapitel

1. Warum der Gesprächsverlauf nicht der Projektzustand ist
2. Der erste lesende Rundgang
3. Produktfragen und technische Fragen trennen
4. Bestätigte Anforderungen erstellen
5. Technische Grundlage und Lieferplan
6. Adoption als überprüfbare Zustandsänderung
7. Der Test mit einem neuen Kontext
8. Den ersten Entwicklungsauftrag abgrenzen
9. Ein tatsächliches Erstgespräch
10. Häufige Fehler und Abnahme des Baselines

## 1. Warum der Gesprächsverlauf nicht der Projektzustand ist

Nach einer erfolgreichen Installation zeigt ArquitecturaRepo absichtlich einen vorsichtigen Ausgangszustand. Der Starter kennt das neue Produkt noch nicht. Ein in einem Beispielordner vorhandener Product State ist nicht die Beschreibung Ihrer Anwendung. Selbst wenn ein Assistent in einem Gespräch bereits eine perfekte Zusammenfassung der gewünschten Funktionen erzeugt hat, sind diese Aussagen noch nicht automatisch mit aktuellem Code, echten Daten und einer bestätigten Verantwortungskette verbunden.

Ein Planner muss daher eine systematische Bestandsaufnahme durchführen. Er klärt zwei unterschiedliche Bereiche: Welche Produktabsicht wurde vom CLIENT wirklich bestätigt? Und welche technische Situation lässt sich am vorhandenen Projekt nachweisen? Diese beiden Antworten können voneinander abweichen. Ein Auftraggeber kann einen Mitgliederexport wünschen, während die vorhandene Anwendung noch nicht einmal Mitglieder persistent speichert. Umgekehrt kann der Code alte Zahlungsfunktionen enthalten, die in der nächsten Version ausdrücklich nicht mehr verwendet werden sollen.

Die Aufgabe besteht nicht darin, ein möglichst beeindruckendes Dokument zu schreiben. Es geht um die Fähigkeit einer späteren Sitzung, gültige Entscheidungen und technische Tatsachen voneinander zu unterscheiden. Eine früher formulierte technische Hypothese darf durch neue physische Belege korrigiert werden. Eine tatsächlich neue Produktentscheidung muss zur aktuellen Anforderung promoviert werden, ohne die historische Entscheidung unkenntlich zu machen.

Sobald wesentliche Fakten fehlen, kennzeichnet der Planner diese als offen. Er ersetzt sie nicht durch allgemeine Branchenannahmen. Ein sicher wirkender, aber erfundener Datenbankstand ist gefährlicher als ein offen benannter unbekannter Stand, denn er kann falsche Migrationen oder Datenverluste auslösen. Dasselbe gilt für nicht bestätigte Freigaben, angeblich verfügbare Geheimnisse und vermeintlich „aktuelle“ Branches.

## 2. Der erste lesende Rundgang

Beginnen Sie mit den tatsächlich vorhandenen Arbeitsoberflächen. Der Planner ermittelt den Repositorypfad, den aktuellen Git-Stand, bestehende Änderungen, vorhandene Tests, Startbefehle, Datenbankkonfiguration, Umgebungsvarianten und etwaige bereits gültige Regelwerke. Falls ein Tool eine andere Arbeitsmappe verwendet, wird diese Abweichung zuerst geklärt.

Eine sinnvolle Inspektionsreihenfolge lautet:

1. Identität der Anwendung und ihr beabsichtigter Nutzerkreis.
2. Aktuelle Dateien und Branches; bekannte ungesicherte Änderungen bleiben erhalten.
3. Bereits vorhandene Anforderungen, Architekturentscheidungen und Produktzustände.
4. Technische Abhängigkeiten, Datenhaltung, externe Dienste und Startpfade.
5. Vorhandene Tests, reale Ausgaben und bekannte Fehlerberichte.
6. Gültige Rollen, Arbeitsfreigaben und Laufzeitbeschränkungen.
7. Unbekannte Fakten mit ihrer Auswirkung auf den nächsten Schritt.

Die Bestandsaufnahme erfolgt zunächst ohne destruktive Befehle und ohne externe Produktänderungen. Ein bestehendes Repository braucht normalerweise keinen neuen Clone. Eine funktionierende Datenbank muss nicht „vorsichtshalber“ neu angelegt werden. Denken Sie beim Arbeiten mit großen Dateien auch an temporäre Caches, Bilder und Artefakte; erhalten Sie nur jene Kopien, die eine konkrete Beweis- oder Wiederherstellungsfunktion besitzen.

Der [Product-Discovery-Prompt](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md) und die [technische Baseline-Regel](../../../../protocols/PRODUCT_DISCOVERY_REQUIREMENTS_AND_TECHNICAL_BASELINE.md) unterstützen diesen Rundgang. Sie sind Leitplanken für konkrete Belege, nicht ein Formular, das blind mit plausiblem Text gefüllt werden soll.

## 3. Produktfragen und technische Fragen trennen

Ein Kunde kann verantwortlich entscheiden, wer ein System nutzt, welche Informationen angezeigt werden sollen und was geschieht, wenn ein Vorgang fehlschlägt. Der Kunde muss nicht die Struktur des Datenbankindexes, die Retry-Strategie oder die Gruppierung interner Klassen bestimmen. Wenn die technische Umsetzung die Produktabsicht gefährdet, soll der Planner verständliche Alternativen und Konsequenzen erläutern.

| Frage an den CLIENT | Technische Verantwortung |
| --- | --- |
| Sollen mehrere Mitarbeiter gleichzeitig Datensätze bearbeiten? | Konkurrenzkontrolle, Transaktionen, Konfliktbehandlung |
| Was bedeutet „Mitglied deaktivieren“ fachlich? | Persistenzmodell, Beziehungen, Migrationsstrategie |
| Welche Informationen sind vertraulich? | Verschlüsselung, Zugriffskontrolle, Protokollierung |
| Muss die Anwendung ohne Internet funktionieren? | Lokale Speicherung, Synchronisierung, Wiederanlauf |
| Was soll spätestens zum vereinbarten Termin nutzbar sein? | Aufgabenteilung, Testarchitektur, Lieferfolge |
| Darf die Anwendung echte Zahlungen abwickeln? | Anbieterintegration nur nach gesonderter Autorisierung |

Stellen Sie Fragen so, dass eine Antwort die spätere Software verändert. „Soll der Button blau oder grün sein?“ ist sinnvoll, wenn eine visuelle Präferenz tatsächlich wichtig ist. „Welche SQL-Transaktion soll im Controller geöffnet werden?“ ist normalerweise keine Kundensache. Der Auftraggeber sollte sich auf Problem, Nutzer, Verhalten, Vertrauen, Risiken und subjektive Qualität konzentrieren können.

Ein gutes Discovery-Gespräch entdeckt auch Widersprüche. Ein Nutzer fordert vielleicht „alles endgültig löschen“, erwartet aber zugleich eine lückenlose Historie jeder Beitragszahlung. Beide Ziele können nicht ohne zusätzliche Regeln gleichzeitig erfüllt werden. Der Planner macht die Spannung sichtbar und holt eine Entscheidung ein, bevor eine irreversible Datenoperation gebaut wird.

## 4. Bestätigte Anforderungen erstellen

Die aktuelle Anforderungssammlung muss in normaler Sprache beantworten, was die Software tun soll und wie Erfolg beobachtet wird. Jede wesentliche Behauptung sollte auf eine echte CLIENT-Entscheidung oder eine ausdrücklich bestätigte bestehende Eigenschaft zurückführbar sein. Ein früheres Gespräch kann diese Herkunft belegen, reicht aber nicht als Beweis für den technischen aktuellen Zustand.

Für das Vereinsbeispiel könnte eine erste vorgeschlagene Grundlage lauten:

| Dimension | Vorgeschlagene erste Version | Status |
| --- | --- | --- |
| Hauptnutzer | Eine Verwaltungskraft am Vereinsrechner | Bestätigung erforderlich |
| Mitgliedsdaten | Name, Kontakt und Mitgliedsstatus | Bestätigung erforderlich |
| Beiträge | Beitragspflicht, Zahlungen und Historie | Bestätigung erforderlich |
| Deaktivierung | Historische Zahlungen bleiben erhalten | Bestätigung erforderlich |
| Netzwerk | Zunächst lokal, nicht öffentlich im Internet | Bestätigung erforderlich |
| Oberfläche | Lesbare Masken und verständliche Fehlermeldungen | Bestätigung erforderlich |
| Wiederherstellung | Backup-Intervall und maximaler Datenverlust | Offen |
| Ausschlüsse | Keine Onlinezahlung und keine mobile App | Bestätigung erforderlich |

Diese Tabelle ist absichtlich ein Vorschlag, kein behaupteter Istzustand. Der CLIENT korrigiert sie und bestätigt die Produktanforderungen. Danach kann die technische Rolle daraus konkrete Prüfbedingungen ableiten. Wird später eine Entscheidung ersetzt, muss die gültige Fassung klar erkennbar bleiben.

Eine gute Anforderung beschreibt Grenzfälle. Wer darf Mitglieder deaktivieren? Was passiert bei einem doppelten Eintrag? Darf ein Mitglied ohne Telefonnummer angelegt werden? Bleibt eine Zahlung nach einer Namensänderung auffindbar? Wie wird ein Fehleintrag korrigiert? Wenn die Antwort funktional wichtig ist, soll sie nicht dem Zufall einer Implementierung überlassen werden.

Schreiben Sie aber nicht jede winzige UI-Operation in einen eigenen strategischen Vertrag. Ziel ist eine zusammenhängende Fähigkeit, die sich vom Nutzerproblem bis zum Test verfolgen lässt. Zu viele getrennte Mikrotickets können den Zusammenhang zerstören und das Projekt stärker verlangsamen als fehlende Dokumentation.

## 5. Technische Grundlage und Lieferplan

Nach der Produktbestätigung bestimmt der Planner die technische Baseline. Sie umfasst mindestens die relevanten Laufzeitversionen, Programmiersprache oder Stack, Datenbank, Sicherheits- und Netzwerkgrenzen, Start- und Bereitstellungspfad sowie die Möglichkeiten zur Sicherung und Wiederherstellung. Diese Angaben müssen zum tatsächlich vorhandenen System passen, nicht nur zu einem bevorzugten Architekturentwurf.

Eine Technologieauswahl ist eine begründete ingenieurtechnische Entscheidung. Für eine lokale Anwendung kann eine eingebettete Datenbank geeignet sein; für mehrere gleichzeitige Nutzer können andere Anforderungen entstehen. Der Planner wägt Fehlerfolgen, Wartbarkeit, Personal, Betrieb und Lieferfrist ab und hält die Entscheidung mit ihrer Gültigkeit fest. Nicht jede erfolgreiche Demonstration beweist, dass dieselbe Architektur später für Internetbetrieb oder hohen Durchsatz geeignet ist.

Der Lieferplan verbindet das bestätigte Ziel mit erreichbaren Terminen und Fähigkeiten. Er enthält nicht zwingend einen riesigen Gantt-Plan. Ein sinnvoller erster Abschnitt kann Mitglieder anlegen und wiederfinden, ein zweiter Beiträge erfassen, ein dritter Auswertungen anzeigen. Jede Fähigkeit sollte ein beobachtbares Ergebnis und passende Akzeptanzkriterien besitzen.

Priorisieren Sie nach Nutzwert, Voraussetzungen und Risiko. Eine Datenbankmigration mit Verlustgefahr braucht zusätzliche Kontrollen. Eine unsichere externe Schnittstelle darf nicht nur deshalb zuerst kommen, weil ein Agent sie besonders leicht generieren kann. Gleichzeitig sollte der Planner keine theoretische Vollständigkeit verlangen, die das erste echte Nutzerfeedback auf unbestimmte Zeit verschiebt.

Der [Baseline-Guard](../../../../tools/baseline_guard.py) und die zugehörigen Schemata helfen beim Erkennen formaler Lücken. Ein Schema kann prüfen, ob ein Feld vorhanden ist. Es kann nicht allein nachweisen, dass dessen Wert wahr oder mit der Kundenabsicht konsistent ist. Deshalb gehören Quellenprüfung und späterer Frischkontext-Test dazu.

## 6. Adoption als überprüfbare Zustandsänderung

Adoption bedeutet, die zuvor rekonstruierten und bestätigten Fakten in eine konsistente Steuerungsebene zu überführen. Dies ist etwas anderes als die Installation von .agentic-sdlc/. Bei der Adoption werden unter anderem gültige Anforderungen, Product State, technische Baseline, Zuständigkeiten, Quellstand und gegebenenfalls ein Lieferplan miteinander verbunden.

Eine verantwortliche Adoption benutzt eine nachvollziehbare Spezifikation und einen Preflight. Der Preflight erkennt Konflikte zwischen erwarteten und tatsächlich vorhandenen Dateien, IDs, Zuständen und Referenzen. Erst wenn die Voraussetzungen passen, darf die Übernahme der Daten erfolgen. Weder ein grüner JSON-Schema-Test noch die Existenz einer Datei mit CURRENT im Namen reicht allein als Nachweis.

Die Werkzeuge [discover_project.py](../../../../tools/discover_project.py), [apply_adoption.py](../../../../tools/apply_adoption.py) und [reconstruct_context.py](../../../../tools/reconstruct_context.py) repräsentieren verschiedene Phasen. Discovery beobachtet. Adoption schreibt nach Freigabe und Preflight. Reconstruction versucht, den aktuellen Sinn wiederherzustellen. Vertauschen Sie diese Schritte nicht und verwenden Sie die tatsächlichen, dokumentierten Parameter des installierten Starters.

Erscheint nach einer Adoption ein Widerspruch, wird die betroffene materielle Ausführung angehalten. Der zuständige technische Bearbeiter untersucht den exakten Grund: eine veraltete SHA, fehlende Datenbankmigration, widersprüchliche Rollen, nicht mehr gültige Anforderung oder fehlerhafte Referenz. Unabhängige lesende Analyse darf weiterlaufen. Man sollte nicht einen zweiten, konkurrierenden Product State erzeugen, nur um die Meldung verschwinden zu lassen.

## 7. Der Test mit einem neuen Kontext

Die wichtigste Prüfung ist ein echter Kontextwechsel. Eine Person oder ein Agent, die oder der die bisherigen Gespräche nicht kennt, liest die vorgesehenen Repository-Oberflächen und beantwortet:

- Welches Produkt soll für wen entstehen?
- Welche Anforderungen hat der CLIENT ausdrücklich bestätigt?
- Welche Version des Codes und welche relevante Datenbank sind aktuell?
- Welche technische Grundlage gilt?
- Wer darf die nächste Entscheidung treffen?
- Welche Kampagne ist gültig und was genau erlaubt sie?
- Welche Fähigkeit wurde nachgewiesen und welche Gates bleiben offen?
- Welche Handlung ist als nächste erlaubt, und welche wäre unzulässig?

Wenn diese Fragen nur beantwortet werden können, indem der ursprüngliche Auftraggeber eine Stunde lang den Chatverlauf nacherzählt, ist die Übernahme noch nicht gelungen. Der Fehler kann eine fehlende Quelle, eine widersprüchliche Referenz oder eine zu verstreute Dokumentation sein. Beheben Sie das ursächlich; ein neuer zusammenfassender Chattext ohne Quellenbindung genügt nicht.

Ein Frischkontext-Test muss auch negatives Wissen erhalten. „Der Zahlungsdienst ist noch nicht autorisiert“, „Die Datenbank ist möglicherweise älter als der Code“ oder „Die Oberfläche wurde noch nicht von einem echten Nutzer geprüft“ sind wertvolle Zustandsinformationen. Sie verhindern, dass ein späterer Bearbeiter aus Schweigen falsche Freigaben ableitet.

## 8. Den ersten Entwicklungsauftrag abgrenzen

Erst nach bestätigter Produktgrundlage und nachvollziehbarer Adoption wird ein materieller Entwicklungsauftrag entworfen. Der Planner betrachtet das Gesamtsystem, die Hauptabhängigkeiten, relevante Daten, Fehlerfolgen, Ressourcen und Akzeptanz. Er führt eine strategische Hauptprüfung und eine gesonderte adversariale Prüfung durch, wenn die Arbeit einen entsprechenden Charter benötigt.

Der Charter beschreibt die gewünschte Fähigkeit, ihre Grenzen, Zuständigkeit, Schnittstellen, Abnahmekriterien und Bedingungen, unter denen die Vereinbarung ungültig wird. Er ist kein minutiöser Stundenplan für jede Codezeile. Nach der Autorisierung übernimmt I3 die tatsächliche Zerlegung, Implementierung, Fehlersuche, Integration und technische Prüfung.

Angenommen, die erste Fähigkeit lautet „Neue Mitglieder mit Pflichtfeldprüfung registrieren und später wiederfinden“. Dazu gehören nicht nur ein Formular und ein grüner Unit-Test. Auch Speicherung, doppelte Einträge, Berechtigungen, Fehlerverhalten und die tatsächliche Bedienbarkeit müssen nach dem vereinbarten Umfang betrachtet werden. Die konkrete technische Aufgabenteilung bleibt bei I3.

Ein fehlgeschlagener Regressionstest führt zur Korrektur innerhalb derselben Kampagne. Eine neue CLIENT-Anforderung wie „Mitglieder müssen sich nun selbst im Internet registrieren“ verändert dagegen möglicherweise Sicherheitsmodell und Scope. Dann wird die strategische Autorität erneut benötigt. Diese Unterscheidung verhindert gleichzeitig unkontrollierte Scope-Ausweitung und endlose Planungsrunden.

## 9. Ein tatsächliches Erstgespräch

Der CLIENT erklärt: „Ich brauche eine kleine Verwaltungssoftware für unseren Sportverein. Sie soll Mitglieder, Beiträge und Aktivitäten auf einem lokalen Rechner verwalten. Die erste Version muss einfach sein; Geld für Onlineanbieter ist nicht vorgesehen.“

Der Planner antwortet zunächst mit einer Rückspiegelung der beabsichtigten Nutzerreise. Er fragt, wer Einträge bearbeiten darf, was bei Deaktivierung passiert, ob Beitragshistorie unverändert bleiben muss und welche Frist den größten Nutzwert bestimmt. Er prüft unabhängig vom Gespräch, welche Dateien und Datenstrukturen im Repository existieren.

Danach legt er eine kompakte Anforderungstabelle und eine technische Ausgangsbeschreibung vor. Der CLIENT bestätigt den fachlichen Teil und korrigiert gegebenenfalls die offenen Punkte. Die technische Rolle entscheidet, wie die Daten verlässlich gespeichert, getestet und gesichert werden. Der Planner ordnet die ersten lieferbaren Fähigkeiten und legt eine nachvollziehbare Baseline an.

Eine neue Sitzung wird anschließend gebeten, dieselbe Ausgangslage aus dem Repository zu rekonstruieren. Nur wenn die wesentlichen Aussagen ohne alte Chatnachrichten reproduzierbar sind, ist die gewünschte Kontinuität belegt. Der erste Charter kann dann so formuliert werden, dass ein Implementierungsteam ihn tatsächlich ausführen und prüfen kann.

## 10. Häufige Fehler und Abnahme des Baselines

Ein typischer Fehler ist es, den Kunden durch technische Rückfragen zum inoffiziellen Architekten zu machen. Ein anderer ist, fehlende fachliche Entscheidungen durch vermeintlich sinnvolle Defaults zu ersetzen. Beides verschiebt Verantwortung falsch. Ein dritter Fehler ist eine zu große Anfangsplanung, die zwar umfangreiche Dokumente erzeugt, aber keine überschaubare erste Fähigkeit sichtbar macht.

Die Baseline ist ausreichend, wenn die Produktabsicht bestätigt, die technische Ausgangslage physisch verifiziert, die Zuständigkeiten klar und die nächste zulässige Aktion rekonstruierbar ist. Nicht jede denkbare künftige Entscheidung muss im Voraus getroffen werden. Materiale Unsicherheit wird gekennzeichnet und dort behandelt, wo sie tatsächlich eine Handlung beeinflusst.

Prüfen Sie abschließend gegen die [Kernregeln des Planners](../../../../protocols/PLANNER_KERNEL.md), den [Adoptionsvertrag](../../../16_TRANSFER_ADOPTION.md) und das [Autoritätsmodell](../../../../protocols/AUTHORITY_MODEL.md). Diese Quellen helfen, produktive Eigenständigkeit und reservierte Entscheidungen sauber auseinanderzuhalten.

**Weiter:** Kapitel 03, täglicher Betrieb.

## Quellen und Gültigkeit

- [Produktentdeckung und technische Baseline](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Übernahme/Adoption](../../../16_TRANSFER_ADOPTION.md)
- [Planner-Kernel](../../../../protocols/PLANNER_KERNEL.md)
- [Produktentdeckungsgespräch](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md)
- [Discover-Tool](../../../../tools/discover_project.py)
- [Adoptionswerkzeug](../../../../tools/apply_adoption.py)
- [Frischkontextrekonstruktion](../../../../tools/reconstruct_context.py)

Die dargestellten Vereinsanforderungen sind Vorschläge für ein fiktives Beispiel, keine bestätigte Realität eines fremden Produkts.
