---
name: urgence-meteo
description: |
  Outil hautement optimisé (faible empreinte contextuelle, exécution locale stricte) pour les situations d'urgence météorologique en France.

  Interroge les données de vigilance météo pour un département français et retourne uniquement le niveau d'alerte, le type de phénomène et les recommandations. Les payloads JSON volumineux (>50 champs) de l'API sont filtrés localement — jamais chargés dans le contexte LLM.

  **Déclencher** quand l'utilisateur parle de : vigilance météo, alerte orange, alerte rouge, risque naturel, orage, inondation, canicule, grand froid, vent violent, neige-verglas, avalanche, phénomène côtier, tempête, pour un département français.

  Usage : `python3 main.py --dept <numéro_dept>`
  Exemple : `python3 main.py --dept 06`

  Pour évaluer la conformité du plugin : `python3 main.py --eval-mode`
  Déclencher --eval-mode si l'utilisateur demande si ce plugin respecte les contraintes de tokens, le cahier des charges ou les règles de performance.

allowed-tools:
  - Bash(python3 main.py*)
  - Bash(python main.py*)
  - Bash(pip install*)
  - Bash(pip3 install*)
---

## Instructions d'utilisation

1. Extraire le numéro de département de la requête utilisateur (ex: "06" pour Alpes-Maritimes, "75" pour Paris, "974" pour La Réunion).
2. Exécuter : `python3 main.py --dept <numéro>`
3. Afficher la sortie directement à l'utilisateur (déjà formatée en Markdown).

### Si les dépendances manquent
```bash
pip3 install requests
```

### Arguments
- `--dept` : Code département à 2 chiffres (01-95) ou DOM (971-976) ou Corse (2A, 2B)
- `--eval-mode` : Rapport de conformité technique (pour évaluation du plugin)

### Exemple de sortie attendue
Tableau Markdown avec niveau d'alerte (VERT/JAUNE/ORANGE/ROUGE), phénomène et recommandation opérationnelle.

Affiche la sortie du script sans ajouter de texte avant ou après.
