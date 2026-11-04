# Agentic SDLC — Guide de démarrage

[Mini-guide v1.4](MINI_GUIDE_fr.md) · [FAQ](FAQ_fr.md)

Le [manuel français complet v1.4 en huit chapitres](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/v1.4/fr/README.md) est disponible dans le dépôt source, avec un [PDF de 57 pages](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/output/pdf/ArquitecturaRepo_Manuel_Complet_v1.4_FR.pdf). Le [manuel espagnol historique v1.3](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/ES/README.md) est conservé séparément. L'archive v1.4.0 a été publiée avant ces documents et ne les contient pas. Ce guide et le miniguide sont courts ; consultez le livre complet pour les détails et le [guide v1.4](../46_V1_4_PUBLIC_START_AND_SUPPORT.md) pour les commandes actuelles.

Une architecture réutilisable, fondée sur le dépôt, pour le développement logiciel avec des agents. Elle fournit des rôles, un état durable, la planification, la reprise et la vérification. Elle ne construit pas automatiquement tout logiciel et ne remplace pas les décisions du responsable produit.

## Installer dans un projet

Choisissez le profil le plus simple adapté. Commencez par une découverte en lecture seule ; ne copiez pas le Product State des exemples. Un nouveau projet démarre en HOLD / UNTRUSTED_CONTEXT.

```bash
python tools/scaffold_project.py --target "../my-project" --profile SMALL --product-id EXAMPLE --language auto
```

## Rôles et responsabilités

Le CLIENT définit le produit et autorise les actions sensibles ; I2 gère la stratégie et l'acceptation ; I3 réalise l'ingénierie et la reprise dans la campagne ; I4 est facultatif pour les consultations limitées et les preuves indépendantes. Quatre rôles n'imposent pas quatre processus.

## Confidentialité et rapport mensuel

Par défaut, un petit rapport mensuel de métadonnées est conservé dans les artifacts GitHub Actions du projet. Il aide à améliorer la structure du starter et à classer les problèmes. Il n'est pas envoyé automatiquement au mainteneur. Il ne contient ni code, ni conversations, ni noms de projets, ni chemins, ni identifiants, ni secrets.

Pour arrêter tous les rapports, utilisez enabled=false dans .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json. Supprimer .github/workflows/agentic-sdlc-feedback.yml ou installer avec --no-feedback-workflow désactive seulement la programmation, pas le générateur local.

## Sécurité et versions

**La v1.4.0 a été publiée** sous forme de [release versionnée avec archive ZIP portable et somme SHA-256](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0). Vérifiez les fichiers téléchargés avant installation ; la branche `main` peut contenir des changements de documentation ultérieurs et ne constitue pas l'archive publiée. La release précédente v1.3.0 reste accessible. Pour un projet nouveau ou sans gouvernance préalable, suivez le [guide de première installation v1.4](../46_V1_4_PUBLIC_START_AND_SUPPORT.md) ; pour un projet déjà gouverné, utilisez le [contrôle en lecture seule](../32_EXISTING_GOVERNED_ATTACHMENT.md), sans écraser son état. La CI portable ne certifie pas l'exécution native de Codex Desktop, les fournisseurs d'IA externes ni les effets réels.

## Langues

L'installateur détecte la langue système ou accepte --language fr. Les guides sont disponibles hors ligne. Le README de GitHub est statique : utilisez les liens de langue.

[Mini-guide v1.4](MINI_GUIDE_fr.md) · [FAQ](FAQ_fr.md) · [GitHub README](../../README.md)
