# Agentic SDLC — Guide de démarrage

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

Pour désactiver : enabled=false dans .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json, supprimer .github/workflows/agentic-sdlc-feedback.yml ou installer avec --no-feedback-workflow.

## Sécurité et versions

Ce code source correspond à la version 1.4.0. **Elle n'est publiée que lorsque la [release immuable v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0), son ZIP et sa somme de contrôle vérifiés sont disponibles**. La release précédente v1.3.0 reste accessible. Pour un projet nouveau ou sans gouvernance préalable, suivez le [guide de première installation v1.4](../46_V1_4_PUBLIC_START_AND_SUPPORT.md) ; pour un projet déjà gouverné, utilisez le [contrôle en lecture seule](../32_EXISTING_GOVERNED_ATTACHMENT.md), sans écraser son état. La CI portable ne certifie pas l'exécution native de Codex Desktop, les fournisseurs d'IA externes ni les effets réels.

## Langues

L'installateur détecte la langue système ou accepte --language fr. Les guides sont disponibles hors ligne. Le README de GitHub est statique : utilisez les liens de langue.

[FAQ](FAQ_fr.md) · [GitHub README](../../README.md)
