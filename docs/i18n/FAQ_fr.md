# Agentic SDLC FAQ (fr)

[FR guide](README_fr.md) · [Mini-guide v1.4](MINI_GUIDE_fr.md) · [Main README](../../README.md)

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

Pas automatiquement. La v1.4 inclut des contrôles portables Goal/Plan et d'autorité, mais l'intégration native de Codex Desktop/Goals à chaque invocation exige des preuves physiques distinctes.

### 7. Gemini est-il obligatoire ou payant par défaut ?

Non. La voie I4 reste désactivée tant que consentement, identifiants, quota et confidentialité ne sont pas vérifiés. Aucun envoi automatique de code privé.

### 8. Peut-il relancer ou effacer mes conversations Codex ?

Non. Le starter ne redémarre, n'administre ni ne supprime les conversations natives de Codex. Tout adaptateur hôte exige une autorisation et des preuves séparées ; v1.4 ne certifie pas ce cycle de vie.

### 9. Quel retour d'information est activé ?

Un petit rapport mensuel de métadonnées conservé dans les artifacts GitHub Actions de votre projet. Il aide à améliorer le starter, sans transmission externe automatique.

### 10. Quelles données sont exclues ?

Code, conversations, noms des dépôts/projets, chemins, secrets, identifiants personnels, exigences, SHA et texte libre non contrôlé.

### 11. Comment changer de langue ou désactiver le feedback ?

Utilisez --language auto|en|es|pt|fr|de|it|ja|zh. Pour arrêter tous les rapports, réglez enabled=false ; --no-feedback-workflow désactive uniquement la programmation. Le README GitHub reste statique.

### 12. Quels tests et comment signaler une erreur ?

**La v1.4.0 est publiée** avec un [tag versionné, une archive ZIP portable et une somme SHA-256](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0) ; vérifiez les fichiers téléchargés. La branche `main` peut contenir des documents plus récents, tandis que la v1.3.0 reste disponible comme release précédente. Les tests portables Linux/Windows ne certifient ni les hôtes d'agents natifs ni l'utilisabilité par des tiers. Ouvrez une Issue avec étapes reproductibles et journaux expurgés. Le contenu original est sous MIT.

### 13. Puis-je combiner l'asynchrone, les équipes et l'IA sans programmation ?

Oui, comme dimensions de configuration. Leur exécution exige un hôte réel, des permissions, une reprise et une vérification indépendante. SMALL reste simple. I2 conserve théorie et choix techniques dans le dépôt canonique; la multiplication des commits/branches est interdite. L'envoi externe minimal reste impossible sans collecteur vérifié et désactivable.

---

[FR guide](README_fr.md) · [Mini-guide v1.4](MINI_GUIDE_fr.md)
