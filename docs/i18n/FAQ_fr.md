# Agentic SDLC FAQ (fr)

[FR guide](README_fr.md) · [Main README](../../README.md)

### 1. Qu'est-ce qu'Agentic SDLC ?

Une architecture réutilisable pour organiser le développement logiciel avec des agents. Ce n'est pas un constructeur automatique de n'importe quelle application.

### 2. Comment démarrer ?

Forkez ou inspectez le dépôt, commencez par une découverte en lecture seule, choisissez le profil minimal et suivez le prompt d'installation. Le scaffold démarre en HOLD.

### 3. Peut-on l'adopter dans un dépôt existant ?

Oui. Reconstituez d'abord le code, les données et les autorisations réels. Ne remplacez pas les fichiers applicatifs et ne prenez pas les exemples pour l'état canonique.

### 4. Quatre rôles exigent-ils quatre modèles ?

Non. CLIENT, Planner I2, Campaign Lead I3 et spécialistes I4 définissent des responsabilités, pas un nombre fixe de processus.

### 5. Qui autorise les changements sensibles ?

Le CLIENT conserve les décisions produit, l'acceptation subjective, la publication, les coûts et les données sensibles. I3 ne peut pas inventer ces autorisations.

### 6. Les Goals et Codex Desktop sont-ils intégrés ?

Pas encore. La v1.2 contient des contrôles facultatifs Goal/Plan, mais l'intégration physique à chaque invocation doit être prouvée.

### 7. Gemini est-il obligatoire ou payant par défaut ?

Non. La voie I4 reste désactivée tant que consentement, identifiants, quota et confidentialité ne sont pas vérifiés. Aucun envoi automatique de code privé.

### 8. Peut-il relancer ou effacer mes conversations Codex ?

Pas à lui seul. Codex Daily Control 2.0.2 est une référence séparée, sans adaptateur hôte accepté dans la v1.2.

### 9. Quel retour d'information est activé ?

Un petit rapport mensuel de métadonnées conservé dans les artifacts GitHub Actions de votre projet. Il aide à améliorer le starter, sans transmission externe automatique.

### 10. Quelles données sont exclues ?

Code, conversations, noms des dépôts/projets, chemins, secrets, identifiants personnels, exigences, SHA et texte libre non contrôlé.

### 11. Comment changer de langue ou désactiver le feedback ?

Utilisez --language auto|en|es|pt|fr|de|it|ja|zh. Pour désactiver : enabled=false ou --no-feedback-workflow. Le README GitHub reste statique.

### 12. Quels tests et comment signaler une erreur ?

1.1.0 est stable ; v1.2 reste candidate avant validation physique indépendante. Ouvrez une Issue avec étapes reproductibles et journaux expurgés. Le contenu original est sous MIT.

---

[FR guide](README_fr.md)
