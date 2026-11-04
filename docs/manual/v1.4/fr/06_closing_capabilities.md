# 06 — Clôture des capacités et acceptation

ArquitecturaRepo · Manuel d'utilisation complet · Édition v1.4 · Français

> Une capacité se clôt sur **un candidat exact et les preuves qui lui correspondent**. Un terminal technique de I3 permet l'audit stratégique ; il n'approuve pas automatiquement le produit, ne remplace pas une évaluation humaine et ne donne pas le droit de publier ou de déployer. La clôture distingue ces décisions tout en évitant de créer une campagne pour chaque bogue.

## Dans ce chapitre

1. Une capacité est un résultat de produit
2. Les cinq composantes d'une clôture
3. Le candidat exact est l'unité de revue
4. Preuves insuffisantes sans campagnes artificielles
5. Accepter, reprendre ou changer d'objectif
6. Revues périodiques et règle d'arrêt
7. Un enregistrement de clôture vérifiable
8. Exemple de rejet et de correction
9. Produit utilisable contre framework vert
10. Que faire après la clôture

## 1. Une capacité est un résultat de produit

«Gestion des membres» n'est pas terminée parce qu'un formulaire existe ou que des commits ont été créés. Elle est terminée lorsque l'utilisateur prévu peut effectuer les actions convenues dans l'environnement pertinent, que les données sont conservées conformément aux exigences, que les contrôles applicables passent et que les responsables compétents acceptent les preuves.

Le Planner définit le charter et les limites de la capacité. I3 développe, intègre un candidat identifiable, exécute les tests et organise la revue indépendante pertinente. Le Planner audite le terminal à partir des exigences actuelles. Le CLIENT conserve son autorité sur les choix de produit, l'expérience et les effets externes réservés.

Une campagne peut comprendre plusieurs sessions, reprises après crash et candidats successifs. Elle ne se termine pas parce qu'un agent atteint une limite de contexte. Les interruptions ne révoquent pas les décisions précédentes, mais ne créent pas non plus de nouvelles autorisations. Le résultat doit rester reconstructible sans mémoire du chat.

Une capture d'écran ne suffit pas à prouver une fonctionnalité qui modifie des données. Un backend qui répond à un test unitaire ne démontre pas qu'un utilisateur peut accomplir la tâche. Les preuves doivent correspondre au résultat réellement promis.

## 2. Les cinq composantes d'une clôture

| Composante | Question à résoudre |
| --- | --- |
| Résultat visible | L'utilisateur peut-il effectuer la tâche dans l'environnement prévu ? |
| Vérifications applicables | Les contrôles de logique, intégration, données, sécurité et expérience pertinents ont-ils été exercés ? |
| État courant cohérent | Code, configuration, exigences, DB et artefacts correspondent-ils au candidat ? |
| Absence de blocage matériel dissimulé | Un défaut ouvert invalide-t-il le résultat annoncé ? |
| Acceptation compétente | Planner et CLIENT ont-ils examiné les preuves relevant de leurs responsabilités ? |

Tous les projets n'exigent pas la même profondeur de contrôle. Un script interne simple n'a peut-être pas de gate perceptuel significatif. Une application qui conserve des cotisations exige des vérifications de persistance, de droits d'accès et de parcours utilisateur. Un contrôle ne peut pas remplacer silencieusement un autre qui importe pour le produit.

Les gates à distinguer sont :

- **Unit :** logique isolée conforme aux entrées et cas négatifs attendus.
- **Integration :** composants interconnectés respectant leurs interfaces réelles.
- **DB/currentness :** données, migrations, états et références actuelles cohérents et durables.
- **Semantic/generalization :** comportement conforme à la règle métier, au-delà d'une fixture étroite.
- **Physical :** application ou artefact exécuté réellement dans l'environnement prévu.
- **Perceptual/human :** expérience et qualité subjective évaluées par une personne compétente lorsque c'est nécessaire.
- **Release :** distribution exacte, permissions, droits, checksums et conditions externes vérifiés.

Une validation JSON ne prouve pas les opérations CRUD. Un screenshot ne prouve pas la DB. Une CI verte ne prouve pas l'expérience. Chaque gate a un candidat, un propriétaire, des critères et des éléments de preuve. Des contrôles disproportionnés peuvent retarder une livraison sans réduire les risques ; des contrôles manquants peuvent produire une fausse acceptation.

## 3. Le candidat exact est l'unité de revue

Le réviseur indépendant examine le même candidat que celui proposé à l'acceptation. Selon le projet, cela comprend le commit, la configuration, la version du schéma, les témoins de base, les hashes d'assets et l'environnement. Une revue du candidat A n'autorise pas une version B modifiée, même si le nom de la branche ou du fichier est identique.

Le parcours normal consiste à intégrer, figer l'identité pertinente, réaliser les tests physiques et la revue, puis présenter le terminal au Planner. Une modification matérielle postérieure exige de renouveler les contrôles affectés. Des preuves réellement indépendantes des changements peuvent être conservées lorsque leurs dépendances sont connues.

Le [protocole de freeze, revue et terminal](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md) définit cette relation. Il ne permet pas au contrôleur de référence d'imiter l'acceptation d'un utilisateur réel ou le comportement d'un système externe qu'il n'a pas exécuté.

Après une revue technique positive, les gates humains, de sécurité, de droit ou de publication peuvent rester ouverts. Le rapport doit le dire clairement. Un terminal signifie «prêt pour le jugement suivant», pas «toutes les autorisations sont acquises».

Cette exigence de précision protège aussi contre des faux négatifs. Si une revue ancienne concerne une fonctionnalité inchangée, elle peut rester pertinente. Mais il faut pouvoir démontrer la relation de dépendance plutôt que supposer que l'ancien PASS est universel.

## 4. Preuves insuffisantes sans campagnes artificielles

Si le terminal ne satisfait pas une condition déjà comprise dans le charter, le Planner renvoie à I3 un ensemble **consolidé de falsificateurs** : exigence, candidat, preuve, résultat observé et gate affecté. I3 corrige, teste, intègre et soumet un nouveau candidat dans la **même campagne**.

Un bug, un test d'intégration échoué, un retry, une refactorisation interne ou un avis de reviewer concernant une erreur de portée sont des sujets d'exécution. Il n'est pas justifié de créer un nouveau charter ou des PASS stratégiques supplémentaires à chaque défaut.

Lorsque le même type de défaillance revient plusieurs fois, I3 doit durcir le sous-système de manière approfondie. Le travail peut demander une inspection des transactions, de la concurrence, des tests négatifs, des invariants et de la revue indépendante. La priorité est d'éliminer la classe de défauts, non de produire une série de faux terminaux.

Une décision de produit nouvelle, une autorisation modifiée ou une incompatibilité stratégique peuvent exiger de revoir le charter. La difficulté d'un bogue, à elle seule, ne modifie pas le périmètre. Cette distinction empêche les cycles inutiles de Planner et les extensions de portée non autorisées.

Un bon terminal est concis : identité et environnement du candidat, parcours réellement exercé, preuves des gates réussis, gates ouverts et leur impact, risques nouveaux et propriétaire de la prochaine action. Ce document indexe des preuves canoniques et ne constitue pas un deuxième Product State.

## 5. Accepter, reprendre ou changer d'objectif

**Accepter.** Lorsque les preuves appropriées existent, le Planner enregistre l'acceptation et met à jour les références canoniques. Le CLIENT effectue l'acceptation réservée sur le produit et l'expérience. Les travaux downstream ne doivent dépendre que des capacités réellement acceptées.

**Reprendre après interruption.** Un nouvel exécuteur reconstruit Goal, charter, checkpoint, source, DB et effets pendants. Il ne déclare pas le travail terminé parce que l'ancienne conversation est inaccessible. Le résultat durable a plus d'autorité qu'un souvenir ou qu'un résumé rassurant.

**Changer de priorité.** Un report de livraison ne modifie pas forcément les exigences. Une nouvelle politique de cotisation, en revanche, modifie le produit. Les supersessions et conséquences doivent être enregistrées ; on ne conserve pas deux règles contradictoires comme état courant du même sujet.

**Conserver HOLD.** Si la correspondance entre le candidat et l'état actuel ne peut pas être vérifiée, les acceptations dépendantes restent bloquées. Les analyses sûres peuvent continuer. HOLD n'est ni un échec définitif ni une permission d'inventer les faits manquants.

## 6. Revues périodiques et règle d'arrêt

Une revue hebdomadaire devrait permettre au CLIENT de demander : quelles capacités sont acceptées, que peut-on démontrer, quel risque de délai est réel, quel budget reste justifié, quelle décision dépend de moi et quelle est la prochaine livraison vérifiable ? Le rapport s'appuie sur le produit, pas seulement sur les activités.

Le nombre de commits, de documents, d'agents, de tests ou de tokens n'est pas une mesure de progression produit. Ces opérations peuvent être nécessaires, mais une fonctionnalité qui ne fonctionne pas ne devient pas plus utile parce qu'elle a généré beaucoup de rapports.

Le starter comporte une règle d'arrêt : une fois les gates de release satisfaits, il ne faut pas accumuler des politiques génériques sans défaillance concrète ou capacité manquante. Chaque mécanisme supplémentaire a un coût de maintenance et peut introduire de nouvelles contradictions.

Le même principe vaut pour une application. Accepter trop tôt un résultat cassé est dangereux ; chercher indéfiniment des microdéfauts sans impact peut empêcher toute livraison. Le Planner et le CLIENT doivent pouvoir distinguer les risques matériels des améliorations secondaires.

## 7. Un enregistrement de clôture vérifiable

Une personne qui n'a pas participé à la campagne doit pouvoir retrouver les éléments essentiels sans relire le chat. L'enregistrement peut pointer vers les surfaces canoniques :

| Champ | Preuve recherchée |
| --- | --- |
| Candidat | Identité précise du code, de la configuration, de l'état et des artefacts. |
| Résultat | Entrée, action et sortie observée du parcours de bout en bout. |
| Tests | Résultats, environnement et commandes pertinents. |
| Données persistantes | Relecture après écriture, redémarrage et récupération si nécessaires. |
| Sécurité et droits | Contrôles proportionnés à la confidentialité et aux ressources externes. |
| Revue indépendante | Réviseur, périmètre et candidat effectivement examinés. |
| Changements après revue | Différences et contrôles renouvelés. |
| Acceptation humaine | Décision authentique, jamais déduite d'une capture. |
| Route suivante | Accepter, renvoyer à I3, demander une décision ou HOLD motivé. |

Ce tableau ne doit pas être recopié dans un second fichier `CURRENT` concurrent. C'est une carte vers les sources existantes. Un lien vers un artefact manquant ou une fixture sans rapport avec le produit est insuffisant pour accepter le résultat.

La preuve de release du framework et la preuve de fonctionnalité d'une application doivent rester distinctes. Le starter peut avoir passé des validations internes et des essais d'installation portables sans démontrer l'ergonomie ou la logique métier d'un produit externe.

## 8. Exemple de rejet et de correction

Supposons qu'une application permet de créer et désactiver des membres. Un reviewer découvre que la désactivation supprime leurs paiements historiques, alors que le charter exige leur conservation. Le Planner renvoie un falsificateur précis : «La désactivation d'un membre avec paiements doit préserver les transactions après redémarrage ; le candidat X les perd».

I3 recherche la cause de persistance, corrige les relations, ajoute une régression pertinente, démontre la lecture après redémarrage, intègre un nouveau candidat et demande une revue indépendante. Il n'ouvre pas une campagne «réparer désactivation» et n'oblige pas le CLIENT à choisir les contraintes de clés étrangères.

Si le reviewer avait examiné A et que la correction produit B, l'ancien PASS ne suffit pas pour B. Les tests non affectés peuvent rester réutilisables, mais le nouveau comportement et les données modifiées doivent être testés et revus sur la bonne identité.

À l'inverse, si le CLIENT demande la réactivation d'un membre avec des permissions spéciales, cela ajoute une règle. Le Planner confirme les conditions et l'impact stratégique. Une nouvelle fonctionnalité n'est pas un simple bogue de l'ancien système.

## 9. Produit utilisable contre framework vert

Un contrôleur peut valider une campagne synthétique et atteindre un terminal sans qu'une interface de produit existe. Pour accepter une gestion des membres, il faut ouvrir l'application, créer une fiche fictive, la retrouver, la modifier, la désactiver et conserver l'historique. Si la persistance est importante, redémarrer et relire. Si des permissions existent, tester également l'accès refusé.

Le `tools/verify_v1_release.py` vérifie une version précise du framework avec des fixtures. Source, installation portable Linux/Windows, distribution publique et capacité d'une application construite avec ce framework sont des gates distincts. La [matrice de support v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) précise les comportements réellement exercés.

Dire «tous les tests sont passés» sans nommer le candidat et les tests peut induire le CLIENT en erreur. Il peut être exact que les contrats du starter soient verts et que l'application n'ait pas encore été exécutée. L'honnêteté sur les limites permet de concentrer le travail sur le bon risque.

Les intégrations natives de fournisseurs tiers demandent leurs propres preuves. Un script portable qui fonctionne ne démontre pas qu'un agent propriétaire a été connecté, authentifié et exécuté dans le projet du CLIENT.

## 10. Que faire après la clôture

Après acceptation, mettez à jour les surfaces canoniques, les références de source et les dépendances qui peuvent réellement être débloquées. Après un rejet pour défaut dans le charter, renvoyez à I3 la correction consolidée. Après invalidation stratégique, reconsidérez le périmètre avec le propriétaire approprié.

Si currentness reste inconnue, maintenez un HOLD ciblé et poursuivez les vérifications sûres. Le CLIENT doit savoir quelles capacités sont utilisables, quels gates restent ouverts, qui les traite et quand un nouveau résultat sera revu.

Une bonne clôture est assez courte pour être comprise et assez précise pour être falsifiable. Si une personne sceptique et absente de l'implémentation ne peut pas retrouver la preuve, l'état n'est pas encore suffisamment reconstructible.

**Suite :** chapitre 07, l'exemple complet d'une application de gestion de club.

## Sources et portée

- [Intégrité de freeze et de terminal](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Cycle de vie des capacités](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Validation exécutable](../../../10_EXECUTABLE_VALIDATION.md)
- [Gates de release du framework](../../../17_V1_RELEASE_GATES.md)
- [Support et distribution v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Vérificateur de release](../../../../tools/verify_v1_release.py)

L'acceptation appartient au produit, au candidat et aux autorités réels. Ces exemples ne confèrent aucune permission supplémentaire.
