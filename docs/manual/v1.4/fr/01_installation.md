# 01 — Installation et configuration

ArquitecturaRepo · Manuel d'utilisation complet · Édition v1.4 · Français

> Installer le starter crée une première couche de coordination ; **cela n'adopte pas automatiquement l'application** et ne démontre pas qu'un produit fonctionne. Les commandes suivent le [guide public v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md). L'état initial `HOLD / UNTRUSTED_CONTEXT` est normal tant que les exigences, les sources et les responsabilités ne sont pas établies.

## Dans ce chapitre

1. Environnement et comptes
2. Starter, fork et application : trois emplacements distincts
3. Vérifier les chemins avant toute écriture
4. Choisir un profil proportionné
5. Créer la couche de coordination
6. Valider sans inventer une acceptation
7. La prochaine étape est la découverte du produit
8. Avant de recommencer une installation
9. Du scaffold à une adoption réelle
10. Connexions, permissions et confidentialité
11. Diagnostiquer sans détruire le contexte

## 1. Environnement et comptes

Le parcours portable v1.4 repose sur Python 3.12, un accès aux fichiers, et idéalement Git. Python 3.12 est la version testée par la CI de cette release. Un éditeur de code peut faciliter l'inspection, mais une connexion à un fournisseur d'IA ou à un environnement de développement particulier n'est pas nécessaire pour créer et vérifier la couche de contrôle.

Sous Windows, ouvrez PowerShell et vérifiez les exécutables disponibles. Les exemples sont donnés avec des guillemets pour que les chemins contenant des espaces restent explicites :

```powershell
& "python" --version
& "python" -m pip --version
& "git" --version
```

Si une commande n'existe pas, vérifiez l'installation, la variable PATH et le terminal utilisé. Une version de Python ouverte par un éditeur peut être différente de celle du shell. Il est préférable de résoudre le problème d'environnement plutôt que de modifier un état de projet pour obtenir artificiellement un contrôle vert.

Sur Linux ou macOS, la commande peut être `python3`. Vérifiez qu'elle désigne l'interpréteur compatible et utilisez les séparateurs de chemins attendus par votre shell. Le nom d'un script présent dans l'archive ne doit pas être deviné : consultez le dépôt et l'aide de la version réellement téléchargée.

GitHub facilite la conservation des décisions et du code, mais il ne faut pas donner plus de permissions que nécessaire. Lire un dépôt, créer un commit, modifier une branche protégée, publier une release et accéder à des données privées sont des opérations différentes. L'installation du starter ne vous donne aucune de ces autorisations automatiquement.

## 2. Starter, fork et application : trois emplacements distincts

Le dépôt ArquitecturaRepo contient le framework de coordination : scripts, protocoles, schémas, exemples et documentation. Un fork peut servir de copie personnelle du framework. Le projet de destination est autre chose : l'application réelle que vous développez, avec son propre code, sa base, ses utilisateurs et ses tests.

Le scaffold part de la source du framework et crée `.agentic-sdlc/` dans le dossier de destination lorsqu'aucun contrôle canonique incompatible n'existe. Il ne transforme pas par magie l'exemple synthétique en application et ne doit pas écraser le code déjà présent. Il ajoute des structures de coordination pour guider les étapes suivantes.

| Emplacement | Fonction |
| --- | --- |
| `ArquitecturaRepo/` | Source du starter, installateur, tests et guides. |
| Fork du starter | Copie versionnée et éventuellement personnalisée. |
| `mon-projet/` | Code et environnement de votre application. |
| `mon-projet/.agentic-sdlc/` | État et contrats de coordination propres à ce projet. |

Une confusion classique consiste à lancer un agent dans le dépôt du starter en pensant qu'il travaille déjà sur l'application. Le premier dépôt peut être parfaitement validé alors que le second n'a jamais été ouvert. Le rapport d'exécution doit identifier les deux chemins et expliquer quelle opération a réellement été effectuée.

Les fixtures fournies pour les tests sont synthétiques. Elles ne possèdent pas les exigences ni les autorisations de votre produit. Ne copiez pas leur Product State ou leur base de données en pensant accélérer l'adoption d'un projet réel.

## 3. Vérifier les chemins avant toute écriture

Avant d'installer, identifiez le dossier courant et le répertoire cible. À la racine du starter v1.4, affichez l'aide du script :

```powershell
& "python" "tools\scaffold_project.py" --help
```

Cette action est en lecture seule. Elle permet de vérifier la version et les options disponibles. Si le script n'est pas trouvé, il faut d'abord savoir dans quel dépôt on se trouve et quelle archive a été extraite. Copier un script d'une version différente dans un projet au hasard n'est pas une réparation fiable.

Un chemin relatif comme `"..\mon-projet"` désigne un dossier voisin, pas un emplacement universel. Le programme doit pouvoir distinguer la source de l'installateur, la destination, les fichiers existants et les limites des chemins liés. Examinez les répertoires avant d'utiliser des commandes capables de créer ou modifier des fichiers.

Pour une installation reproductible, téléchargez le [GitHub Release v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0) et vérifiez le checksum SHA-256 du ZIP portable. Un checkout du tag est également une source versionnée. En revanche, `main` évolue : les guides ajoutés plus tard ne sont pas nécessairement contenus dans l'archive v1.4.0 déjà publiée.

Si une application possède déjà `.agentic-sdlc/`, Product State, campagnes ou données canoniques, arrêtez l'installation générique. Le [précontrôle en lecture seule des projets gouvernés](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) existe précisément pour éviter d'écraser cette autorité.

## 4. Choisir un profil proportionné

ArquitecturaRepo propose six profils. Ils orientent les familles de contrôles, sans créer des autorisations ni garantir la réussite de l'application :

| Profil | Quand l'envisager |
| --- | --- |
| `SMALL` | Petit produit dont les données et risques restent modestes. |
| `STATEFUL` | Données persistantes, utilisateurs, schémas, sauvegardes et récupération. |
| `ARTIFACT_HEAVY` | Nombreux fichiers, rendus coûteux, provenance, licences et réutilisation. |
| `MULTI_WORKSTREAM` | Plusieurs chantiers alimentent le même produit final. |
| `MULTI_PRODUCT` | Plusieurs produits distincts partagent des ressources ou politiques. |
| `HIGH_CONSEQUENCE` | Risques matériels pour la sécurité, la confidentialité ou l'intégrité. |

Un premier outil sans données critiques peut utiliser `SMALL`. Une application de club qui conserve cotisations et membres pourrait justifier `STATEFUL`. Un pipeline audiovisuel avec de nombreux médias peut avoir besoin de traçabilité et de contrôle des ressources. Le profil doit correspondre aux besoins réels ; il ne s'agit ni d'une médaille ni d'une invitation à multiplier les agents.

La [documentation des profils](../../../06_SCALING_PROFILES.md) et des [modes de projet](../../../27_PROJECT_MODES_AND_STACK_SELECTION.md) explique leurs choix. Un profil n'oblige pas à héberger des microservices, à prendre un abonnement ou à installer un modèle. Les décisions sur le stack et les coûts seront confirmées dans l'adoption.

## 5. Créer la couche de coordination

Dans le dossier du starter, sous PowerShell, créez un contrôle initial pour un projet nouveau et non gouverné :

```powershell
& "python" "tools\scaffold_project.py" --target "..\mon-projet" --profile "SMALL" --product-id "MON_PROJET" --objective "Objectif initial à confirmer" --language "fr" --no-feedback-workflow
```

Pour un exemple fictif de club avec données persistantes, on pourrait utiliser :

```powershell
& "python" "tools\scaffold_project.py" --target "..\club-app" --profile "STATEFUL" --product-id "CLUB_GESTION" --objective "Gestion fictive des membres et cotisations" --language "fr" --no-feedback-workflow
```

Adaptez chemin, identifiant et objectif au projet autorisé. Sous un shell Unix, utilisez `"tools/scaffold_project.py"` et `"../mon-projet"` avec les séparateurs appropriés. L'installateur doit préserver le code de l'application et refuser les écrasements d'une gouvernance canonique préexistante.

L'état initial attendu est `HOLD / UNTRUSTED_CONTEXT`. Le framework n'a pas encore établi quelles sont les exigences validées, la source actuelle, le propriétaire du Product State ni les campagnes approuvées. Changer un champ JSON pour afficher `READY` ne rendrait pas ces informations vraies.

L'option `--with-runtime` peut ajouter un runtime portable de référence, mais elle n'authentifie aucun fournisseur externe et ne lance pas automatiquement Codex Desktop. `--no-feedback-workflow` évite l'installation du planificateur mensuel de rapport, sans désactiver nécessairement le générateur local de métadonnées. Les deux mécanismes ont des réglages distincts.

## 6. Valider sans inventer une acceptation

Une fois la couche créée, placez-vous dans le dossier de **l'application cible**. Exécutez les commandes de diagnostic de l'installation v1.4 :

```powershell
& "python" -m pip install -r ".agentic-sdlc\requirements-validation.txt"
& "python" ".agentic-sdlc\tools\project_status.py" --control-root ".agentic-sdlc"
& "python" ".agentic-sdlc\tools\discover_project.py" --project-root "."
& "python" ".agentic-sdlc\tools\reconstruct_context.py" --root ".agentic-sdlc"
```

Le premier commande installe les dépendances locales déclarées. `project_status.py` inspecte le contrôle actuel. `discover_project.py` examine des métadonnées et des hashes de fichiers dans le périmètre autorisé, sans transmettre le contenu au mainteneur. `reconstruct_context.py` vérifie ce qu'une nouvelle session peut reconstruire à partir des surfaces durables.

Le résultat peut rester en HOLD si le baseline n'a pas été adopté. C'est un résultat correct ; il indique que des décisions ou des témoins de source manquent. Le validateur de contrats ne démontre pas à lui seul que le frontend s'ouvre, que la DB contient les bons enregistrements ou que l'interface est compréhensible.

Vérifiez trois points : la couche se trouve au bon endroit, les anciens fichiers de l'application ont été préservés et les résultats de diagnostic restent disponibles pour une prochaine session. Conservez les erreurs exactes. Si une dépendance manque, installez le fichier `requirements-validation.txt` déclaré plutôt que d'altérer Product State.

Le statut de cette étape est «scaffold installé et inspecté», pas «produit prêt». L'adoption doit encore relier le contrôle générique au code réel, aux données et aux décisions du CLIENT.

## 7. La prochaine étape est la découverte du produit

Le Planner examine le produit : qui l'utilisera, quelles règles sont déjà confirmées, quelles données existent, quelle partie du code fonctionne et quel résultat doit être livré d'abord. Les [instructions d'installation et d'adaptation](../../../../prompts/INSTALL_THIS_SDLC.md), le [parcours de découverte](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md) et le [contrat d'adoption](../../../16_TRANSFER_ADOPTION.md) donnent les références correspondantes.

Il faut séparer les faits du code des décisions de produit. Une table `users` ne prouve pas que tout utilisateur peut être supprimé. Une interface de paiement ne prouve pas qu'une intégration externe est autorisée. Le Planner confronte les hypothèses à la source et demande au CLIENT les décisions qui ne peuvent pas être prises par l'ingénierie.

Une adoption complète comprend une spécification examinée, un preflight, des sources et propriétaires cohérents, puis une reconstruction de contexte frais. C'est seulement après ces gates qu'une campagne matérielle peut recevoir son charter. Installer puis programmer immédiatement sans connaître le baseline risquerait de construire une fonctionnalité hors sujet.

La durée du discovery doit rester proportionnée. Un prototype simple peut avoir un premier objectif confirmé rapidement. Un système exposé sur internet avec données sensibles nécessite une exploration plus approfondie des interfaces, de la sécurité, de la récupération et des coûts.

## 8. Avant de recommencer une installation

Si `.agentic-sdlc/` existe déjà, inspectez-le avant de réessayer. Il peut contenir une autorité active, un journal de transition, un Goal, des références de DB et des artefacts nécessaires à la récupération. Une nouvelle installation par-dessus peut effacer des informations que le contrôleur aurait dû conserver.

Ne supprimez pas le projet pour «faire fonctionner le tutoriel». Ne contournez pas un refus de préservation avec une option de force. Pour un projet déjà gouverné, le bon chemin commence par un attachment de lecture et une décision explicite sur les migrations éventuelles. Ce chemin n'est pas un upgrade universel et automatique de v1.2/v1.3.

En cas d'interruption, une opération peut avoir produit un effet partiel. Il faut lire l'état réellement présent avant de répéter. Un journal inachevé ne doit pas être effacé aveuglément ; un fichier de contrôle ne doit pas être remplacé par une version vierge simplement parce que la console a échoué.

Un incident d'environnement peut être corrigé par l'ingénierie sans repasser par toute la stratégie. En revanche, deux contrôleurs qui revendiquent la même autorité ou une source de vérité conflictuelle peuvent exiger une réconciliation avec le propriétaire approprié.

## 9. Du scaffold à une adoption réelle

Le chemin complet comprend la découverte du code, la confirmation des besoins, le baseline de produit, le baseline technique, les jalons de livraison, la spécification d'adoption, le preflight, la promotion cohérente des références et le test de contexte frais. Chaque étape apporte des faits nécessaires à la suivante.

Le baseline technique identifie versions de code, dépendances, DB, environnement, réseau, tests et risques. Le baseline de produit identifie comportements, utilisateurs, exclusions et critères de validation. Aucun des deux ne remplace l'autre. Le Planner doit les relier sans inventer que l'application remplit déjà les exigences.

Les dépendances de capacités déterminent l'ordre des campagnes. Un club ne doit pas implémenter l'éligibilité des inscriptions à partir d'un statut de cotisation non défini. Inversement, des travaux réellement indépendants peuvent avancer en parallèle si les fichiers, données et permissions ne créent pas de risque d'interférence.

Le CLIENT peut rester concentré sur les choix fonctionnels et la validation des résultats. L'ingénierie gère les schémas, leases, checkpoints, retries et migrations. Le système échoue si l'utilisateur doit superviser manuellement chaque détail pour éviter des incohérences entre agents.

## 10. Connexions, permissions et confidentialité

Les connecteurs GitHub, modèles d'IA, services cloud et bases de données ne deviennent actifs que si l'environnement dispose des autorisations correspondantes. Le starter public ne contient pas de jetons. Une erreur d'authentification doit être diagnostiquée dans le périmètre concerné, sans demander des secrets en clair ni élargir aveuglément les droits.

Le générateur local de retours d'architecture manipule des métadonnées restreintes. Selon l'installation, un workflow périodique peut enregistrer des rapports dans les propres artefacts GitHub Actions du projet. Aucun endpoint de collecte externe n'est livré dans la distribution publique. `--no-feedback-workflow` désactive l'ordonnancement ; pour arrêter toute génération, réglez `enabled=false` dans le fichier local de configuration du feedback.

Consultez la [politique de confidentialité et de feedback](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md) avant d'autoriser des effets sortants. Les rapports publics de bogues doivent utiliser des données fictives et des logs expurgés. N'envoyez pas les noms des clients, bases privées, chemins personnels, tokens ou conversations à un issue public.

La licence MIT du starter n'accorde pas automatiquement les droits sur les images, musiques, polices, datasets ou services tiers utilisés dans une application. Les droits réels doivent être vérifiés de manière raisonnable selon l'usage, sans généraliser des permissions inexistantes.

## 11. Diagnostiquer sans détruire le contexte

Si Python n'est pas reconnu, vérifiez l'exécutable. Si `jsonschema` manque, installez les dépendances déclarées. Si un chemin est introuvable, vérifiez la racine courante. Si le scaffold refuse d'écraser un contrôle existant, arrêtez l'installation générique. Si la DB ou le Product State est incohérent, conservez les références et cherchez la cause.

Un problème de Git doit être traité en préservant les modifications locales et les versions distantes. Une base SQLite/WAL nécessite un témoin cohérent. Une action interrompue exige un readback avant un retry. Le [chapitre 05](05_errors_and_recovery.md) détaille la récupération, les autorisations et les preuves de sortie d'incident.

Le compte rendu d'installation doit identifier source exacte, chemin de destination, profil, commandes, résultats de validation et limites ouvertes. Il ne doit pas annoncer que l'application est développée, publiée ou acceptée lorsque seul le scaffold a été créé.

**Suite :** chapitre 02, le Planner, la découverte et l'adoption d'un projet réel.

## Sources et portée

- [Guide public v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Profils](../../../06_SCALING_PROFILES.md)
- [Transfert et adoption](../../../16_TRANSFER_ADOPTION.md)
- [Précontrôle des projets gouvernés](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Confidentialité et feedback](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md)
- [Script d'installation](../../../../tools/scaffold_project.py)

Ces commandes et exemples n'autorisent pas le remplacement d'un système existant ni la facturation ou le déploiement d'un service externe.
