# 03 — Fonctionnement quotidien

ArquitecturaRepo · Manuel d'utilisation complet · Édition v1.4 · Français

> Une session commence par les références **CURRENT**, le code et les preuves, non par le souvenir du dernier échange. I3 possède l'exécution technique dans les limites du charter ; les autorisations, la confidentialité, les coûts et les gates restent valables durant toute la campagne.

## Dans ce chapitre

1. Reprendre le travail sans repartir de zéro
2. Transformer une demande en capacité vérifiable
3. Responsabilité continue du Controller
4. Autorisations et effets externes
5. Lire un rapport d'exécution de manière critique
6. Git, changements locaux et continuité
7. Ressources, artefacts et espace disque
8. Coordination, concurrence et rôle du CLIENT
9. Revue indépendante du candidat exact
10. Une routine quotidienne simple

## 1. Reprendre le travail sans repartir de zéro

Ouvrir un nouveau chat n'ouvre pas un nouveau projet. Le Planner ou le Controller récupère l'intention confirmée, le Product State, la branche et le commit réels, les éventuelles modifications locales, les campagnes actives, les owners, les témoins de DB et les artefacts. Les résumés de conversation peuvent indiquer une piste, mais ne doivent pas remplacer ces sources.

La reconstruction commence habituellement en lecture seule. Si l'état actuel n'est pas vérifiable, il vaut mieux déclarer l'incertitude précise que choisir une version arbitraire. Deux branches portant des noms similaires ou deux fichiers `final` peuvent contenir des résultats différents. Les références et hashes permettent de connaître le candidat qui a réellement été testé.

Une nouvelle session doit pouvoir répondre : quelle capacité est en cours, qui la contrôle, quel travail reste autorisé, quels gates ont été exercés et quel prochain effet peut être exécuté ? Si la réponse dépend uniquement de la mémoire d'un agent précédent, la continuité est encore insuffisante.

Le [bootstrap du dépôt](../../../01_FORK_AND_BOOTSTRAP.md) et le [protocole de reconstruction de currentness](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md) décrivent le rôle des sources et des références. Un rapport `READY` n'est pas une preuve s'il pointe vers des éléments manquants ou contradictoires.

## 2. Transformer une demande en capacité vérifiable

Le CLIENT demande par exemple : «Je veux voir toutes les cotisations en retard et la date du dernier paiement». Le Planner vérifie la définition du retard, le calendrier, les paiements partiels, les droits d'accès et les sources de données disponibles. Il distingue ce qui est nouveau de ce qui fait déjà partie d'une campagne approuvée.

Un charter de capacité indique le résultat à obtenir, les limites, les interfaces, les dépendances, les propriétaires, les critères d'acceptation et les falsificateurs. Il ne doit pas imposer chaque fonction, fichier et commit. Une telle microgestion réduirait la responsabilité opérationnelle du Controller et ferait remonter de simples défauts au niveau stratégique.

Le Planner peut exclure les fonctionnalités qui ne servent pas le premier résultat. Afficher les retards ne signifie pas automatiquement introduire des paiements en ligne, une notification par email ou un tableau de bord complexe. Ces effets nécessitent des décisions de produit distinctes.

Un bon objectif est observable. «L'administrateur peut rechercher les cotisations impayées pour une période donnée sans perdre l'historique» permet de concevoir des tests. «Rendre le backend plus professionnel» est trop vague tant qu'on n'a pas identifié une défaillance ou une capacité concrète à améliorer.

## 3. Responsabilité continue du Controller

Après autorisation, I3 planifie les tâches tactiques, implémente, exécute les tests, corrige les défauts, adapte des composants internes et prépare les candidats successifs. Le même charter peut durer plusieurs sessions et survivre à des interruptions. Un test échoué ou un problème de syntaxe ne constitue pas une invalidation stratégique.

Si la revue indépendante trouve que les données sont perdues après un redémarrage, I3 investigue le stockage, corrige la cause, ajoute une régression, reteste et soumet un nouveau candidat. Il ne crée pas une nouvelle campagne à chaque échec. Le Planner audite un terminal consolidé lorsqu'une décision stratégique réelle est possible.

Après deux retours ou plus d'une même catégorie de problème, le Controller doit rechercher la cause systémique. Une suite de petites corrections qui répare un cas tout en laissant les autres cassés n'est pas un progrès fiable. Le durcissement peut comprendre contrats, gestion des transactions, concurrence, tests négatifs et revue indépendante.

I4 peut aider sur une tâche bien délimitée, mais multiplier les agents n'améliore pas automatiquement la qualité. Les travaux en parallèle doivent respecter l'ownership des fichiers, bases, schémas et artefacts. Deux acteurs qui écrivent au même endroit sans coordination peuvent provoquer plus de conflits que de gains.

## 4. Autorisations et effets externes

Les lectures, tests locaux et corrections techniques prévues par un charter peuvent généralement être effectués par I3 dans ses permissions. Les actions irréversibles ou externes sont différentes : publier un package, envoyer un email, dépenser, exposer des données privées, supprimer une base réelle ou modifier un service de production peut nécessiter une validation explicite.

| Action | Traitement approprié |
| --- | --- |
| Lire les sources et diagnostiquer. | Travail technique en lecture seule. |
| Modifier du code dans le charter. | Autorité de I3, avec contrôles adaptés. |
| Ajouter une dépendance. | Vérifier origine, permissions, sécurité et nécessité. |
| Déployer ou publier. | Confirmer le gate de release et l'autorisation. |
| Dépenser via un fournisseur externe. | Respecter budget et consentement explicite. |
| Copier un token ou une base privée dans le chat. | À éviter ; employer le mécanisme de secrets approuvé. |
| Constater un conflit de Product State. | HOLD dépendant et réconciliation des sources. |

Un utilisateur ne devrait pas décider de chaque détail de SQL ou des options de retry. L'ingénierie doit cependant expliquer les conséquences d'une nouvelle politique de confidentialité, d'un accès public ou d'une dépense récurrente. La frontière entre produit et technique dépend de l'effet réel de la décision.

Le framework peut fournir des contrôleurs portables de référence, notamment `campaignctl.py`. Leur présence ne prouve pas qu'un fournisseur propriétaire ait authentifié un agent ou exécuté une action native. Une affirmation d'exécution réelle doit être corroborée par l'environnement ou le service concerné.

## 5. Lire un rapport d'exécution de manière critique

Un rapport utile identifie le candidat exact, l'environnement, les actions réellement effectuées, les entrées, les résultats observés, les tests, la revue et les limites. Il doit permettre au Planner d'auditer la capacité et au CLIENT de savoir ce qui est utilisable sans parcourir des milliers de lignes de logs.

Les gates restent différents : unit pour la logique isolée, integration pour les interfaces ensemble, DB/currentness pour la cohérence des données et références, semantic pour la règle métier, physical pour une exécution réelle, perceptual/human pour l'expérience jugée par une personne, release pour l'artefact publié et ses autorisations.

Une capture d'écran prouve qu'une interface a été affichée à un moment donné. Elle ne prouve pas que les données sont sauvegardées. Une réponse JSON conforme ne prouve pas qu'un utilisateur trouve la fonction. Une CI verte du starter ne certifie pas un déploiement d'application. Chaque PASS doit avoir une portée explicite.

Demandez donc : quelle version a été testée, dans quel environnement, avec quel scénario, quels résultats et quels gates restent ouverts ? Le rapport peut être court, mais ses liens doivent mener aux sources canoniques réellement examinées. Le nombre de commits ou de tokens consommés n'est pas une mesure de fonctionnalité livrée.

## 6. Git, changements locaux et continuité

Git suit les changements de fichiers, pas l'ensemble de l'autorité. Un commit n'identifie pas à lui seul la campagne, l'acteur autorisé ni la cohérence de la DB. Les documents de currentness et les enregistrements d'exécution sont nécessaires pour reconstruire les relations entre code, données, artefacts et revues.

Avant de synchroniser, inspectez les modifications locales. Une opération aveugle de nettoyage peut effacer des fichiers non intégrés ; une fusion mal préparée peut mélanger deux décisions incompatibles. Préservez les versions utiles et comparez la base commune avec les changements distants. Un nom de branche n'est pas une garantie d'identité du contenu.

Les checkpoints peuvent servir à récupérer une session interrompue sans représenter une acceptation. À l'inverse, une capacité acceptée doit pointer vers un candidat et des preuves dont l'identité reste stable. La progression s'observe par le résultat produit, les gates gagnés et les risques réduits, non par la fréquence des commits.

Les [outils de delta du dépôt](../../../../tools/repo_delta.py) permettent de limiter l'inspection aux changements pertinents. Ils ne remplacent pas le jugement sur les interfaces et n'autorisent pas la suppression de sources inconnues. Une nouvelle session doit constater le ref exact au lieu de se fier au souvenir d'un précédent agent.

## 7. Ressources, artefacts et espace disque

Un projet peut accumuler des clones, worktrees, caches, captures, fichiers audio/vidéo et builds. L'espace disque est une ressource protégée. Conservez de préférence un checkout persistant canonique par dépôt. Lorsque l'isolement de travaux concurrents le justifie, utilisez des worktrees temporaires qui partagent les objets Git et nettoyez-les une fois leur rôle terminé.

Avant de générer un artefact volumineux, vérifiez s'il existe déjà une version utilisable dont la provenance est connue. Un reviewer peut consulter le même fichier canonique par chemin et hash sans en obtenir une copie personnelle supplémentaire. Les rendus et intermédiaires sont conservés lorsqu'ils ont une valeur de preuve ou de produit, pas simplement «au cas où».

Le [protocole d'inventaire et de garbage collection](../../../34_FILE_ARTIFACT_INVENTORY_AND_GC.md) et `tools/workspace_gc.py` encadrent la suppression. Commencez par un inventaire read-only et un dry-run. N'effacez ni données humaines inconnues, ni sources, ni artefacts acceptés, ni éléments canoniques nécessaires à la reconstruction.

Le coût concerne aussi les services d'IA, le temps de calcul et les ressources réseau. Une opération techniquement facile peut entraîner des dépenses ou une exposition de données. Le Controller doit respecter le budget et les conditions d'arrêt autorisés, sans convertir une permission de test local en permission de facturation.

## 8. Coordination, concurrence et rôle du CLIENT

Lorsque plusieurs chantiers existent, chacun a un propriétaire et un périmètre de ressources. Deux équipes peuvent avancer en parallèle si leurs modifications sont indépendantes. Deux acteurs qui changent la même DB, le même schema ou le même contrat nécessitent des garanties de coordination. Le nom du projet ne suffit pas à conclure que deux actions sont sûres en concurrence.

Le MASTER OWNER peut intervenir sur les conflits d'ownership, les politiques dupliquées, la mauvaise intégration entre chantiers ou les campagnes qui restent prisonnières de faux terminaux. Il ne doit pas devenir un deuxième Planner reprenant chaque décision. La correction doit cibler la cause du dysfonctionnement systémique.

Le CLIENT confirme des règles métier, des limites de coût, des effets externes et des jugements d'expérience. Il peut servir de relais manuel entre une conversation ChatGPT et un exécuteur qui n'est pas directement accessible : recevoir un message complet, le transmettre et consulter le rapport. Ce rôle ne le transforme pas en responsable de la cohérence technique.

Les messages adressés à I3 doivent être suffisamment autonomes : objectif, références actuelles, contraintes, gates et conditions de clôture. Évitez les fragments de patch que le CLIENT devrait assembler. Le système existe pour diminuer sa charge de coordination, pas pour la déplacer dans un autre outil.

## 9. Revue indépendante du candidat exact

Avant un terminal, I3 intègre un candidat dont les sources et configurations sont identifiables. Une revue indépendante examine ce candidat précis. Si la source change ensuite de manière matérielle, les contrôles affectés doivent être renouvelés. Il n'est pas nécessaire de répéter des tests indépendants d'une partie inchangée lorsque cette indépendance est démontrable.

Le [protocole de freeze et de revue](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md) aide à structurer cette relation. Il ne prouve pas automatiquement le comportement d'une application sur un téléphone, dans un navigateur ou dans un environnement de production : l'essai physique reste nécessaire quand il fait partie du produit.

Si le reviewer relève un bug couvert par le charter, I3 corrige et représente un candidat. Si le résultat révèle une décision métier nouvelle, le Planner consulte le CLIENT. Si les témoins de currentness sont insuffisants, le terminal doit déclarer cette limite au lieu de la masquer par des tests verts.

Le but de la revue n'est pas d'interdire indéfiniment une capacité pour des détails sans importance, mais de découvrir et résoudre les risques matériels. Le Planner doit pouvoir comparer critères, preuves et impact, puis prendre une décision stratégique défendable.

## 10. Une routine quotidienne simple

En début de session, reconstruisez les sources, l'objectif, l'autorité et les blocages. Pendant l'exécution, conservez les checkpoints et vérifiez les effets importants. Avant un terminal, intégrez le candidat, exécutez les gates pertinents, obtenez la revue et rédigez un rapport traçable.

En cas d'interruption, conservez journal et identité de l'opération ; le prochain exécuteur doit reprendre sans dupliquer un effet. Un bug ordinaire revient à I3 dans la même campagne. Une modification véritable du produit revient au Planner. Une contradiction matérielle non résolue donne un HOLD spécifique pour les travaux dépendants.

À la fin de la semaine, le CLIENT doit connaître les capacités réellement utilisables, les risques restants, les décisions à prendre et les prochaines démonstrations. Si la réponse n'est qu'une liste d'activités techniques, il reste à transformer ce travail en valeur produit.

**Suite :** chapitre 04, demander une modification sans perdre le périmètre ni créer des campagnes artificielles.

## Sources et portée

- [Bootstrap et dépôt courant](../../../01_FORK_AND_BOOTSTRAP.md)
- [Protocole de reconstruction](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md)
- [Intégrité de revue et terminal](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Outil d'inspection du delta](../../../../tools/repo_delta.py)
- [Inventaire et gestion des artefacts](../../../34_FILE_ARTIFACT_INVENTORY_AND_GC.md)
- [Validation exécutable](../../../10_EXECUTABLE_VALIDATION.md)

Le framework décrit des mécanismes et des limites ; son installation ne certifie pas qu'un hôte d'IA tiers a exécuté une opération réelle.
