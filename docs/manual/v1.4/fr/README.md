# ArquitecturaRepo — Manuel complet d'utilisation, v1.4 (Français)

**Huit chapitres détaillés · édition fondée sur les sources v1.4.**

Ce livre est distinct du [miniguide français](../../../i18n/MINI_GUIDE_fr.md) et de la [FAQ](../../../i18n/FAQ_fr.md), qui sont des introductions plus courtes. Il reprend la structure d'apprentissage du [manuel historique espagnol v1.3](../../ES/README.md) et actualise les références, les limites et les commandes pour v1.4. L'édition historique reste intacte.

## Table des matières

| Chapitre | À consulter pour |
| --- | --- |
| [00 — Avant de commencer](00_before_you_begin.md) | Objectif, rôles, preuves et limites. |
| [01 — Installation](01_installation.md) | Profils, scaffold, vérifications et HOLD initial. |
| [02 — Planner et adoption](02_planner_and_adoption.md) | Découverte, exigences, baseline et premier charter. |
| [03 — Fonctionnement quotidien](03_daily_operation.md) | Currentness, Git, exécution, revues et continuité. |
| [04 — Demander des changements](04_requesting_changes.md) | Règles nouvelles, bogues, priorités et choix humains. |
| [05 — Erreurs et récupération](05_errors_and_recovery.md) | Préservation, transactions, DB/WAL, sécurité et incidents. |
| [06 — Clôture et acceptation](06_closing_capabilities.md) | Candidat exact, gates, décision humaine et règle d'arrêt. |
| [07 — Exemple guidé d'un club](07_worked_club_example.md) | Parcours fictif depuis la découverte jusqu'aux preuves et à la récupération. |

## Quel document utiliser ?

1. Pour un premier essai, utilisez le [miniguide](../../../i18n/MINI_GUIDE_fr.md) et le [guide d'installation public v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md).
2. Pour comprendre la coordination et les preuves, lisez ces huit chapitres complets.
3. Pour une installation reproductible, utilisez le [GitHub Release v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0) avec son checksum et son manifest. La branche `main` comporte des documents ajoutés après la publication du ZIP ; ils ne figurent **pas automatiquement dans l'archive v1.4.0**.
4. Pour un produit réel, ses exigences confirmées, son code, sa DB, son Product State et ses preuves actuelles priment sur les exemples du livre.

Le framework est indépendant d'un fournisseur d'IA. Ce manuel n'installe pas d'LLM et n'autorise ni dépense, ni publication, ni déploiement externe. L'application de club décrite est pédagogique et n'est pas un produit déjà livré.

## Éditions et portée

- **Français v1.4 :** ces huit chapitres détaillés et leur PDF.
- **Sept autres langues v1.4 :** éditions longues indépendantes, avec leurs propres sources et PDF. L'[index canonique](../../../../README.md) référence les huit éditions sans recopier une liste susceptible de devenir obsolète.
- **Espagnol v1.3 :** édition historique conservée, sans réécriture rétroactive.
- **Miniguides v1.4 :** huit résumés pratiques distincts, disponibles dans les langues de l'installateur.

La pagination dépend du format et de la typographie du PDF. L'ordre des huit chapitres suit le parcours original ; les légendes de figures anciennes ne sont pas présentées comme des illustrations récupérées lorsqu'aucune image source n'est disponible.

## Sources et corrections

- [Démarrage et support v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Notes de release et mises à niveau](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)
- [Transfert et adoption](../../../16_TRANSFER_ADOPTION.md)
- [FAQ française](../../../i18n/FAQ_fr.md)

Un lien cassé, une commande d'une ancienne version ou une affirmation non vérifiée constituent des défauts de documentation. Il faut les corriger avec les références réelles, sans transformer l'historique en preuve de fonctionnalités futures.
