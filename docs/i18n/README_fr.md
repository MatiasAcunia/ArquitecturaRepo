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

La version stable est 1.1.0. La 1.2 reste candidate : Codex Desktop Goal, Gemini, les effets externes et les tâches multiprojets nécessitent une validation physique. Une CI verte ne prouve pas l'acceptation produit.

## Langues

L'installateur détecte la langue système ou accepte --language fr. Les guides sont disponibles hors ligne. Le README de GitHub est statique : utilisez les liens de langue.

[FAQ](FAQ_fr.md) · [GitHub README](../../README.md)
