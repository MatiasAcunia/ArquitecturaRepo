# 02 — Le Planner et l'adoption du projet

ArquitecturaRepo · Manuel d'utilisation complet · Édition v1.4 · Français

> La création de `.agentic-sdlc/` n'est pas l'adoption d'un produit. Le Planner doit relier les contrats génériques à un code réel, des exigences confirmées, des propriétaires légitimes, des données actuelles et un environnement vérifiable. L'adoption doit permettre la reconstruction depuis un contexte neuf **sans inventer d'état ni doubler une gouvernance existante**.

## Dans ce chapitre

1. Parler du produit avant de parler des agents
2. Préparer le contexte de travail
3. Découverte : poser les questions qui comptent
4. Baseline du produit et plan de livraison
5. L'adoption comme lien avec le projet réel
6. L'épreuve du contexte frais
7. Autoriser la première campagne
8. Exemple de session avec le Planner
9. Un baseline que le CLIENT peut confirmer
10. Délimiter une première capacité

## 1. Parler du produit avant de parler des agents

Une personne explique : «Je voudrais gérer les inscriptions de mon club» ou «j'ai besoin d'une API pour mon activité». Le Planner commence par comprendre les personnes utilisatrices, les tâches difficiles et le résultat que le CLIENT souhaite observer. Il ne répond pas immédiatement par une liste d'agents, de microservices ou de règles de gouvernance.

Le CLIENT n'a pas à fournir le schéma relationnel ni l'arborescence de classes. Il doit toutefois confirmer les règles qui changent le comportement du produit. Par exemple, une inscription peut-elle dépasser la capacité d'une activité ? Les paiements historiques doivent-ils rester après une désactivation ? Ces décisions ont des conséquences techniques ; elles ne peuvent pas être devinées par l'implémentation.

Une bonne première conversation clarifie le public, l'environnement, les données, les permissions, les contraintes de temps et de budget, les exclusions et le premier résultat utile. Des questions restent parfois ouvertes. Le Planner les conserve comme telles, sans convertir une possibilité en exigence approuvée.

La profondeur de cette exploration doit correspondre au risque. Un prototype local sans données sensibles peut demander une courte session. Une application publique qui traite de l'argent ou des informations personnelles exige un modèle plus précis des droits d'accès, de la récupération, des coûts et des impacts possibles.

## 2. Préparer le contexte de travail

Avant de modifier le projet, examinez sa source et son état. Quelle est la branche Git actuelle ? Quel commit correspond au code réellement ouvert ? Existe-t-il des modifications locales non intégrées ? Quels tests, fichiers de configuration, bases de données, outils de démarrage et artefacts sont présents ? Une copie ressemblant au bon dépôt ne suffit pas à prouver son identité.

L'investigation initiale peut être en lecture seule. Le but est de découvrir l'état réel, pas d'imposer immédiatement le modèle d'un projet fictif. Si l'application possède déjà un Product State ou un contrôleur canonique, le [précontrôle de gouvernance existante](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) protège cette autorité. Une seconde couche concurrente ne doit pas être installée pour faire disparaître un message de HOLD.

Un inventaire de fichiers et de hashes aide à vérifier la source, mais ne révèle pas à lui seul les exigences. Une table nommée `payments` ne précise pas les règles de remboursement. Un dossier `admin` ne prouve pas que l'accès est effectivement protégé. Le Planner vérifie les faits techniques avec la source et les règles fonctionnelles avec le CLIENT.

Protégez la confidentialité des éléments étudiés. Le dépôt public du framework n'est pas le lieu où placer des données privées du produit. Un manifeste peut référencer un artefact par identité ou hash sans copier son contenu vers un service tiers. La continuité ne requiert pas l'exposition de secrets.

## 3. Découverte : poser les questions qui comptent

Dans l'exemple d'un club, le Planner peut demander : qui travaille sur les inscriptions, quand un membre est-il considéré en règle, qu'arrive-t-il aux activités complètes, comment une annulation libère-t-elle une place et qui peut consulter l'historique des paiements ? Les réponses affectent les interfaces et les données.

Une question n'est utile que si sa réponse change une décision. Demander au CLIENT de choisir le nom d'une méthode alors que le problème est fonctionnel serait une perte de temps. À l'inverse, décider sans lui qu'un paiement ancien peut être supprimé serait franchir une frontière d'autorité.

| Nature de la question | Exemple | Ce qu'elle détermine |
| --- | --- | --- |
| Besoin | «Quelle tâche est pénible aujourd'hui ?» | La première capacité utile. |
| Règle métier | «Une dette bloque-t-elle l'inscription ?» | L'éligibilité et les messages. |
| Données | «Conserve-t-on les opérations annulées ?» | L'historique et le modèle de persistance. |
| Usage | «Deux employés travaillent-ils simultanément ?» | La concurrence et les accès. |
| Sécurité | «Qui voit les coordonnées personnelles ?» | Les autorisations et la visibilité. |
| Livraison | «Quand la première version doit-elle être utilisable ?» | Le périmètre et les dépendances critiques. |

Le Planner confronte ces réponses aux décisions déjà présentes. Il ne repose pas chaque question si la source canonique est claire. Il signale au CLIENT les choix qui restent ouverts et les conséquences d'une réponse. Si l'incertitude ne bloque pas une activité indépendante, cette activité peut être préparée sans inventer la règle manquante.

Les [instructions de découverte](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md) et le [cadre de spécification et livraison](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md) donnent des références. Elles ne remplacent pas la vérification des sources vivantes du projet concerné.

## 4. Baseline du produit et plan de livraison

Les réponses confirmées constituent un baseline de produit : objectifs, utilisateurs, comportements, critères de validation, exclusions et questions non résolues. En parallèle, l'ingénierie établit un baseline technique fondé sur le code : stack, dépendances, schéma, données actuelles, réseau, sécurité, tests, sauvegardes et déploiement prévu.

Les deux baselines se complètent. Une description métier ne prouve pas que l'application existe ; un schéma SQL ne prouve pas que le CLIENT l'approuve. Leur relation doit être explicite et pointée vers la version réelle de la source, avec owners et état courant vérifiables.

La livraison est découpée en capacités observables. Pour un club, on peut commencer par l'identité des membres, puis les cotisations, ensuite les activités et enfin les inscriptions. Chaque étape a des critères concrets et des dépendances. On évite d'autoriser des travaux qui s'appuient sur une règle de paiement non décidée.

Les jalons datés doivent être réalistes et conditionnés par des risques identifiés. «Créer cent commits» n'est pas un jalon de produit. «Un administrateur peut enregistrer un membre et le retrouver après redémarrage» fournit une preuve mesurable. Le Planner ajuste le plan lorsque les exigences, les ressources ou les contraintes changent réellement.

La documentation doit rester compacte et canonique. Le but n'est pas de recopier les mêmes exigences dans cinq fichiers `CURRENT`, mais de rendre les décisions et références accessibles, versionnées et non contradictoires.

## 5. L'adoption comme lien avec le projet réel

Adopter le framework signifie associer ses mécanismes de coordination au projet existant. Le Planner et l'ingénierie identifient source Git, Product State, responsabilités, données, artefacts, campagne actuelle et interfaces. Ils vérifient ce qui peut être transféré et ce qui ne doit pas être écrasé.

Le [contrat de transfert et d'adoption](../../../16_TRANSFER_ADOPTION.md) décrit les enregistrements et les tests nécessaires. Une spécification d'adoption doit être examinée et validée avant toute promotion matérielle de l'état. Un exemple synthétique n'est pas un substitut à la source de vérité de l'application.

Pour un dépôt possédant déjà un contrôle canonique, un attachment de lecture et une éventuelle migration autorisée sont nécessaires. Une installation générique par-dessus une campagne active ou un Product State v1.2/v1.3 peut détruire l'historique d'autorité. Le scaffold v1.4 n'est pas un mécanisme d'upgrade automatique universel.

Les données persistantes nécessitent une preuve cohérente. Avec SQLite/WAL, un hash du fichier principal peut ne pas représenter les transactions les plus récentes. Il faut un snapshot transactionnellement cohérent lorsque le contrat l'exige. Si la correspondance avec le code ou l'état courant est inconnue, on garde un HOLD sur les écritures dépendantes.

Les artefacts suivent le même principe : un fichier nommé `resultat-final.pdf` ne prouve pas son identité. Le chemin, le hash, les sources et le contexte doivent être reliés à la capacité lorsque cela compte pour la revue, la réutilisation ou la publication. Il n'est pas nécessaire de dupliquer des gigaoctets pour chaque agent ; on peut référencer l'artefact canonique.

## 6. L'épreuve du contexte frais

L'adoption doit être compréhensible par une nouvelle session qui ne connaît pas les discussions antérieures. Cette session retrouve le produit, les décisions actuelles, le propriétaire de la campagne, le code, la DB, les preuves et la prochaine action autorisée. C'est une épreuve plus pertinente que la simple présence de fichiers bien formés.

L'outil installé `reconstruct_context.py` vérifie certaines relations du contrôle portable. Il ne lit pas l'esprit du CLIENT et ne remplace pas l'inspection de l'application. Un nouveau Planner doit comparer ses résultats avec les sources et signaler les contradictions plutôt que de choisir le résumé le plus récent.

Si deux campagnes revendiquent la même ressource, elles doivent être réconciliées. Si un reviewer a approuvé un commit différent de celui qui est ouvert, la revue ne doit pas être réutilisée sans analyse. Si une DB n'a pas de témoin cohérent, on documente l'incertitude et l'owner capable de la résoudre.

Un HOLD précis peut indiquer : «La base utilise WAL et aucune photographie cohérente correspondant au code adopté n'a été trouvée ; les lectures sont autorisées, les écritures qui dépendent de cette cohérence sont suspendues». Ce diagnostic est plus utile qu'une déclaration vague d'impossibilité ou qu'un `READY` fabriqué.

## 7. Autoriser la première campagne

Après adoption, le Planner définit un charter de capacité : résultat visé, raison, limites, interfaces, dépendances, ownership, critères d'acceptation, gates et falsificateurs. Il ne transforme pas le charter en une liste de centaines de microtâches imposant chaque commande à I3.

Avant une autorisation importante, une première analyse stratégique reconstruit le produit final et les interactions entre données, runtime, sécurité, coûts, licence, récupération, utilisateur et étapes downstream. Une seconde analyse adversariale cherche des hypothèses fausses. Une nouvelle analyse stratégique supplémentaire n'est justifiée que par un changement de preuve ou un risque systémique matériel.

Une fois le charter approuvé, I3 possède l'exécution. Les tests échoués, refactorisations internes, nouvelles révisions techniques et reprises après crash restent normalement dans la même campagne. Le Planner reçoit un terminal consolidé quand il existe une véritable décision stratégique à prendre.

Cette frontière permet au CLIENT de rester responsable du produit sans devenir gestionnaire des erreurs internes. L'ingénierie peut travailler longtemps et s'adapter à des échecs sans perdre la continuité ni demander une nouvelle signature à chaque correction.

## 8. Exemple de session avec le Planner

Le CLIENT explique : «Je veux une application locale pour gérer les membres d'une association ; nous utilisons actuellement une feuille de calcul et nous avons besoin d'une première version dans un mois». Le Planner demande quels parcours doivent fonctionner au premier jalon, qui utilisera le logiciel et si les données actuelles doivent être migrées.

Il vérifie le dépôt existant et les éventuels fichiers de données. S'il existe déjà une interface et une DB, il ne les jette pas pour reproduire un exemple. S'il n'y a pas de code, il propose une technologie proportionnée aux contraintes et explique les impacts importants sur l'installation et la maintenance.

La première capacité pourrait être l'enregistrement et la recherche de membres avec persistance. Les cotisations seraient un jalon suivant, une fois l'identité des membres stable. Les exclusions de la première version peuvent être les paiements en ligne, les notifications et les applications mobiles.

À la fin, le CLIENT sait quelles décisions ont été confirmées, quelles questions restent ouvertes, quelle démonstration aura lieu et ce qu'il doit encore choisir. Il n'est pas nécessaire qu'il connaisse tous les fichiers de contrôle ni les paramètres internes d'une transaction.

## 9. Un baseline que le CLIENT peut confirmer

Un baseline simple pourrait dire : «Un administrateur peut créer, chercher, modifier et désactiver des membres. L'historique des cotisations doit rester disponible. Le programme fonctionne sur ordinateur local. La première livraison n'effectue aucun paiement en ligne». Ces phrases deviennent des exigences seulement après confirmation.

L'ingénierie fournit ensuite les faits vérifiables : commit et configuration adoptés, environnement d'exécution, DB, méthode de sauvegarde, tests de persistance et de permissions. Les inconnues sont identifiées ; on n'invente pas de licence, de capacité du serveur ou d'approbation du CLIENT pour compléter une grille.

Ce baseline permet d'évaluer le résultat. Une interface séduisante qui ne sauvegarde pas un membre ne satisfait pas la capacité. Une application qui envoie des demandes à un fournisseur de paiement non autorisé dépasse le scope. Les critères d'acceptation mettent le comportement du produit avant le volume du code.

Lorsqu'un retour d'utilisation révèle une nouvelle règle, le Planner enregistre la supersession et examine les dépendances. Il ne maintient pas simultanément deux versions contradictoires comme vérité actuelle pour le même sujet.

## 10. Délimiter une première capacité

Un charter peut viser «Gestion des membres avec persistance démontrable». Il décrit création, recherche, édition et désactivation sur données fictives ; conservation des historiques nécessaires ; permissions ; interfaces de l'application ; et gates correspondant à l'environnement réel.

Les tests peuvent couvrir données invalides, doublons, lecture après écriture, redémarrage, accès non autorisé et parcours de l'interface. Une revue indépendante examine le candidat intégré exact. Le CLIENT intervient dans les jugements de produit et d'expérience, pas dans chaque décision de code.

Si désactiver un membre efface l'historique malgré l'exigence, I3 corrige dans la même campagne. Si le CLIENT demande ensuite un export fiscal, le Planner doit examiner les besoins, la confidentialité et les autorisations nouvelles. Les deux événements n'ont pas la même route.

Le terminal de I3 indique le candidat, les tests réalisés, les preuves physiques, les résultats de revue et les limites. Le Planner audite et accepte ou renvoie les falsificateurs pertinents. La capacité suivante dépendra de ce qui a été réellement accepté, pas d'une promesse contenue dans un rapport.

**Suite :** chapitre 03, fonctionnement quotidien et continuité de l'ingénierie.

## Sources et portée

- [Session de découverte du produit](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md)
- [Exigences, stack et livraison](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Transfert et adoption](../../../16_TRANSFER_ADOPTION.md)
- [Précontrôle des dépôts gouvernés](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Standard des charters de campagne](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Limites d'autorité du CLIENT](../../../../protocols/CLIENT_BOUNDARY.md)

Les exemples ne constituent pas des spécifications en vigueur tant que les sources et le propriétaire du produit réel ne les ont pas confirmés.
