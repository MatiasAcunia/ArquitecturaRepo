# Pont de continuité des agents — Agent Continuity Bridge 0.2.1

## Pourquoi il existe

ArquitecturaRepo gère les autorités, plans et validations du développement. Ce module facultatif isole un contrôleur externe de continuité des agents, avec sa propre version. Il ne remplace ni le modèle IA ni le responsable de campagne. Le cœur portable fonctionne sans lui.

## Fonctions actuellement vérifiées

Inspection hors ligne d’une archive Codex Daily Control 3.1 : chemins sûrs, inventaire, SHA-256, version et cohérence de configuration ; enregistrement d’une empreinte dans un projet existant, vérification et désenregistrement sûr. Aucune donnée privée, identifiant de Goal, clé ou configuration utilisateur n’est distribuée.

## Prérequis et connexion

Python 3.10+ ; projet ArquitecturaRepo existant avec .agentic-sdlc ; archive 3.1 obtenue séparément. Pour exécuter le contrôleur natif : Windows, PowerShell 5.1, Codex Desktop compatible, puis Git, SQLite et éventuellement Drive/rclone configurés. Ce module ne les installe pas.

## Sécurité et limites

La version 3.1 reste une préversion non validée sur un véritable poste Windows/Codex. Clôture native, transfert Desktop, reprise des quotas et livraison distante restent désactivés/non vérifiés.

## CLI

```bash
python "bridge.py" inspect --package "CONTROLLER_3_1.zip"
python "bridge.py" install --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" status --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" uninstall --project "MY_PROJECT"
```


Installation dans un projet existant : `python install_into_project.py --project "PROJET"`. Lancez `.agentic-sdlc/extensions/agent-continuity-bridge/pluginctl.py`. Désenregistrez le contrôleur avant la désinstallation `--remove`. Aucune action native n’est effectuée.
