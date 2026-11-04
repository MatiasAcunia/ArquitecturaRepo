# 07 — Exemple guidé : une application de gestion pour un club

ArquitecturaRepo · Manuel d'utilisation complet · Édition v1.4 · Français

> Cet exemple est **fictif et pédagogique**. Il ne décrit pas une application déjà développée, un backend généré automatiquement ou une preuve qu'un modèle d'IA a livré un CRUD accepté. Dans un projet réel, les exigences, les sources, la DB, les permissions et les preuves doivent provenir du produit adopté.

## Dans ce chapitre

1. Le produit demandé par le club
2. Découvrir les questions qui changent le résultat
3. Installer la couche de contrôle, pas l'application
4. Première capacité : gestion des membres
5. Du Planner à I3 : un ordre de travail complet
6. Ce qu'il faut tester avant d'accepter
7. Deuxième capacité : cotisations et paiements
8. Évaluer l'ensemble du parcours
9. Premier cycle avec des données fictives
10. Enregistrer et acheminer un défaut
11. Les dépendances du deuxième cycle
12. Exercice final : récupérer le projet

## 1. Le produit demandé par le club

Imaginez une petite association locale. Une personne administrative gère les membres, cotisations, activités et inscriptions dans plusieurs feuilles de calcul. La nouvelle application doit permettre de retrouver une fiche, savoir qui a payé, conserver les opérations historiques et ne pas accepter plus d'inscriptions que la capacité d'une activité.

La première version sera utilisée en interne. Le CLIENT décide de ne pas ajouter pour l'instant de paiement en ligne, d'application mobile séparée, de facturation réglementaire, de notifications automatiques ou d'intégrations complexes. Cela limite les risques et permet de vérifier rapidement les comportements essentiels.

Cette description ne fixe pas encore le langage, la DB, le serveur ou les permissions exactes. Le Planner confirme l'usage réel et les règles de produit. L'ingénierie choisit une solution proportionnée en tenant compte du code existant, de la sécurité, du coût et de la maintenance. Installer le framework n'implémente aucune de ces fonctionnalités.

Un ordre de capacités plausible est identité des membres, cotisations, activités et inscriptions. Les cotisations dépendent d'une identité stable ; les inscriptions fondées sur le statut financier dépendent de cotisations correctes. Cet ordre protège les interfaces et évite de programmer des règles de métier contradictoires.

Il ne faut pas confondre ces dépendances avec la nécessité de multiplier les agents. Un Planner peut conserver la stratégie pendant qu'un Controller prend en charge l'ingénierie. Des spécialistes sont utiles lorsqu'il existe un travail réellement séparable ou une revue indépendante pertinente.

## 2. Découvrir les questions qui changent le résultat

Le Planner demande : qui utilisera le logiciel, combien de membres existent, l'application doit-elle fonctionner sans internet, quelles données personnelles sont nécessaires, comment les sauvegardes seront-elles réalisées et quand la première version doit-elle être démontrée ? Les réponses peuvent modifier le stack, les interfaces et le plan.

Une règle proposée est : «Un administrateur peut désactiver un membre, mais les paiements antérieurs doivent rester disponibles aux personnes autorisées». Cette règle doit être confirmée. La désactivation est-elle réversible ? Le membre doit-il disparaître de toutes les recherches ou seulement du filtre des actifs ? Quelles données doivent rester visibles ?

Autres points : une cotisation en retard empêche-t-elle une inscription ? Les paiements partiels comptent-ils ? Une annulation libère-t-elle immédiatement une place ? Une liste d'attente existe-t-elle ? Peut-on corriger un paiement et qui en a le droit ? Le Planner ne transforme pas des suppositions en règles actuelles pour avancer plus vite.

| Domaine | Premier comportement proposé |
| --- | --- |
| Membres | Créer, modifier, rechercher, désactiver et conserver l'historique. |
| Cotisations | Enregistrer les paiements, identifier les retards et consulter les opérations. |
| Activités | Définir nom, horaire, capacité et places disponibles. |
| Inscriptions | Ajouter/annuler selon la capacité et les règles de cotisation. |
| Hors périmètre | Paiements en ligne, app mobile, notifications massives, tableaux de bord complexes. |

La table reste une proposition tant que le CLIENT ne l'a pas confirmée. Le besoin de données durables suggère un profil `STATEFUL`, mais cela n'établit pas une politique de confidentialité, un schéma ou une permission de production. Ces éléments sont reconstruits dans l'adoption réelle.

## 3. Installer la couche de contrôle, pas l'application

Dans un dépôt nouveau et non gouverné, le starter v1.4 peut créer une couche `.agentic-sdlc/`. Depuis la racine du framework, le PowerShell suivant est un exemple :

```powershell
& "python" "tools\scaffold_project.py" --target "..\club-app" --profile "STATEFUL" --product-id "CLUB_GESTION" --objective "Gestion fictive des membres et cotisations" --language "fr" --no-feedback-workflow
```

Le résultat initial est `HOLD / UNTRUSTED_CONTEXT`. L'installateur ne crée pas automatiquement une interface ou une DB, ne configure pas d'LLM et n'autorise pas de campagne. Le [chapitre 01](01_installation.md) explique les commandes de diagnostic et les limites de ce scaffold.

Si le dépôt `club-app/` contient déjà un Product State ou un contrôleur canonique, ne réinstallez pas le starter par-dessus. Utilisez le [précontrôle en lecture seule](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) pour reconstruire les références et préparer une éventuelle adoption sans écraser l'autorité existante.

Le Planner et I3 inspectent ensuite les sources, l'inventaire, les données, les exigences et l'environnement. Ils préparent une spécification d'adoption, passent les contrôles de preflight, établissent des références cohérentes et démontrent que le contexte peut être récupéré par une nouvelle session.

Le CLIENT confirme les priorités, contraintes et choix fonctionnels. L'ingénierie propose le stack, les sauvegardes, les accès et les jalons datés. Une campagne matérielle ne devient autorisée qu'après adoption suffisante et charter explicite. Si la source de vérité est inconnue, un HOLD ciblé protège le travail dépendant.

## 4. Première capacité : gestion des membres

Les paiements et inscriptions ont besoin d'un identifiant de membre fiable. Commencer par les membres est donc une décision de dépendance produit, non une préférence pour une technologie. Un charter pourrait demander :

> Un administrateur autorisé peut créer une fiche, la rechercher, la modifier et la désactiver, sans détruire les paiements et inscriptions historiques qui doivent être conservés.

Le charter définit interfaces, données, propriété, erreurs attendues et gates. Il ne demande pas au CLIENT de concevoir le schéma SQL ou les noms des classes. I3 choisit l'implémentation, gère les tests, les corrections et les revues dans la portée autorisée.

Les contrôles peuvent inclure identifiants en double, données invalides, lecture après écriture, persistance après redémarrage, recherche actifs/inactifs, relations historiques et accès non autorisé. Si l'application possède une interface, le parcours utilisateur complet doit être exercé sur le candidat intégré réel.

Une capture de la fiche créée ne prouve pas que l'enregistrement est durable. Un test de validation des champs ne prouve pas que la personne peut retrouver la fiche. Les gates unitaires, d'intégration, de DB, physiques et perceptuels répondent à des questions différentes.

Si des données réelles existent déjà, l'ingénierie doit préserver l'état actuel et prévoir sauvegarde, migration et rollback adaptés. Les données fictives du manuel ne représentent pas la base de l'association et ne doivent jamais être présentées comme preuves d'une adoption réelle.

## 5. Du Planner à I3 : un ordre de travail complet

Un message de campagne peut rester concis tout en donnant les références nécessaires. Dans une véritable exécution, il faudrait remplacer cet exemple par les sources et IDs actuels :

> **Goal:** Livrer la capacité de gestion des membres dans le charter autorisé.
>
> **Context:** Reconstruire les exigences confirmées, le Product State, le dépôt, le commit et la DB actuelle.
>
> **Constraints:** Conserver l'historique et les permissions ; ne pas développer cotisations, notifications ou fonctions hors périmètre.
>
> **Execution gates:** Tester réellement création, recherche, édition, désactivation et persistance après redémarrage ; traiter les entrées invalides, les doublons et les accès interdits. Faire une revue indépendante du candidat intégré.
>
> **Done when:** Fournir l'identité exacte du candidat, preuves physiques, résultats des contrôles, rapport de revue, gates ouverts et terminal stratégique honnête.

I3 peut diviser le travail en tâches, résoudre des bugs, modifier la structure interne, relancer les tests et intégrer un nouveau candidat sans demander un charter à chaque étape. Si le double clic sur «enregistrer» crée deux fiches contrairement à une règle d'unicité, c'est un défaut à réparer dans cette campagne.

Lorsque des actions ont un coût ou un risque matériel, le Controller définit un inventaire, une méthode, des limites et des conditions d'arrêt pour l'unité de travail. Cela ne l'autorise pas à utiliser un fournisseur payant ou à introduire une fonctionnalité externe non demandée.

## 6. Ce qu'il faut tester avant d'accepter

Prenons un membre synthétique `MEMBRE-001`. Le tableau décrit ce qu'une future application devrait démontrer. Ce n'est **pas** une preuve que ces tests ont déjà été exécutés :

| Étape | Action utilisateur | Résultat observable attendu |
| --- | --- | --- |
| 1 | Ouvrir le programme comme administrateur. | Le mécanisme d'accès autorise le rôle prévu. |
| 2 | Créer `MEMBRE-001` avec des champs fictifs valides. | Un seul enregistrement apparaît avec un identifiant stable. |
| 3 | Rechercher par identifiant autorisé. | La bonne fiche apparaît sans exposer des données privées. |
| 4 | Modifier un téléphone fictif. | La nouvelle valeur est visible après enregistrement et relecture. |
| 5 | Fermer puis rouvrir l'application. | Les données persistent dans le chemin réel de DB/recovery. |
| 6 | Désactiver le membre. | Il n'apparaît plus comme actif, mais son identité historique reste. |
| 7 | Consulter l'historique avec le bon rôle. | Paiements et inscriptions conservés restent disponibles. |
| 8 | Essayer une entrée invalide ou un doublon. | L'application refuse clairement sans corruption de l'état. |

Pour chaque étape, notez l'entrée, le résultat attendu, l'observation, l'environnement et le commit. Un HTTP 200 ne suffit pas à établir la persistance ; une relecture indépendante est nécessaire. Si le produit promet la durabilité après redémarrage, le test doit réellement redémarrer le processus concerné.

Si deux employés utilisent l'application simultanément, il faut tester les interactions qui peuvent entrer en concurrence. Un test séquentiel ne prouve pas que deux inscriptions simultanées respecteront le dernier siège disponible. Les cas de test dépendent des risques et de l'architecture réelle.

Utilisez des données fictives pour les captures publiques. Ne publiez pas noms, coordonnées ou paiements réels. L'évaluation perceptuelle relève d'une personne compétente sur un candidat représentatif, séparément des contrôles de sécurité et de données.

Si l'application n'a pas encore été construite, les étapes sont `NOT RUN`, pas `PASS`. Le manuel décrit une méthode pour produire des preuves ; il n'a pas exécuté les fonctionnalités de ce club fictif.

## 7. Deuxième capacité : cotisations et paiements

Une fois la gestion des membres acceptée, le CLIENT demande l'enregistrement des cotisations. Le Planner confirme périodes, échéances, paiements partiels, corrections, rôles et doublons. Un statut «à jour» doit provenir de règles et de données cohérentes, pas d'un calcul improvisé dans chaque écran.

Une politique possible est : «Un paiement saisi par erreur est annulé par une écriture d'audit ; la transaction originale n'est pas effacée». Le CLIENT décide de cette règle. Le Planner l'enregistre ; I3 implémente persistance, validation, idempotence, contrôle des permissions et récupération.

La répétition d'une requête, à cause d'une connexion instable ou d'un double clic, ne doit pas produire un deuxième paiement lorsque le contrat exige une seule opération. Les tests doivent exercer la frontière où le doublon peut réellement survenir, pas seulement une fonction isolée.

Si le produit traite de l'argent réel, les gates de confidentialité, d'autorisation, de journalisation et de publication doivent être renforcés en proportion du risque. Le starter ne contient pas de service de paiement et n'autorise pas l'usage d'un fournisseur externe. Cet exemple sert à penser les données et les preuves.

Les activités et inscriptions viennent ensuite, lorsque l'identité et le statut de cotisation sont fiables. Inutile d'ajouter spontanément microservices, cloud, application mobile ou système complexe de rôles. Chaque mécanisme supplémentaire doit répondre à un besoin ou à un risque observé.

## 8. Évaluer l'ensemble du parcours

Après cet exercice, vous devriez pouvoir distinguer les décisions du CLIENT, les exigences confirmées par le Planner, l'exécution contrôlée par I3, la revue indépendante et l'acceptation finale. Vous devriez aussi expliquer pourquoi une validation verte du framework ne signifie pas que la gestion du club est prête.

L'enjeu n'est pas de mémoriser chaque nom de JSON, mais de comprendre où se trouve la vérité actuelle, quel acteur peut la changer et quelle preuve confirme un comportement. Une architecture qui génère beaucoup de documents mais ne démontre pas l'enregistrement d'un membre n'a pas livré la première capacité.

Ces principes s'appliquent à d'autres produits : API, réservation, application éducative ou outil interne. Les gates nécessaires varient selon les données, utilisateurs et conséquences, mais la séparation entre intention, autorisation, implémentation, preuve et jugement reste pertinente.

Une comparaison avec la programmation directe dans un chat doit rester honnête. Un petit prototype peut être plus rapide en conversation libre ; un produit long peut gagner en continuité et en qualité de revue. Les bénéfices doivent être mesurés avec des travaux réels, non proclamés comme une supériorité universelle.

## 9. Premier cycle avec des données fictives

Inventez «Personne de test A» et un numéro de contact manifestement fictif. Confirmez avec le CLIENT les champs requis et l'identifiant unique. Le Planner exprime les critères de produit et l'ingénierie choisit les contraintes de stockage, transactions et gestion des erreurs.

Exécutez le parcours complet : création, liste, recherche, modification, redémarrage, relecture, désactivation et consultation de l'historique autorisé. Notez chaque résultat observé. Une capture de la première création n'est que le début de la démonstration de persistance.

Ajoutez des cas négatifs : identifiant répété, champs invalides, panne contrôlée de DB pendant l'écriture et soumission répétée. Les messages et effets exacts dépendent des règles confirmées, mais l'application ne doit pas produire silencieusement des données contradictoires.

Si plusieurs opérateurs existent, examinez les actions simultanées : deux personnes réservent la dernière place ou modifient le même enregistrement. Un test isolé ne permet pas de conclure que la concurrence est sûre. Le Controller choisit des scénarios représentatifs du risque réel.

Le CLIENT peut ensuite signaler que certains champs sont difficiles à comprendre ou que la désactivation manque d'explication. Le Planner classe le retour : défaut d'un comportement convenu ou nouvelle règle de produit. I3 corrige les problèmes couverts sans ouvrir une campagne stratégique supplémentaire.

## 10. Enregistrer et acheminer un défaut

Supposons que la désactivation de «Personne de test A» fasse disparaître les paiements historiques. Si leur conservation était exigée, c'est un bug dans la campagne courante. Notez candidat, étapes, données synthétiques, observation et gate concerné.

Le Planner renvoie les falsificateurs à I3. Le Controller recherche la cause dans les relations de persistance, corrige, ajoute une régression, exécute le readback après redémarrage, intègre un nouveau candidat et obtient une revue indépendante pertinente. Il n'ouvre pas une campagne distincte pour chaque symptôme.

Maintenant, le CLIENT demande si un membre inactif peut récupérer son ancien numéro en cas de réactivation. Si cette règle n'avait jamais été décidée, le Planner la confirme avant de l'intégrer à la stratégie. On ne peut pas appeler bogue le choix entre deux comportements qui n'avaient pas été spécifiés.

Le manuel ne doit pas fabriquer de preuve à partir de cette histoire. Tant qu'aucune application réelle n'a été développée, les tests restent `NOT RUN`. Le but est d'apprendre à identifier les autorités, données et observations nécessaires à une acceptation honnête.

## 11. Les dépendances du deuxième cycle

Les cotisations ont besoin d'un membre stable et de règles explicites sur les paiements partiels, doublons, échéances et corrections. Le Planner utilise la capacité précédente réellement acceptée comme base. I3 implémente sur les interfaces et sources actuelles, pas sur une version mémorisée d'une ancienne conversation.

Avant les inscriptions, vérifiez que le statut des cotisations est produit de manière actuelle et consommable. Si la règle d'éligibilité utilise une dette mal définie, l'API et la UI pourraient donner des résultats contradictoires. Le chemin critique sert à prévenir ces incohérences, pas à justifier davantage d'agents.

La livraison incrémentale permet au CLIENT de tester les membres avant d'investir dans les cotisations. Les retours réels peuvent faire découvrir des exigences nouvelles ; leur effet est plus facile à comprendre quand les capacités ont des interfaces et preuves claires.

N'ajoutez pas spontanément des mécanismes techniques coûteux. Les microservices, services cloud, notifications et paiements externes sont des options, pas des objectifs. La première version doit avant tout résoudre des tâches concrètes avec une sécurité et une maintenance proportionnées.

## 12. Exercice final : récupérer le projet

Imaginez que le travail s'interrompt aujourd'hui. Demain, un nouveau Planner arrive sans lire le chat précédent. Le dépôt et le runtime autorisé doivent indiquer si la gestion des membres est acceptée, quel candidat et quelles preuves l'établissent, quelles décisions sur les cotisations restent ouvertes, qui possède la campagne et quelle action peut suivre.

Si deux campagnes se déclarent actives sur la même ressource, le nouveau responsable réconcilie l'autorité. Si un rapport est marqué `CURRENT` mais pointe vers une source ancienne, il ne devine pas. Si le témoin de DB est absent, il conserve un HOLD ciblé et poursuit les vérifications sûres.

Classez les événements rencontrés : nouvelle décision métier, bogue dans le charter, panne d'environnement, permission externe manquante ou invalidation stratégique. Chacun suit une route et un propriétaire adaptés. L'architecture réussit lorsqu'il est possible de faire ce classement à partir des sources durables.

Le résultat de l'exercice n'est pas la présence de `.agentic-sdlc/`, ni un nombre de commits. C'est la capacité d'un produit à accomplir un parcours réel et de l'équipe à en retrouver la preuve après une interruption, sans transformer le CLIENT en coordinateur technique.

**Fin de l'exemple :** revenez à l'[index des chapitres](README.md) pour approfondir un thème ou consulter les sources techniques.

## Sources et portée

- [Exemple synthétique minimal](../../../../examples/minimal/README.md)
- [Fork et bootstrap](../../../01_FORK_AND_BOOTSTRAP.md)
- [Découverte, exigences et livraison](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Limites du CLIENT](../../../../protocols/CLIENT_BOUNDARY.md)
- [Standard des charters](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Guide public v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Précontrôle de gouvernance existante](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)

Ce scénario est pédagogique. Il ne représente ni une application déployée, ni une fonctionnalité acceptée, ni une intégration externe démontrée.
