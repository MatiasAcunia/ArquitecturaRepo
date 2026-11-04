# 04 — Demander des changements et de nouvelles capacités

ArquitecturaRepo · Manuel d'utilisation complet · Édition v1.4 · Français

> Une demande utile explique **le comportement attendu du produit**, son contexte et la manière de constater le résultat. Le CLIENT n'a pas à prescrire l'implémentation. Le Planner confirme les décisions nouvelles ; I3 corrige les défauts et effectue les changements techniques déjà couverts par le charter.

## Dans ce chapitre

1. Décrire le résultat recherché
2. Distinguer fonctionnalité nouvelle, bogue et refactorisation
3. Un format simple pour exprimer une demande
4. Priorités, coût et chemin critique
5. Changements sensibles concernant données et sécurité
6. Retour utilisateur et évaluation perceptuelle
7. Renvoyer les défauts au même Controller
8. Éviter les politiques et campagnes doublonnées
9. Exemples de demandes bien délimitées
10. Confirmer que la nouvelle version est actuelle

## 1. Décrire le résultat recherché

Le CLIENT peut simplement dire : «Je souhaite consulter les cotisations impayées par membre et voir son dernier paiement». Cette phrase décrit une action observable. Le Planner vérifie le sens de «impayé», les périodes, les droits d'accès et les dépendances avec le stockage existant avant d'autoriser l'ingénierie.

Une formulation comme «rends le backend meilleur» ne permet pas de savoir si une modification a répondu au problème. «La recherche de membres prend plusieurs secondes lorsque notre base dépasse cinq mille enregistrements ; je voudrais retrouver rapidement les résultats corrects» fournit un contexte mesurable. L'ingénierie pourra analyser les performances et choisir une solution appropriée.

Le propriétaire du produit n'a pas à choisir préalablement un index, un cache ou une bibliothèque. Il doit préciser l'expérience souhaitée et les limites de coût, de données et de qualité. Les moyens techniques relèvent du Controller dans le cadre confirmé, avec remontée des décisions qui changent réellement le produit.

Un exemple visuel ou une courte capture peut aider, à condition d'être associé à un candidat et de ne pas exposer d'informations privées. Le problème, le résultat attendu et la manière de l'éprouver importent davantage qu'une grande quantité de commentaires ou captures non contextualisés.

## 2. Distinguer fonctionnalité nouvelle, bogue et refactorisation

Un **bogue** signifie que le programme ne respecte pas une règle déjà confirmée. Une **fonctionnalité nouvelle** ajoute ou modifie un comportement de produit. Une **refactorisation** restructure l'implémentation sans changer le contrat fonctionnel. Les trois nécessitent des tests, mais pas la même décision stratégique.

Exemple : le charter prévoit que la désactivation d'un membre conserve l'historique de ses paiements. La fonction efface cet historique. Il s'agit d'un bogue dans la campagne actuelle, et I3 doit corriger la persistance et faire une régression. Le Planner n'ouvre pas une nouvelle campagne «réparer le bouton».

Si le CLIENT demande ensuite que des membres inactifs puissent être réactivés avec des droits particuliers, c'est une règle nouvelle. Le Planner doit confirmer qui peut réactiver, comment les paiements sont traités et quel impact cela a sur les interfaces. On ne peut pas inventer une réponse et appeler «bug fix» ce qui modifie le produit.

Une refactorisation de classe ou d'API interne peut rester dans le mandat de I3. Si elle change le contrat public ou impose une migration de données au-delà du périmètre, il faut examiner les conséquences et la validité du charter. Le nom donné à l'opération ne remplace pas l'analyse des effets.

| Situation | Route normale |
| --- | --- |
| Comportement existant contraire à une exigence. | Correction et tests par I3 dans la campagne actuelle. |
| Nouvelle règle métier demandée par le CLIENT. | Confirmation, impact et autorisation par le Planner. |
| Réorganisation technique sans effet fonctionnel. | Exécution par I3 avec contrôles appropriés. |
| Conflit entre projets ou propriétaires canoniques. | Coordination stratégique, éventuellement I1. |
| Publication, dépense ou partage externe nouveau. | Autorisation spécifique du responsable habilité. |

## 3. Un format simple pour exprimer une demande

La plupart des demandes peuvent contenir cinq informations : état actuel, résultat attendu, contexte d'utilisation, contraintes et preuve de réussite. Il n'est pas nécessaire de demander au CLIENT de remplir un contrat complexe. Le Planner peut structurer ensuite la capacité et ses dépendances.

Par exemple : «Dans la liste des membres actifs, un membre désactivé apparaît encore. Je souhaite qu'il soit exclu de cette liste, tout en conservant son historique visible aux administrateurs. La correction doit être vérifiée après redémarrage». Si cette règle était déjà confirmée, l'énoncé est une description de bogue exploitable.

Autre demande : «La trésorerie doit exporter chaque mois un CSV des montants encaissés, sans numéros de téléphone». C'est une capacité nouvelle. Le Planner confirme le calendrier, le format, les autorisations, les risques d'exposition et le caractère actuel des chiffres. I3 implémente l'export et les tests adaptés.

Une préférence de présentation est également légitime : «Sur mobile, le nombre de places restantes doit être visible avant de remplir le formulaire». La solution technique peut être discutée, mais le jugement final sur la facilité d'usage ne doit pas être déduit automatiquement du nombre de tests verts.

## 4. Priorités, coût et chemin critique

Déplacer une fonctionnalité à plus tard n'implique pas nécessairement de changer ses exigences. Modifier une règle d'éligibilité, en revanche, peut affecter plusieurs capacités et nécessite une supersession explicite. Le Planner distingue ainsi calendrier, portée et sémantique du produit.

Le chemin critique indique quelles capacités conditionnent les suivantes. Si une inscription dépend du statut des cotisations, il vaut mieux avoir une source fiable de ce statut avant d'implémenter les règles d'inscription. Les éléments réellement indépendants peuvent avancer en parallèle si les ressources et contrats ne créent pas d'interférence.

Pour une première livraison rapide, une petite capacité fonctionnelle vaut souvent mieux qu'une architecture techniquement ambitieuse dont l'usage principal n'est pas démontré. Un CRUD correctement persisté peut révéler des problèmes de modèle et d'interface avant l'ajout de fonctions secondaires. La réduction du périmètre ne doit toutefois pas supprimer les gates nécessaires pour le comportement promis.

Le coût comprend développement, calcul, stockage, services externes et maintenance. Le nombre d'agents ou de commits ne mesure pas ce bénéfice. Un nouveau mécanisme doit résoudre une catégorie de défaut ou débloquer une capacité réelle ; sinon, il ajoute de la complexité sans valeur.

Un changement qui entraîne une dépense, une publication ou une opération irréversible demande un preflight et l'autorité correspondante. Une autorisation pour tester localement ne permet pas d'envoyer des données privées à un fournisseur ni de déclencher une facturation nouvelle.

## 5. Changements sensibles concernant données et sécurité

Certaines demandes ont des conséquences importantes malgré une interface simple. «Fusionner des membres en double» peut altérer des transactions historiques. «Rendre le rapport accessible à tous» peut exposer des coordonnées personnelles. «Changer de base» peut invalider des sauvegardes ou des références de currentness.

Le Planner reconstruit les propriétaires, entrées/sorties, données actuelles, dépendances downstream, règles d'invalidation et risques de récupération. I3 prépare les migrations, transactions, cas négatifs, idempotence, tests de concurrence et rollback dans les limites autorisées. Les étapes ayant des effets sur des données réelles demandent une preuve cohérente du résultat.

Pour SQLite en mode WAL, un snapshot doit correspondre à l'état transactionnel utile ; le fichier principal isolé peut être périmé. Si la source des données ne peut être identifiée, un HOLD spécifique protège les actions dépendantes. Le fait qu'un schéma de contrôle soit valide ne certifie pas les données qu'il décrit.

Il faut également distinguer désactivation logique, anonymisation, suppression physique et politique de conservation. Le CLIENT décide de la règle métier dans les limites légales ; l'ingénierie détermine comment l'appliquer de manière vérifiable. Un script destructif ne doit pas cibler un répertoire large ni des données dont l'ownership est inconnu.

Les artefacts générés dépendent parfois de sources, licences et paramètres. Un rapport ou une vidéo produit à partir d'entrées qui ont changé peut perdre sa validité. Renommer un fichier en `final` n'établit pas son lineage et ne rend pas actuelles des références anciennes.

## 6. Retour utilisateur et évaluation perceptuelle

Une interface peut passer tous ses tests automatiques et rester difficile à utiliser. L'évaluation humaine est un gate distinct. Un retour utile décrit la tâche et le problème : «Quand aucune place n'est disponible, le message n'explique pas comment rejoindre une liste d'attente» est plus actionnable que «l'écran est mauvais».

Le CLIENT peut préciser la hiérarchie visuelle, l'accessibilité et les préférences du public. L'ingénierie propose des options et peut mesurer des propriétés objectives, mais elle ne doit pas inventer une approbation esthétique. Les captures de démonstration doivent correspondre au candidat réel, dans un environnement pertinent et avec des données fictives.

Si le problème d'UX viole un critère déjà confirmé, c'est un défaut à corriger par I3. S'il révèle une règle nouvelle, le Planner doit la confirmer. Un changement de couleur mineur peut rester dans le périmètre d'implémentation selon le charter, alors qu'une nouvelle interaction de paiement demande davantage d'analyse.

N'envoyez pas des captures comportant des noms réels, numéros de téléphone, tokens ou documents privés dans une issue publique. Un exemple synthétique et un rapport expurgé peuvent reproduire le problème sans exposer les utilisateurs du produit.

## 7. Renvoyer les défauts au même Controller

Lorsqu'un terminal est rejeté pour des problèmes déjà couverts par le charter, le Planner renvoie un ensemble **consolidé de falsificateurs** : exigence, candidat, résultat observé, preuve et gate concerné. I3 analyse, corrige, réintègre et obtient une nouvelle revue applicable. La campagne existante reste responsable de l'exécution.

Il n'est pas nécessaire de créer un nouveau charter ou un PASS stratégique pour chaque erreur de test. Ce processus ferait perdre au Controller son rôle d'ingénieur responsable et obligerait le CLIENT à arbitrer des corrections techniques. Une fois autorisé, I3 possède le debugging et les retries normaux jusqu'au terminal réel.

Lorsque le même défaut revient plusieurs fois, I3 doit cesser les corrections superficielles et examiner le sous-système de manière exhaustive. Cela peut impliquer la persistance, la concurrence, les invariants, la qualité des tests et une revue indépendante. Le but n'est pas de produire une succession de rapports `PASS` étroits, mais de résoudre la cause de la régression.

Une modification de l'intention du CLIENT reste une décision de produit ; elle ne doit pas être cachée sous «correction de bug». Symétriquement, un défaut normal n'est pas une invalidation stratégique du charter. La frontière entre les deux protège la vitesse et la responsabilité.

## 8. Éviter les politiques et campagnes doublonnées

Chaque préoccupation doit avoir un propriétaire canonique et une surface d'état courant. Deux campagnes qui changent une même interface sans coordination peuvent produire des contrats contradictoires. Deux fichiers `CURRENT` prétendant définir les mêmes exigences risquent de désorienter la prochaine session.

Avant d'ajouter une politique, cherchez le contrat existant. Les décisions stables, l'état mutable, l'autorité de campagne et les journaux de runtime ont chacun leur rôle. Une copie supplémentaire d'un résumé de vérité peut être utile comme index, mais ne doit pas devenir une deuxième autorité active.

La réutilisation des artefacts nécessite également une provenance. Si un rapport approuvé est repris ailleurs, il faut savoir quelles entrées l'ont produit et ce qui pourrait invalider cette approbation. Le stockage et les fichiers temporaires doivent être gérés sans multiplier des copies lourdes inutilement.

Un MASTER OWNER intervient lorsque les causes sont systémiques : duplication des politiques, churn de Planner, mauvaise séparation d'ownership ou défaillances d'intégration. Il doit corriger l'organisation concernée au lieu de créer une nouvelle étape de contrôle pour chaque bogue.

## 9. Exemples de demandes bien délimitées

**A — Cotisations en retard.** «Afficher les membres qui n'ont pas payé le mois, en tenant compte des versements partiels». Le Planner confirme la définition du mois, du paiement et de la dette ; I3 utilise la DB actuelle et teste les cas négatifs et la sécurité des consultations.

**B — Perte d'historique.** «Après désactivation, les paiements disparaissent alors qu'ils devaient rester consultables». C'est un bogue dans le charter. I3 corrige la cause, montre le readback et obtient la revue nécessaire sur le nouveau candidat.

**C — Export CSV.** «La trésorerie veut un total mensuel sans coordonnées personnelles». C'est une capacité nouvelle. Il faut confirmer le format, la période, le rôle autorisé, la précision des montants et les risques propres aux fichiers CSV.

**D — Interface mobile.** «Le bouton d'annulation n'est pas accessible sur un écran étroit». Il faut vérifier le parcours sur le dispositif concerné et distinguer la correction d'un défaut de présentation d'une nouvelle règle de comportement.

**E — Nouvelle DB partagée.** «Nous voulons remplacer le stockage local par un serveur multiutilisateur». Cela change réseau, concurrence, authentification, sauvegardes, coût et récupération. Une analyse stratégique et une migration avec rollback sont nécessaires.

Ces exemples n'imposent pas un template rigide. Ils montrent comment séparer intention, décisions ouvertes, exécution et preuves, pour éviter que l'architecture ne détourne le temps des vrais besoins du produit.

## 10. Confirmer que la nouvelle version est actuelle

Après la modification, I3 doit identifier le candidat intégré, les tests exécutés, les résultats physiques et les artefacts affectés. Le Product State, le code, les données et la revue doivent correspondre à cette identité. Un diff ou une déclaration «fait» ne prouvent pas que l'utilisateur pourra accomplir la tâche.

Le Planner audite le terminal contre les exigences et enregistre acceptation, retour à I3 ou question de produit. Le CLIENT juge les critères réservés, notamment l'expérience. Les dépendants downstream ne doivent être débloqués qu'à partir d'une capacité effectivement acceptée.

Une session future doit pouvoir retrouver la décision sans relire le chat. Si elle découvre un lien cassé, une source périmée ou deux exigences actives contradictoires, elle doit réconcilier cette situation. Une modification n'est durable que si son résultat et ses références restent vérifiables.

Le meilleur indicateur d'une demande bien traitée est la réduction d'incertitude : on sait ce qui a changé, pourquoi, qui a approuvé la règle, comment le résultat a été testé et quelle action devient possible ensuite.

**Suite :** chapitre 05, incidents, erreurs et récupération du projet.

## Sources et portée

- [Limites du CLIENT](../../../../protocols/CLIENT_BOUNDARY.md)
- [Standard des charters](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Cycle des capacités et preuves](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Découverte et plan de livraison](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Revue du candidat exact](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Support public v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)

Les exemples fictifs ne créent pas des exigences réelles ni des autorisations de campagne. Le propriétaire et les sources du produit concerné restent déterminants.
