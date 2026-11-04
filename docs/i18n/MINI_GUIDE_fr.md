# ArquitecturaRepo — Mini-guide v1.4.0 (français)

Ce mini-guide couvre huit étapes (00–07) pour utiliser **v1.4.0** dans un vrai projet. C'est un **résumé pratique**, pas une traduction intégrale de l'ancien manuel espagnol v1.3, conservé dans le dépôt source. La [publication versionnée v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0) constitue la distribution de référence ; v1.3.0 reste disponible.

Ce mini-guide a été ajouté à `main` **après** la publication v1.4.0 ; le ZIP et le conteneur v1.4.0 d'origine **ne le contiennent pas**. Une future distribution hors ligne devra avoir un numéro de version distinct.

## 00 · Comprendre l'outil et ses limites

ArquitecturaRepo est une couche de pilotage **locale au dépôt** : besoins, décisions, responsabilités, état courant, campagnes, preuves et reprise après interruption. Ce n'est ni un générateur automatique d'applications ni un remplacement de Codex.

- CLIENT choisit les objectifs produit, autorise les actions sensibles et accepte l'expérience utilisateur.
- I1 coordonne plusieurs projets si nécessaire ; I2 Planner définit la stratégie, les capacités et leurs critères de validation.
- I3 Controller développe, débogue, teste, intègre et reprend les travaux dans la campagne autorisée.
- I4 est facultatif : **quatre rôles n'imposent pas quatre agents ou conversations**.

L'application peut rester privée. Le starter public n'a pas besoin de recevoir son code, ses bases de données, ses secrets ou ses conversations. Les fournisseurs de modèles externes dépendent d'autorisations distinctes ; l'installation ne donne aucun accès automatique.

## 01 · Installation prudente

Utilisez Python 3.12, testé en CI. Téléchargez l'[archive portable v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/download/v1.4.0/ArquitecturaRepo-v1.4.0-portable.zip), vérifiez sa somme `.sha256` publiée, extrayez l'archive et ouvrez un terminal **dans le dossier du framework**. Vous pouvez aussi utiliser le tag Git immuable `v1.4.0`.

Pour une application nouvelle ou existante **sans gouvernance canonique**, choisissez `SMALL` :

```bash
python "tools/scaffold_project.py" --target "../mon-projet" --profile SMALL --product-id MON_PROJET --objective "Objectif initial à confirmer" --language fr --no-feedback-workflow
```

Sous PowerShell :

```powershell
python "tools\scaffold_project.py" --target "..\mon-projet" --profile "SMALL" --product-id "MON_PROJET" --objective "Objectif initial à confirmer" --language "fr" --no-feedback-workflow
```

Le programme ajoute `.agentic-sdlc/` sans remplacer le code ou les workflows existants et refuse l'écrasement d'un contrôleur antérieur. `--no-feedback-workflow` désactive le calendrier des rapports, **pas** le générateur local. Pour désactiver tous les rapports, mettez `enabled=false` dans `.agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json`. Aucun collecteur externe n'est inclus.

Ensuite, **dans le dossier de l'application cible** :

```bash
python -m pip install -r ".agentic-sdlc/requirements-validation.txt"
python ".agentic-sdlc/tools/project_status.py" --control-root ".agentic-sdlc"
python ".agentic-sdlc/tools/discover_project.py" --project-root "."
python ".agentic-sdlc/tools/reconstruct_context.py" --root ".agentic-sdlc"
```

Sous PowerShell, utilisez les chemins entre guillemets avec `\`. L'état initial `HOLD / UNTRUSTED_CONTEXT` est **normal** : les besoins et les autorisations restent à confirmer. Si votre projet possède déjà Product State, campagnes ou contrôleur, **ne réinstallez pas par-dessus**. Consultez le [précontrôle en lecture seule](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/32_EXISTING_GOVERNED_ATTACHMENT.md). Aucune migration automatique universelle v1.2/v1.3 n'est fournie.

## 02 · Planner et adoption

Reconstituez le vrai code, les besoins, les données, les dépendances, la sécurité et les contraintes. CLIENT confirme cette base ; I2 prépare un charter de **capacité**, indiquant résultat, frontières, propriétaires, interfaces, critères de réussite, contrôles et conditions de rejet. Ne copiez jamais un état produit fictif depuis les exemples.

## 03 · Travail quotidien

Repartez du Git réel, de l'état CURRENT et des preuves, pas seulement d'un ancien chat. I3 prend en charge développement, essais, corrections et reprise dans **la même campagne autorisée**. Une panne ordinaire n'exige pas un nouveau charter. Si Git, identité, autorité, bail ou SQLite/WAL ne concordent pas, conservez `HOLD`. Le CI portable n'atteste pas l'intégration native avec Codex Desktop/Goals ou des services externes.

## 04 · Demander une modification

Décrivez le résultat visible, les contraintes et le test d'acceptation. Exemple : « Afficher les cotisations impayées sans modifier les paiements historiques ; valider sur cas payés et en retard ». I2 évalue le changement stratégique ; I3 exécute les ajustements internes déjà autorisés.

## 05 · Erreurs et reprise

- `UNTRUSTED_CONTEXT` : reconstruire la vérité du produit ; ne pas forcer le statut.
- `jsonschema` manquant : installer les dépendances du fichier `requirements-validation.txt` généré.
- `EXISTING_CONTROL_PRESERVED` : arrêter ; utiliser le parcours en lecture seule, sans `--force` ni suppression.
- Preuves Git/SQLite WAL/acteur ou bail contradictoires : suspendre toute écriture matérielle.
- Exécution interrompue : conserver journal, identité et artefacts ; reprendre la campagne existante. Le nettoyage exige une propriété vérifiée.

Pour les Issues publics, ne partagez que des étapes reproductibles et des logs expurgés, sans noms privés, chemins personnels, clés ni données confidentielles.

## 06 · Valider une capacité

Distinguez tests unitaires, intégration, cohérence DB/currentness, sémantique, exécution physique, appréciation humaine et publication. Un test vert n'est pas l'acceptation du CLIENT. Conservez la source exacte, les preuves, les responsables et la décision dans l'état canonique. Les tests synthétiques ne certifient pas une application de production.

## 07 · Exemple : club d'adhérents

1. CLIENT demande les fiches d'adhérents, les cotisations et les impayés.
2. I2 étudie les données et les droits existants et établit une capacité minimale.
3. I3 réalise adhésion → cotisation → consultation, avec tests et reprise.
4. Un calcul erroné est corrigé dans **la même** campagne.
5. CLIENT teste le parcours et accepte ou signale les défauts ; les preuves persistent.

## Références et limites

[Guide court](README_fr.md) · [FAQ](FAQ_fr.md) · [README racine](../../README.md) · [Périmètre public v1.4](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/46_V1_4_PUBLIC_START_AND_SUPPORT.md).

Ce guide ne constitue ni un audit de sécurité, ni un test d'utilisabilité indépendant, ni une preuve de meilleure performance que l'utilisation directe de Codex. La licence MIT ne couvre pas automatiquement les œuvres tierces.
