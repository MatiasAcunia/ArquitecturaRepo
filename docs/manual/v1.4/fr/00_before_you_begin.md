# 00 — Avant de commencer

ArquitecturaRepo · Manuel d'utilisation complet · Édition v1.4 · Français

> ArquitecturaRepo est une architecture de coordination pour le développement logiciel, pas une application prête à l'emploi ni un programmeur automatique. Sa valeur consiste à rendre les décisions, les responsabilités, l'état courant et les preuves **reconstructibles au-delà d'une conversation**. Pour les commandes et le périmètre effectivement testés dans la version publique, consultez le [guide de démarrage v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) et les [notes de version](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md).

## Dans ce chapitre

1. Ce que vous installez et pourquoi
2. Qui prend quelles décisions
3. Les informations qui doivent survivre au chat
4. Comment lire le manuel complet
5. Préparer les décisions du CLIENT
6. Périmètre, limites et versions
7. Un parcours de développement concret
8. Questions fréquentes avant de commencer
9. Une fiche de départ d'une page
10. Comment évaluer la valeur du système

## 1. Ce que vous installez et pourquoi

Imaginez un projet développé avec un assistant de programmation. Un jour, l'assistant crée une API, corrige un problème et propose une organisation. Le lendemain, une nouvelle session s'ouvre et personne ne sait exactement pourquoi telle décision a été prise, quelle version du code correspond à la dernière revue ou quel résultat le propriétaire du produit avait accepté. Le code existe, mais son contexte opérationnel reste fragile.

ArquitecturaRepo vise ce problème de continuité. Il place les décisions durables et leurs références dans le dépôt et dans des surfaces canoniques explicitement identifiées. Les exigences du produit, l'identité des sources, les responsabilités, les campagnes d'ingénierie, les revues et les preuves sont liées de manière vérifiable. Une conversation reste une interface pratique, mais elle ne devient pas la seule mémoire du projet.

L'installation initiale peut créer un dossier `.agentic-sdlc/` dans un dépôt de produit qui ne possède pas déjà une gouvernance canonique incompatible. Cette couche contient des contrats, des modèles d'état, des protocoles et des outils de validation. Elle ne construit pas automatiquement votre application, ne configure pas votre base de production et n'obtient pas d'accès à un fournisseur d'IA.

Le but n'est pas d'ajouter un grand nombre d'agents. Il s'agit de réduire le temps perdu à reconstruire le contexte, de prévenir les décisions contradictoires et de vérifier les résultats avant d'annoncer qu'une fonctionnalité est prête. Une structure plus lourde que les risques qu'elle traite peut devenir contre-productive : la proportionnalité fait partie du principe de conception.

La continuité est particulièrement importante lorsque le projet dure plusieurs semaines. Un même objectif peut impliquer du code, une base de données, des fichiers générés, des décisions humaines, des interruptions et des personnes qui ne travaillent pas au même moment. Sans provenance claire, un rapport positif sur une ancienne version peut être confondu avec l'état actuel.

## 2. Qui prend quelles décisions

Le **CLIENT** est la personne responsable du produit. Il décide du problème à résoudre, des priorités, des contraintes, des choix métier et des effets externes nécessitant son autorisation. Il peut demander une application tout en ne connaissant pas les subtilités de Git, des transactions SQL ou des runners. L'organisation doit protéger son temps et ne pas lui transférer les opérations techniques.

Le **I2 Planner** reconstruit la situation, confirme les exigences, définit les capacités et leurs dépendances, propose la stratégie et audite les résultats terminaux. Pour une décision stratégique importante, il examine le produit de bout en bout puis réalise un examen adversarial séparé. Il ne revient pas automatiquement au début du processus à chaque bogue ordinaire.

Le **I3 Controller** prend en charge l'exécution continue d'une campagne autorisée. Son travail comprend l'implémentation, les tests, les refactorisations internes, la résolution des défauts, la récupération des interruptions, l'intégration et la revue indépendante. Tant que le travail reste dans les limites de la campagne, il ne demande pas une nouvelle autorisation stratégique pour chaque correction.

Le **I4** peut être un spécialiste ou un réviseur indépendant pour une tâche délimitée. Les quatre niveaux de responsabilités ne signifient pas quatre instances d'IA obligatoires. Un **I1 MASTER OWNER** peut être utile lorsqu'il faut coordonner plusieurs produits ou lignes de travail, résoudre des contradictions d'ownership ou protéger les dépendances entre systèmes. Une petite application n'a pas besoin de reproduire toute cette organisation si ses risques ne le justifient pas.

| Question | Autorité normale |
| --- | --- |
| Quel problème le produit doit-il résoudre ? | CLIENT, avec découverte guidée par le Planner. |
| Quelle capacité construire en premier ? | Planner selon les priorités confirmées. |
| Comment structurer classes, transactions ou index ? | Ingénierie sous la responsabilité de I3. |
| Le résultat respecte-t-il les exigences décidées ? | Tests et revue, puis audit du Planner. |
| L'expérience est-elle satisfaisante pour le public prévu ? | Évaluation humaine compétente, éventuellement CLIENT. |
| Peut-on payer, publier ou transmettre des données ? | Autorité explicite du responsable concerné. |

Ces distinctions évitent deux extrêmes. L'ingénierie ne doit pas inventer une règle de produit faute de réponse, et le CLIENT ne doit pas avoir à choisir les paramètres techniques d'une requête ou à réparer manuellement un contrôleur. Chaque décision doit rester auprès de son propriétaire légitime.

## 3. Les informations qui doivent survivre au chat

Une nouvelle session doit pouvoir identifier les besoins confirmés, la source actuelle, les éléments de Product State, le propriétaire de chaque opération et la prochaine action autorisée. Le dépôt contient le code et les décisions versionnées. La base de données peut contenir des faits vivants. Des manifests et des artefacts démontrent les résultats. Des journaux de transaction permettent de comprendre une interruption. Ces surfaces ont des rôles différents.

Une simple déclaration «terminé» ne remplace pas la preuve. Si un réviseur examine le candidat A et qu'un agent modifie ensuite le code pour produire B, la revue de A ne certifie pas B. La même branche Git et un nom de fichier inchangé ne suffisent pas à garantir l'identité. Les références doivent pointer vers le candidat effectivement examiné.

Le même problème existe pour les données. Une base SQLite en mode WAL peut avoir des modifications confirmées qui ne se trouvent pas encore dans le fichier principal. Un hash de ce seul fichier n'atteste pas nécessairement l'état transactionnel complet. Selon le risque, il faut un témoin cohérent ou une incertitude explicitement enregistrée.

Les décisions de produit, l'état courant mutable, l'autorité de campagne et les journaux de runtime doivent rester séparés. Si plusieurs fichiers prétendent être la source de vérité actuelle pour le même sujet, le prochain agent risque de choisir le mauvais. Une bonne architecture possède un propriétaire et une surface canonique pour chaque préoccupation.

La mémoire de conversation reste utile pour retrouver une piste, mais elle peut être incomplète ou périmée. En cas de contradiction, la source physique vivante et les enregistrements canoniques priment. Si une incertitude matérielle ne peut pas être résolue, l'action dépendante reste en HOLD, tandis que des vérifications de lecture peuvent continuer.

## 4. Comment lire le manuel complet

Le livre comprend huit chapitres détaillés. Le chapitre 00 explique le cadre. Le chapitre 01 traite de l'installation. Le chapitre 02 présente le Planner, la découverte des besoins et l'adoption. Le chapitre 03 décrit le travail quotidien. Le chapitre 04 explique comment demander des changements. Le chapitre 05 aborde les erreurs et la récupération. Le chapitre 06 distingue les preuves et l'acceptation. Le chapitre 07 suit un exemple fictif de gestion d'un club.

Pour un premier essai rapide, utilisez le [miniguide français](../../../i18n/MINI_GUIDE_fr.md). Il est volontairement court et ne constitue pas ce manuel complet. La [FAQ française](../../../i18n/FAQ_fr.md) répond à des questions de démarrage. Les documents de référence du dépôt servent à vérifier des comportements et contrats précis.

Il n'est pas indispensable de mémoriser tous les noms de fichiers internes. Il faut surtout apprendre à poser les bonnes questions : que souhaite la personne utilisatrice, où est la preuve, qui peut agir, quelle version est actuelle et qu'est-ce qui empêcherait une acceptation honnête ? La pratique avec un produit concret donne du sens à ces concepts.

Les commandes figurant dans les chapitres sont des exemples adaptés à v1.4. Les interfaces et les outils peuvent évoluer. Avant une action importante, vérifiez les options du script de la version effectivement utilisée et ne mélangez pas des guides historiques avec une distribution plus récente sans contrôler les différences.

## 5. Préparer les décisions du CLIENT

Avant la première campagne, une description d'une page peut suffire : qui utilisera le produit, pour quelle tâche, quel premier résultat observable, avec quels délais et quel budget. Mentionnez les données sensibles, les contraintes d'accès et les opérations qui devront être explicitement autorisées. Les inconnues peuvent rester inconnues si elles sont clairement identifiées.

Par exemple, «je veux gérer les membres d'un club» ne précise pas si une cotisation impayée bloque l'inscription à une activité, si une désactivation efface l'historique ou si plusieurs employés travaillent simultanément. Le Planner doit confirmer ces règles, car elles changent la fonctionnalité. En revanche, le nom d'une classe ou le choix d'un index SQL appartient normalement à l'ingénierie.

Un bon premier objectif est observable : «Un administrateur peut créer un membre fictif, le retrouver et voir que ses modifications persistent après redémarrage». Cette phrase donne une direction à l'implémentation et des critères de test. «Construire une architecture professionnelle» n'indique pas à lui seul comment mesurer la livraison.

Le CLIENT peut apprendre en voyant un prototype puis ajuster son besoin. Les décisions nouvelles doivent être enregistrées et leurs conséquences évaluées. Le système n'est pas conçu pour rendre irrévocable la première intuition, mais pour éviter que plusieurs versions contradictoires de la même règle restent actives.

## 6. Périmètre, limites et versions

La [version publique v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0) existe sous forme de distribution versionnée, avec archive portable, checksum et manifest. Pour une installation reproductible, contrôlez les octets téléchargés contre cette publication. La branche `main` peut avoir reçu de la documentation après la sortie : son contenu ne fait pas rétroactivement partie de l'archive publiée.

Les mécanismes portables testés comprennent les profils, le scaffold, la validation, la récupération et des parcours synthétiques sur Linux et Windows. Cette vérification ne démontre pas qu'une application particulière est correcte ni qu'une intégration native à Codex Desktop ou à un autre service a été exercée. Les outils externes ont leurs propres autorisations et tests.

ArquitecturaRepo est indépendant du fournisseur de modèle. Il n'installe pas un LLM, ne configure pas de facturation et n'autorise pas des effets de réseau par défaut. Il peut aider à coordonner une équipe humaine, des agents facultatifs ou un mélange des deux. Les résultats dépendent de l'implémentation et des preuves effectives, non du seul nom de l'architecture.

Les profils `SMALL`, `STATEFUL`, `ARTIFACT_HEAVY`, `MULTI_WORKSTREAM`, `MULTI_PRODUCT` et `HIGH_CONSEQUENCE` permettent de proportionner les contrôles. Ils ne constituent pas des niveaux de certification ni des obligations de créer davantage d'agents. Le profil est choisi selon le risque réel du produit et peut être réévalué si ce risque change.

Une application qui possède déjà une gouvernance canonique ne doit pas être écrasée par le scaffold générique. Le [précontrôle en lecture seule](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) permet d'examiner les sources et témoins requis. Il ne constitue pas une migration universelle d'un Product State v1.2/v1.3 ni une permission de remplacer des données existantes.

## 7. Un parcours de développement concret

Prenons une petite application de réservation. Le CLIENT demande la création et la consultation de réservations, avec impossibilité de dépasser la capacité d'une salle. Le Planner vérifie les utilisateurs, les conflits, les annulations, les données et le délai. Les décisions confirmées forment un baseline de produit lié au code et à l'environnement actuels.

Le Planner définit une première capacité et un charter. I3 implémente les interfaces, corrige les bogues, intègre un candidat et exécute les contrôles applicables. L'essai physique consiste à créer une réservation, relire le résultat, tenter un conflit et vérifier la persistance si elle fait partie des exigences. Le rapport doit indiquer la version exacte testée.

Le Planner audite ensuite les preuves. Le CLIENT juge les décisions réservées, notamment l'expérience utilisateur. Si une double réservation est possible alors qu'elle est interdite, I3 la corrige dans la campagne actuelle. Si le CLIENT introduit ensuite une priorité réservée à certains membres, c'est une règle nouvelle que le Planner doit confirmer et intégrer à la stratégie.

Après acceptation, les références canoniques indiquent le candidat réellement approuvé. Une personne qui rejoint le projet demain peut retrouver les exigences, l'état et la prochaine action sans relire toute la discussion. Cette continuité est l'un des avantages potentiels d'une architecture de développement structurée.

## 8. Questions fréquentes avant de commencer

**Faut-il plusieurs agents ?** Non. Les responsabilités peuvent être assumées par un petit nombre de personnes ou d'outils, à condition de conserver les limites d'autorité et les preuves nécessaires. Plus d'agents peut au contraire augmenter les conflits si les ressources partagées ne sont pas coordonnées.

**Est-ce mieux que coder directement dans un chat ?** Cela dépend du contexte. Une petite démonstration peut être plus rapide en dialogue direct. Un produit long et évolutif peut bénéficier d'une meilleure conservation des décisions et des preuves. Le gain doit être évalué en temps, qualité, erreurs, récupérabilité et effort demandé au CLIENT ; il ne faut pas proclamer une supériorité non mesurée.

**Que faire lorsqu'un agent se trompe ?** Si le défaut relève du charter approuvé, I3 corrige et reteste. La difficulté technique ne justifie pas automatiquement un nouveau plan stratégique. Une vraie modification du besoin ou une invalidation matérielle peut en revanche justifier une nouvelle décision du Planner.

**Que signifie HOLD ?** C'est l'interdiction temporaire d'une action dépendante lorsque les preuves ou autorisations sont insuffisantes. Cela n'empêche pas les diagnostics sûrs en lecture seule. Un HOLD utile précise la cause, le propriétaire et les informations à obtenir.

**Le dépôt de mon application peut-il rester privé ?** Oui. Le starter n'exige pas l'envoi du code, des données, des identifiants ou des conversations à son mainteneur. Les intégrations externes ont leurs propres réglages et doivent respecter les permissions et la confidentialité.

## 9. Une fiche de départ d'une page

Avant une campagne, essayez de répondre à ces questions. Les réponses doivent pointer vers les sources véritables du projet, pas vers un document parallèle devenu concurrent :

| Sujet | Ce qui doit être connu |
| --- | --- |
| Produit | Public, problème et premier résultat observable. |
| Dépôt | Source réelle, branche/ref, modifications locales et historique pertinent. |
| Responsabilités | CLIENT, Planner, Controller et propriétaires des ressources partagées. |
| Exigences | Décisions confirmées, questions ouvertes et exclusions. |
| Environnement | Stack, base, réseau, contraintes de sécurité, coûts et accès. |
| État courant | Product State et références sans contradiction matérielle. |
| Campagne | Objectif autorisé, interfaces, critères et falsificateurs. |
| Preuves | Gates nécessaires, identité du candidat et résultats vérifiés. |
| Continuité | Prochaine action reconstructible dans une session nouvelle. |

Si une donnée essentielle manque, identifiez qui peut la confirmer. Un identifiant de commit absent est un problème de traçabilité, pas une préférence métier. Une règle d'accès non décidée relève du CLIENT. Une erreur de test relève généralement du Controller. Les bonnes routes réduisent les discussions inutiles.

Cette fiche sert d'index, pas de nouvelle surface `CURRENT`. Dupliquer la même vérité dans plusieurs fichiers sans ownership clair accroît le risque de divergence. Le principe reste un état canonique par sujet, avec des références qui permettent de comprendre ses dépendances.

## 10. Comment évaluer la valeur du système

Après plusieurs semaines, mesurez si le projet reprend facilement après une interruption, si les décisions restent cohérentes, si les défauts sont résolus au bon niveau et si les personnes utilisatrices disposent d'une capacité démontrable. La quantité de commits, de réunions et de tokens ne constitue pas une mesure directe du produit.

Pour comparer à une approche de programmation directe, observez le temps total, l'effort du CLIENT, la qualité des tests, les régressions, la continuité et la facilité de transférer le travail. L'architecture peut imposer un coût initial plus important ; ce coût est justifié seulement s'il améliore réellement la livraison ou réduit un risque important.

N'ajoutez pas un nouveau protocole par réflexe après chaque problème. Une règle supplémentaire doit traiter une catégorie de défaillances ou une capacité qui manque vraiment. L'efficacité du système tient à la qualité des décisions et de leur exécution, pas à la taille de sa documentation.

**Suite :** chapitre 01, installation et configuration de la couche de contrôle v1.4.

## Sources et portée

- [Vue d'ensemble de l'architecture](../../../00_ARCHITECTURE_OVERVIEW.md)
- [Profils de déploiement](../../../06_SCALING_PROFILES.md)
- [Limite de décision du CLIENT](../../../../protocols/CLIENT_BOUNDARY.md)
- [Cycle de vie des capacités](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Démarrage public v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Notes de version v1.4](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)

Ce chapitre présente une méthode et ses limites. Il ne certifie pas des applications tierces, des intégrations externes ni des performances comparatives non mesurées.
