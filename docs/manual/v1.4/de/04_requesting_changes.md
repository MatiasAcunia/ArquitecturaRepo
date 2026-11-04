# 04 — Produktänderungen richtig anfordern

ArquitecturaRepo · Vollständiges Benutzerhandbuch · Ausgabe v1.4 · Deutsch

> Der Auftraggeber soll eine gewünschte Wirkung beschreiben können, ohne die technische Umsetzung selbst zu verwalten. Dieses Kapitel zeigt, wie Änderungen klar, überprüfbar und mit nachvollziehbarer Priorität formuliert werden. Verbindliche Grenzen stehen im [CLIENT-Boundary-Protokoll](../../../../protocols/CLIENT_BOUNDARY.md) und im [Anforderungsprozess](../../../../protocols/PRODUCT_DISCOVERY_REQUIREMENTS_AND_TECHNICAL_BASELINE.md).

## Kapitelübersicht

1. Mit dem Ergebnis beginnen
2. Ein kompakter Änderungsauftrag
3. Welche Entscheidungen beim CLIENT bleiben
4. Änderungen der Meinung ohne Geschichtsverlust
5. Qualitätswünsche ohne Technikvorgabe
6. Prioritäten setzen und den Umfang begrenzen
7. Wann der Planner wirklich zurückfragen muss
8. Fünf gut formulierte Beispiele
9. Neue Produktabsicht oder gewöhnlicher Fehler?
10. Wenn Software funktioniert, aber nichts nützt
11. Eine praktische Gesprächsvorlage

## 1. Mit dem Ergebnis beginnen

Viele Softwareänderungen werden als technische Anweisungen formuliert: „Baue einen REST-Endpunkt“, „füge einen Index hinzu“ oder „nutze eine andere Datenbank“. Solche Aussagen können richtig sein, wenn der Auftraggeber selbst eine technische Randbedingung setzen will. In gewöhnlicher Produktarbeit sind sie aber oft nur Vermutungen über die eigentliche Lösung.

Beginnen Sie besser mit dem Problem und dem beobachtbaren Ergebnis. Statt „Erstelle einen Cache für Mitglieder“ könnten Sie sagen: „Die Verwaltungskraft muss ein Mitglied bei rund zehntausend Einträgen schnell finden können, ohne die gleiche Suche mehrfach zu starten.“ Die technische Rolle untersucht dann, ob ein Index, eine Datenbankabfrage, eine andere Oberfläche oder eine Kombination den gewünschten Effekt zuverlässig erreicht.

Das vermeidet zwei Fehler. Erstens kann ein vorschnell vorgeschriebener Lösungsweg die falsche Ursache behandeln. Zweitens lädt er den CLIENT mit technischer Verantwortung auf, die er weder übernehmen muss noch übernehmen sollte. Der Auftraggeber behält trotzdem die Kontrolle über Qualität, Budget, Zeitplan und den sichtbaren Erfolg.

Ein guter Änderungswunsch beschreibt mindestens: Wer möchte was erreichen? Welcher konkrete Ablauf funktioniert heute nicht oder soll sich verbessern? Woran erkennt die Person die neue Fähigkeit? Welche bestehenden Regeln dürfen nicht verletzt werden? Gibt es eine harte Frist, Kostenobergrenze oder externe Freigabe?

## 2. Ein kompakter Änderungsauftrag

Für alltägliche Wünsche reicht häufig ein kurzer Text. Eine mögliche Vorlage:

> Als Verwaltungsmitarbeiterin möchte ich Beiträge eines Mitglieds nach Zeitraum filtern und die Summe sehen. Der Filter muss bei leeren Ergebnissen verständlich reagieren und darf keine Zahlungen verändern. Die erste Version braucht keinen Export. Wichtig ist die korrekte Summe vor einer aufwendigen Gestaltung.

Diese Formulierung ist verständlich, abgrenzbar und testbar. Sie legt weder die SQL-Abfrage noch die Klassenaufteilung fest. Der Planner kann daraus die notwendigen Schnittstellen und Abnahmekriterien ableiten. Die technische Umsetzung bleibt bei I3.

Für eine größere Änderung ergänzen Sie Daten- und Betriebsfolgen: Gibt es personenbezogene Daten? Sind Nutzerrechte betroffen? Werden bestehende Aufzeichnungen umgeschrieben? Muss das Produkt offline funktionieren? Sollen Dritte eine Nachricht erhalten? Ein abgrenzbarer Änderungsauftrag muss solche Risiken früh sichtbar machen.

Unbekannte Entscheidungen dürfen ausdrücklich offen bleiben. Beispielsweise kann der CLIENT sagen: „Ich weiß noch nicht, ob ehemalige Mitglieder im Suchergebnis erscheinen sollen. Prüft die Auswirkungen und fragt mich, bevor ihr die Regel festlegt.“ Das ist eine ehrliche Arbeitsgrundlage. Eine stillschweigende technische Annahme wäre dagegen eine unautorisierte Produktentscheidung.

## 3. Welche Entscheidungen beim CLIENT bleiben

Der CLIENT entscheidet über Zweck, Zielgruppe, Prioritäten und sichtbares Verhalten. Er darf eine Gestaltung ablehnen, auch wenn sie technisch korrekt ist. Er entscheidet über das gewünschte Nutzererlebnis und die zulässigen externen Handlungen, soweit sie ihm vorbehalten sind. Technische Rollen dürfen erklären, dass eine bestimmte Kombination von Anforderungen teuer, riskant oder unvereinbar ist, aber die Produktabsicht nicht heimlich austauschen.

Die technische Umsetzung entscheidet dagegen normalerweise, wie ein Datenmodell strukturiert, eine Schnittstelle aufgebaut, ein Fehler behandelt oder ein Test organisiert wird. Der Planner verantwortet die technische Strategie und der Controller die operativen Details. Wenn eine technische Wahl den Budgetrahmen oder die Benutzererfahrung stark beeinflusst, werden ihre Folgen erklärt und gegebenenfalls eine neue Produktentscheidung eingeholt.

Ein Beispiel: Der CLIENT möchte eine Sicherung seiner Vereinsdaten. Er muss erklären, wie viel Datenverlust noch akzeptabel wäre und ob externe Speicherung erlaubt ist. Engineering bestimmt anschließend die konkrete Backuptechnik, die Fehlererkennung und den Wiederherstellungstest. Es wäre verkehrt, den CLIENT nach dem passenden Dateisystem-Flush oder Transaktionsisolationsgrad zu fragen.

Eine andere Grenze sind rechtliche und externe Entscheidungen. Dass ein Agent eine Veröffentlichung technisch ausführen könnte, ersetzt nicht die erforderliche Freigabe. Besonders bei Mitgliederdaten, Bildern Dritter, Zahlungsdiensten und produktiven Änderungen muss klar sein, welche Handlung erlaubt ist und wer sie genehmigt hat.

## 4. Änderungen der Meinung ohne Geschichtsverlust

Produktentwicklung ist ein Lernprozess. Eine früher bestätigte Anforderung darf später geändert werden. Vielleicht war die Vereinsanwendung zunächst nur lokal geplant, und nach einer erfolgreichen Testphase möchte der CLIENT doch mehrere Standorte anbinden. Die neue Entscheidung ist zulässig, aber sie verändert möglicherweise Netzwerk, Zugriffsrechte und Sicherheitsstrategie.

Die neue Anforderung muss mit ihrer Herkunft und ihrem Zeitpunkt zum aktuellen Zustand erhoben werden. Die frühere Entscheidung kann als historische Begründung erhalten bleiben, darf aber nicht mehr als gleichrangige aktuelle Autorität gelten. Der technische Planner beurteilt die Auswirkungen auf Code, Daten, laufende Kampagnen und geplante Lieferungen.

Ein nicht mehr passender Charter muss nicht durch heimliche Scope-Erweiterung gerettet werden. Wenn die Änderung die ursprünglich erlaubte Fähigkeit wesentlich umdefiniert, wird die entsprechende strategische Entscheidung neu getroffen. Betrifft sie nur eine kleine, bereits erlaubte Korrektur, kann I3 die Arbeit ohne neue Kampagne fortsetzen.

Vermeiden Sie das reflexartige Löschen alter Dokumente. Mit einer nachvollziehbaren Supersession lässt sich später verstehen, weshalb eine technische Entscheidung damals richtig war und heute nicht mehr gilt. Genau diese Herkunft schützt das Projekt vor scheinbaren Widersprüchen zwischen Chatverlauf und Repository.

## 5. Qualitätswünsche ohne Technikvorgabe

Qualität ist nicht auf Unit-Tests begrenzt. Ein Formular kann alle Eingaben korrekt speichern und trotzdem so unübersichtlich sein, dass der Nutzer im Alltag Fehler macht. Der CLIENT darf daher konkrete Wahrnehmungs- und Bedienungsziele nennen: lesbar, schnell erfassbar, klar bei Fehlern, konsistent mit dem übrigen Produkt oder nutzbar auf einem bestimmten Bildschirm.

Für die Vereinsverwaltung könnte der Wunsch lauten: „Neue Mitglieder sollen ohne Anleitung in höchstens wenigen verständlichen Schritten angelegt werden können. Pflichtfelder müssen erkennbar sein. Bei einer doppelten Person soll das System vor dem Anlegen warnen.“ Diese Aussage lässt mehrere technische Entwürfe offen, macht aber das gewünschte Erlebnis prüfbar.

Technische Qualität wird ebenfalls beschrieben, nur von anderen Eigentümern. Dazu gehören Fehlerbehandlung, Tests, Datenintegrität, Sicherheitskontrollen, Wiederherstellung und Wartbarkeit. Die konkrete Gewichtung muss zu den realen Risiken passen. Eine gefährliche Migration braucht andere Nachweise als eine rein kosmetische Farbänderung.

Fragen Sie nach einer sichtbaren Demonstration, wenn die Oberflächenqualität im Mittelpunkt steht. Ein Screenshot zeigt einen Zustand, aber nicht unbedingt den Ablauf. Eine kurze Aufnahme oder ein tatsächlich bedienbarer Kandidat kann mehr belegen. Sichern Sie den konkreten Kandidaten, damit spätere Veränderungen nicht unbemerkt mit dem geprüften Stand verwechselt werden.

## 6. Prioritäten setzen und den Umfang begrenzen

Ein häufiger Fehler ist, zehn neue Wünsche gleichzeitig als unabhängig dringende Goals zu behandeln. Das erschwert die Planung und erzeugt unklare Schnittstellen. Stellen Sie zuerst fest, welche Änderungen von anderen abhängen und welche zusammen eine für den Nutzer brauchbare Fähigkeit ergeben.

Nehmen wir an, der Verein wünscht neue Mitgliedskategorien, E-Mail-Erinnerungen, Beitragsberichte und eine hübschere Startseite. Wenn Beitragsberichte die Mitgliedskategorien benötigen, ist die Reihenfolge relevant. E-Mail-Erinnerungen können externe Datenschutz- und Versandfreigaben erfordern. Die Startseite kann hingegen getrennt verbessert werden, solange sie keine gemeinsame technische Ressource blockiert.

Eine hilfreiche Prioritätseinteilung ist: notwendig für den ersten echten Nutzerablauf, wichtig für Sicherheit und Korrektheit, unmittelbar wertvoll aber verschiebbar, später oder ausdrücklich außerhalb des Umfangs. Der CLIENT bestimmt den Nutzwert; Engineering legt Abhängigkeiten und sichere Reihenfolge dar.

Eine angemessene erste Version soll früh genug nutzbar sein, um echte Rückmeldungen zu erzeugen. Das bedeutet nicht, Tests oder Datenschutz zu ignorieren. Es bedeutet, die Grenze so zu ziehen, dass innerhalb dieses Bereichs eine ehrliche, vollständig überprüfte Fähigkeit entsteht und nicht bloß ein großes Versprechen.

## 7. Wann der Planner wirklich zurückfragen muss

Eine Rückfrage ist nötig, wenn eine ungeklärte Produktentscheidung das Ergebnis materiell verändert. Das gilt beispielsweise für die Löschung historischer Zahlungen, die Freigabe einer öffentlichen Benutzerregistrierung oder den Versand echter Mahnungen. Sie kann auch nötig sein, wenn zwei bestätigte Wünsche unvereinbar sind.

Eine Rückfrage ist normalerweise nicht nötig, weil ein Unit-Test fehlschlägt, eine Abhängigkeit aktualisiert werden muss oder der Controller eine interne Klasse anders aufteilen will. Diese Angelegenheiten gehören in die technische Verantwortung, sofern keine neue wesentliche Gefahr oder Produktfolge entsteht.

Formulieren Sie die Frage mit Konsequenzen. Statt „Soll ich Option A oder B wählen?“ ist besser: „Wenn deaktivierte Mitglieder verborgen werden, sieht die Verwaltung frühere Zahlungen nur über den Archivfilter. Wenn sie sichtbar bleiben, ist die Liste länger, aber der Verlauf leichter auffindbar. Welche Arbeitsweise entspricht Ihrem Verein?“

So muss der CLIENT nicht die ganze Architektur verstehen. Er kann die tatsächliche Nutzerentscheidung treffen. Die technische Rolle übernimmt anschließend ihre Übersetzung in Implementierung und Tests.

## 8. Fünf gut formulierte Beispiele

**Beispiel 1 — Suche:** „Eine Mitarbeiterin soll Mitglieder nach Namen oder Nummer suchen können. Deaktivierte Personen müssen auf Wunsch mit angezeigt werden. Die Suche darf keine Datensätze verändern.“ Dies legt Zweck und Grenzen fest, nicht den Index.

**Beispiel 2 — Beiträge:** „Beim Erfassen einer Beitragszahlung muss die Person, der Betrag und das Datum sichtbar sein. Ein versehentlicher Doppelklick darf nicht zwei Zahlungen anlegen.“ Hier folgt aus der Nutzerabsicht eine wichtige technische Idempotenzanforderung.

**Beispiel 3 — Deaktivierung:** „Eine deaktivierte Person darf keine neuen Aktivitäten buchen. Frühere Buchungen und Zahlungen bleiben nachvollziehbar.“ Der Planner muss auf mögliche Konflikte zu bestehenden Datenschutz- oder Aufbewahrungsregeln achten.

**Beispiel 4 — Export:** „Der Vorstand benötigt monatlich eine Zusammenfassung ohne persönliche Kontaktadressen. Der Export soll nur durch berechtigte Personen möglich sein.“ Der Wunsch enthält zugleich eine Sicherheitsgrenze.

**Beispiel 5 — Oberfläche:** „Die wichtigsten täglichen Aktionen sollen ohne Fachbegriffe erkennbar sein. Fehlermeldungen müssen erklären, was der Nutzer korrigieren kann.“ Das ist eine Qualitätserwartung, keine CSS-Anweisung.

Zu jedem Beispiel kann Engineering realistische Abnahmekriterien ausarbeiten. Dazu gehören positive Abläufe, Grenzfälle, Auswirkungen auf vorhandene Daten und die passenden getrennten Gates. Der CLIENT muss nicht die Testautomatisierung selbst programmieren.

## 9. Neue Produktabsicht oder gewöhnlicher Fehler?

Die Unterscheidung ist einfach, aber folgenreich. Ein Fehler liegt vor, wenn das bestehende bestätigte Verhalten falsch umgesetzt wurde. Ein neuer Wunsch verändert dieses Verhalten oder erweitert seinen Geltungsbereich. Im ersten Fall sollte I3 innerhalb der bereits autorisierten Arbeit korrigieren. Im zweiten Fall kann eine neue Entscheidung nötig sein.

Beispiel Fehler: Eine Suche soll laut bestätigtem Charter auch Umlaute finden, tut es aber nicht. Die Implementierung muss repariert werden. Beispiel neue Produktabsicht: Die Suche soll nun zusätzlich externe Vereinsdatenbanken abfragen. Das bringt neue Berechtigungen, Schnittstellen und möglicherweise Datenschutzfolgen mit sich.

Ein wiederkehrender Fehler wird nicht allein durch häufiges Auftreten strategisch. Er kann auf eine systemische technische Ursache hinweisen, die I3 mit umfassendem Hardening und unabhängiger Prüfung behandelt. Erst eine wirkliche Veränderung der zulässigen Grenzen oder eine neue wesentliche Gefahr führt zu einer strategischen Neubeurteilung.

Verantwortlichkeiten dürfen nicht durch Berichtsformate verschwimmen. Wenn der Controller sagt „Ich brauche eine neue Kampagne, weil der Reviewer zwei Defekte gefunden hat“, fragen Sie zunächst, ob die Defekte bereits durch den aktuellen Charter abgedeckt waren. Ist dies der Fall, bleibt ihre Korrektur Teil der laufenden Arbeit.

## 10. Wenn Software funktioniert, aber nichts nützt

Es ist möglich, dass alle technischen Tests grün sind und der CLIENT das Ergebnis dennoch ablehnt. Vielleicht erfordert eine häufige Aktion zu viele Schritte. Vielleicht verwendet die Oberfläche unverständliche Begriffe. Vielleicht ist die Auswertung zwar mathematisch korrekt, beantwortet aber nicht die Frage, die der Vorstand wirklich stellt.

Formulieren Sie eine solche Ablehnung konkret: „Ich kann den Beitragsstand eines Mitglieds finden, aber ich brauche zuerst einen schnellen Überblick über alle überfälligen Beiträge. Die aktuelle Oberfläche hilft bei meiner Hauptaufgabe noch nicht.“ Damit bleibt der fachliche Fortschritt sichtbar und der tatsächliche Mangel wird verständlich.

Anschließend unterscheidet der Planner, ob das ursprünglich vereinbarte Ergebnis nicht erfüllt wurde oder ob eine neue Präferenz hinzugekommen ist. Daraus ergibt sich die richtige Route. Für eine bereits vereinbarte, aber unzureichend umgesetzte Qualität ist meist Nacharbeit innerhalb des bestehenden Auftrags zuständig.

Eine freundliche Bewertung ist keine Pflicht. Die human-perceptual-Prüfung soll tatsächlich feststellen, ob die Software ihren Zweck erfüllt. Das ist besonders wichtig, wenn ein KI-Werkzeug die Umsetzung sehr schnell, aber ohne reale Nutzerinteraktion erzeugt hat.

## 11. Eine praktische Gesprächsvorlage

Sie können die folgenden fünf Fragen in einer kurzen Besprechung beantworten:

1. Welcher Nutzer erlebt heute welches Problem?
2. Was soll er nach der Änderung konkret besser tun können?
3. Welche bestehenden Daten, Rechte und Abläufe müssen unverändert bleiben?
4. Welcher Termin, welche Kosten oder welches Qualitätsmerkmal sind vorrangig?
5. Welche offene Produktentscheidung würde die Umsetzung grundsätzlich verändern?

Danach soll Engineering den aktuellen Code prüfen, die Folgen erklären, die richtige Fähigkeit abgrenzen und die technischen Risiken behandeln. Nicht jeder Wunsch benötigt ein großes Dokument. Wichtig ist, dass die gültige Entscheidung an der kanonischen Stelle nachvollziehbar wird und sich auf eine reale Abnahme beziehen lässt.

Der beste Änderungsauftrag spart beiden Seiten Arbeit: Der CLIENT beschreibt den gewünschten Nutzen; die technische Rolle verantwortet die Umsetzung und kann begründet zurückfragen, falls das Produkt sonst anders würde als beabsichtigt. Diese Arbeitsteilung ist Kern von ArquitecturaRepo.

**Weiter:** Kapitel 05, Fehler und Wiederherstellung.

## Quellen und Gültigkeit

- [CLIENT-Grenze](../../../../protocols/CLIENT_BOUNDARY.md)
- [Produktentdeckung und technische Baseline](../../../../protocols/PRODUCT_DISCOVERY_REQUIREMENTS_AND_TECHNICAL_BASELINE.md)
- [Planner-Kernel](../../../../protocols/PLANNER_KERNEL.md)
- [Anforderungen und Lieferplan](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Charter-Standard](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Abnahme von Fähigkeiten](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)

Die vorgeschlagenen Wünsche betreffen das fiktive Vereinsbeispiel. Sie sind keine bereits bestätigten Anforderungen für eine fremde Installation.
