# 05 — Erreurs, incidents et récupération

ArquitecturaRepo · Manuel d'utilisation complet · Édition v1.4 · Français

> Récupérer un projet ne signifie pas simplement faire disparaître un message d'erreur. Il faut revenir à un état **vrai, cohérent et vérifiable**, en préservant les sources, les propriétaires, les journaux de transaction et les preuves pertinentes. Un défaut ordinaire reste sous la responsabilité de I3 ; une contradiction matérielle de currentness ou d'autorité exige une autre réconciliation.

## Dans ce chapitre

1. Conserver les preuves avant de réparer
2. Pannes d'environnement, de comptes et de permissions
3. Lorsque la validation de contrôle échoue
4. Git ne sert pas à effacer les problèmes
5. Défauts répétés et causes systémiques
6. Sécurité, confidentialité et droits externes
7. Prouver la fin de l'incident
8. Trois scénarios de récupération
9. Opérations sensibles et autorisations
10. Ce qu'un test vert ne prouve pas
11. Retours d'architecture et données locales

## 1. Conserver les preuves avant de réparer

Lorsqu'une opération échoue, sauvegardez le message exact, la commande ou l'action, la date, le dépôt et worktree, le commit ou candidat concerné, ainsi que les éventuels effets partiels. Ne supprimez pas immédiatement `.agentic-sdlc/`, les fichiers de DB ou les logs. Ces données peuvent être indispensables pour comprendre la cause et reprendre sans perdre du travail.

Commencez par classer l'incident. Une dépendance Python absente, un conflit Git, une règle métier mal implémentée, un journal transactionnel incomplet, une autorisation de publication manquante et une base de données incohérente sont des problèmes différents. Le propriétaire et la démarche ne sont pas interchangeables.

| Signal | Première réponse sûre |
| --- | --- |
| Un test de la fonctionnalité échoue. | I3 conserve la reproduction et corrige dans le charter courant. |
| Un validateur rejette une référence canonique. | HOLD sur l'effet dépendant, inspection de la relation fautive. |
| Des changements Git locaux et distants divergent. | Préserver les deux et étudier les deltas. |
| Des données réelles peuvent être endommagées. | Suspendre les écritures sensibles, protéger backups, WAL et journaux. |
| Il manque le droit de publier ou de payer. | Ne pas effectuer l'effet externe. |
| Un hôte a cessé de répondre pendant une opération. | Effet inconnu ; lire l'état avant toute nouvelle tentative. |

La correction est terminée lorsqu'on a démontré le gate concerné sur le candidat courant. Supprimer une ligne de log ou modifier un champ `READY` peut produire un rapport agréable sans réparer le produit. Les investigations en lecture seule peuvent souvent continuer pendant que les écritures sensibles restent bloquées.

Le CLIENT doit connaître les conséquences de l'incident et les choix qui lui appartiennent. Il ne doit pas gérer chaque conflit de fichiers ou décider de l'algorithme de récupération. I3 assume les défauts techniques couverts par le charter et rend compte de manière vérifiable.

## 2. Pannes d'environnement, de comptes et de permissions

**Python est introuvable.** Vérifiez le chemin, l'interpréteur actif, sa version et le PATH. Installez les dépendances déclarées depuis une source fiable. Ne modifiez pas le Product State pour contourner un problème de configuration locale.

**Impossible d'accéder à GitHub.** Distinguez absence d'authentification, permissions insuffisantes, installation du connecteur, visibilité du dépôt et branche inaccessible. Un refus de lecture ne justifie pas de demander tous les droits du compte ni de copier un token en clair dans la conversation.

**L'agent travaille dans le mauvais projet.** Comparez dossier courant, remote, ref, fichiers et éventuels worktrees. Deux chemins similaires ne sont pas interchangeables. Avant d'écrire, il faut confirmer que le projet ouvert correspond réellement à celui que le CLIENT a autorisé.

**La session ou le service expire.** La fin d'un thread ne termine pas la campagne. Le nouvel acteur reconstruit Goal, charter, owner, candidate, checkpoint et effets pendants. Une réponse interrompue ne signifie pas nécessairement qu'une action externe n'a pas été exécutée.

**Permission du système refusée.** Identifiez la cible exacte et les droits requis. Ne contournez pas un contrôle de sécurité en utilisant un autre chemin ou une suppression plus large. Lorsque l'autorisation est réservée, interrompez l'effet et demandez la décision correspondante.

Les erreurs d'environnement se résolvent souvent simplement, mais le diagnostic doit précéder les mutations. Une réparation aveugle peut masquer une divergence de version ou effacer des données que le Controller aurait pu récupérer.

## 3. Lorsque la validation de contrôle échoue

Le `tools/validate_project.py` installé examine la structure et les contrats de `.agentic-sdlc/`. Il peut détecter un propriétaire dupliqué, un `CURRENT` incohérent, un candidat différent de celui revu ou une transition incomplète. Il ne prouve pas que l'application se connecte réellement à sa base, que les permissions métier fonctionnent ou que l'expérience utilisateur est satisfaisante.

Avant toute réparation, conservez le résultat, le root du contrôle, le commit actuel, les changements locaux et les témoins de DB. Identifiez si une relation est absente, périmée, contradictoire ou bloquée par une transaction. Ne modifiez pas directement les valeurs d'état pour obtenir un rapport vert.

Les mises à jour de plusieurs fichiers utilisent un [journal de récupération transactionnelle](../../../12_TRANSACTION_RECOVERY.md). Lorsque les hashes avant/après ne correspondent pas à l'effet attendu, la procédure doit préserver le conflit plutôt que de réécrire silencieusement les fichiers d'un autre acteur. Un journal pendant peut légitimement bloquer les opérations suivantes.

SQLite en mode Write-Ahead Logging ajoute une difficulté. Le fichier principal `.db` peut être en retard par rapport à l'état transactionnel courant. Un snapshot cohérent, incluant les effets pertinents du WAL, est nécessaire lorsque la currentness en dépend. Le [précontrôle des projets gouvernés](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) documente ces limites ; ce n'est pas un outil automatique de réparation de production.

Après la récupération du contrôle, vérifiez séparément le comportement physique de l'application. Un schéma JSON valide ne remplace pas une opération de lecture/écriture de DB et une preuve de DB ne remplace pas la vérification d'une interface.

## 4. Git ne sert pas à effacer les problèmes

Un conflit Git représente deux changements potentiellement valables. Ne choisissez pas mécaniquement «version locale» ou «version distante». Examinez la base commune, les différences, les owners et les décisions qui ont conduit aux modifications. Le but est d'intégrer le bon comportement, pas seulement de rendre le statut Git propre.

N'utilisez pas de reset destructif ou de suppression d'un dépôt entier pour éviter la réconciliation. Les modifications non intégrées peuvent appartenir à l'utilisateur ou à une campagne active. Préservez-les tant que leur provenance et leur pertinence n'ont pas été établies.

Les outils de [différentiel de source](../../../../tools/repo_delta.py) et d'[inventaire/gestion des artefacts](../../../34_FILE_ARTIFACT_INVENTORY_AND_GC.md) aident à comprendre l'espace de travail. Ils ne permettent pas d'effacer arbitrairement du code, des données inconnues, des assets acceptés ou des éléments de preuve canoniques. Une opération de nettoyage commence par un inventaire et un dry-run.

Les commits ne sont pas des certificats d'identité d'acteur. La preuve qu'un agent avait l'autorité pour écrire doit provenir des surfaces de contrôle pertinentes, pas seulement d'un nom d'auteur Git. Une branche qui avance ne prouve pas non plus que les revues ou les témoins de DB correspondent au nouveau candidat.

Lorsqu'un fichier change après une revue favorable, les contrôles concernés doivent être renouvelés. La récupération ne doit jamais transformer une approbation d'ancienne version en acceptation implicite d'une autre source.

## 5. Défauts répétés et causes systémiques

Un défaut déjà couvert par le charter appartient au Controller. Tests échoués, migration en périmètre, refactorisation interne, bug découvert par un réviseur ou interruption du runtime ne nécessitent pas une nouvelle campagne ni une nouvelle analyse du Planner.

Si le même type de panne réapparaît dans plusieurs candidats, le Controller doit arrêter les microcorrections successives. Il faut examiner le sous-système : transactions, contrats, concurrence, données, tests négatifs, limites d'intégration et causes de la régression. Un durcissement complet avec revue indépendante peut être nécessaire.

Prenons une désactivation de membre qui supprime ses paiements. Corriger un seul cas sans tester les paiements partiels ou les interactions avec d'autres tables peut laisser le problème vivant. Une solution causale examine les relations de persistance et démontre la conservation du bon historique après un redémarrage.

Le Planner revient lorsque I3 présente un terminal stratégique ou lorsqu'une preuve nouvelle invalide réellement le charter. La difficulté du bug n'est pas, à elle seule, une modification de la stratégie. Cette frontière protège le CLIENT de cycles de planification sans résultat produit.

À l'échelle d'un portefeuille, le MASTER OWNER doit aussi détecter les défauts systémiques : polices dupliquées, Controllers qui n'assument pas les corrections, confusion des responsabilités et problèmes répétés d'intégration entre chantiers. La solution doit viser le mécanisme responsable, pas ajouter une nouvelle cérémonie à chaque incident.

## 6. Sécurité, confidentialité et droits externes

Les logs et rapports publics doivent être expurgés. N'insérez pas de tokens, mots de passe, données de membres, chemins privés, bases complètes ou transcriptions de conversations dans des issues accessibles à tous. Une fixture fictive peut souvent reproduire le défaut sans exposer les personnes concernées.

Le starter n'autorise pas l'envoi du code vers un fournisseur externe. Les modèles et connecteurs restent facultatifs et nécessitent une configuration et des permissions spécifiques. Une solution qui exige facturation, publication ou transmission de données doit obtenir l'autorisation avant de réaliser l'effet.

Une licence libre du framework ne couvre pas automatiquement des ressources tierces. Images, polices, musique et datasets ont leurs propres droits. Évaluez-les de manière proportionnée à l'usage réel, sans présumer qu'une permission existe ni imposer un contrôle documentaire sans lien avec le risque.

Une sauvegarde de production peut contenir des informations sensibles. La rendre publique pour simplifier un test n'est pas acceptable. Les essais doivent protéger confidentialité, intégrité et accès. L'effacement, la restauration et la modification de données sont des actions distinctes qui demandent des contrôles différents.

## 7. Prouver la fin de l'incident

Une réparation terminée doit pouvoir être reproduite. Le rapport indique l'incident, la source et le candidat, la cause, la correction, les tests exécutés, l'état persistant, la revue et les limites restantes. Le message d'erreur ne doit pas simplement disparaître ; le comportement attendu doit fonctionner dans l'environnement pertinent.

Pour une migration, vérifiez l'état après écriture et, si nécessaire, après redémarrage. Pour une interface, ouvrez réellement l'écran avec des données appropriées. Pour un effet externe interrompu, lisez l'état distant avant de réessayer afin d'éviter un doublon. La récupération doit respecter idempotence et autorisation.

Si la correction modifie le candidat après la revue, renouvelez les gates affectés. I3 peut produire un terminal technique avec des preuves, mais ne peut pas accorder de lui-même le consentement du CLIENT à une publication ou à une qualité subjective.

Un compte rendu de récupération doit être court mais reconstructible. Un autre ingénieur doit pouvoir identifier les fichiers, l'environnement et la prochaine action sans lire la conversation entière.

## 8. Trois scénarios de récupération

**Scénario A — Installation interrompue.** Le scaffold a écrit certains fichiers avant la fermeture du terminal. Inspectez la destination, gardez les données existantes et comparez l'état avec le contrat. Utilisez la route de récupération sûre ; n'effacez pas toute l'application pour relancer l'installateur.

**Scénario B — Paiement au résultat inconnu.** Une opération reçoit un timeout après l'envoi. Le Controller doit déterminer si un paiement a réellement été enregistré en consultant un identifiant d'opération ou un état transactionnel. Répéter aveuglément peut provoquer un double effet. Si la preuve manque, gardez un HOLD sur la répétition dangereuse.

**Scénario C — Revue périmée.** Le réviseur a approuvé A, mais le code a été modifié pour B. La validation de A n'accepte pas B. I3 identifie les différences, répète les contrôles concernés et obtient une revue du candidat intégré exact. Les preuves non affectées peuvent être conservées si leur indépendance est justifiée.

Ces scénarios ont des causes différentes : effet partiel, idempotence et identité du candidat. Aucun ne nécessite automatiquement une campagne stratégique nouvelle. Chacun exige une preuve cohérente et un propriétaire opérationnel clair.

## 9. Opérations sensibles et autorisations

Avant une opération à risque, déterminez le système cible, le propriétaire de la ressource, les conséquences, la réversibilité, les données exposées, les moyens de retour arrière et les permissions réelles. Une action automatisable n'est pas nécessairement autorisée.

| Opération | Limite à respecter |
| --- | --- |
| Inspecter les sources et réaliser des tests locaux. | Permissions techniques et périmètre courant. |
| Modifier du code sous charter. | Ownership, tests et revue de I3. |
| Changer des données ou un schéma de production. | Preflight, migration, sauvegarde et preuve de readback. |
| Supprimer des fichiers ou bases. | Cible exacte et autorisation matérielle si nécessaire. |
| Envoyer des données à des tiers. | Confidentialité, licence et consentement spécifique. |
| Publier un artefact ou une release. | Gate de distribution et autorité adéquate. |

Si une autorisation manque, arrêtez l'effet et demandez-la. Ne cherchez pas une voie détournée pour contourner le refus. Si la difficulté se limite à un problème technique déjà autorisé, I3 le résout sans transférer au CLIENT les décisions internes d'ingénierie.

La récupération automatique suit les mêmes principes. Un script de nettoyage ne doit pas supprimer un répertoire large dont l'ownership est inconnu. Un retry doit être sûr quant à ses effets. La vitesse ne justifie pas de perdre la preuve de ce qui a été modifié.

## 10. Ce qu'un test vert ne prouve pas

La validation de structure du starter vérifie des contrats documentaires et des références. Un test de scaffold vérifie l'installation en environnement contrôlé. Un scénario synthétique de récupération prouve un comportement limité du mécanisme testé. Aucun de ces tests ne certifie automatiquement un produit tiers en production.

Une fonction unitaire peut réussir tandis que l'API est mal connectée. L'intégration peut passer avec une DB qui ne correspond pas à la source actuelle. Une interface peut s'ouvrir et rester inutilisable pour son public. Les gates de DB/currentness, semantic, physical et perceptual doivent être distingués.

Une publication exige aussi de vérifier l'artefact exact, sa version, son checksum et son accessibilité sur le service visé. Un ZIP construit localement et une tag Git ne prouvent pas que tous les assets d'une release ont réellement été publiés. L'acceptation doit nommer le gate et sa portée.

Quand un gate n'a pas de sens pour la capacité, expliquez pourquoi. Quand il est requis et non exécuté, ne le remplacez pas par un test moins pertinent qui a déjà réussi. Le but est de vérifier les risques réels sans recherche interminable de défauts accessoires.

## 11. Retours d'architecture et données locales

En v1.4, un générateur local de rapports restreints de métadonnées peut être actif par défaut. Un workflow mensuel, lorsqu'il est installé, enregistre les résultats dans les propres artefacts GitHub Actions du projet. La distribution publique ne contient pas d'endpoint de collecte externe.

L'option `--no-feedback-workflow` désactive l'ordonnancement, pas le générateur local. Pour arrêter tous les rapports, réglez `enabled=false` dans `.agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json`. Consultez la [politique de confidentialité](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md) et le workflow exact avant d'autoriser toute transmission.

Un rapport de bogue du framework peut indiquer la version, la plateforme, les étapes de reproduction, des données synthétiques et des messages expurgés. Il n'a pas besoin du code privé ni des conversations de l'utilisateur. Les informations nécessaires à la correction sont différentes de celles qui permettraient d'identifier une personne.

La récupération réussie se reconnaît au fait qu'un nouveau travailleur peut identifier l'état courant, le résultat observé, les limites et la prochaine action. Si seule l'ancienne conversation donne ces réponses, l'état durable reste incomplet.

**Suite :** chapitre 06, clôture des capacités et acceptation avec des preuves exactes.

## Sources et portée

- [Récupération des transactions](../../../12_TRANSACTION_RECOVERY.md)
- [Précontrôle des projets déjà gouvernés](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Outil d'inspection de source](../../../../tools/repo_delta.py)
- [Inventaire et suppression sûre](../../../34_FILE_ARTIFACT_INVENTORY_AND_GC.md)
- [Confidentialité et feedback](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md)
- [Support public v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)

Les mécanismes précis de récupération dépendent du projet et des permissions. Aucun exemple de ce chapitre n'autorise la destruction d'un état réel.
