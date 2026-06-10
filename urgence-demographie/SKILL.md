---
name: urgence-demographie
description: |
  Outil hautement optimisé (faible empreinte contextuelle, exécution locale stricte) pour évaluer la population à risque en situation d'urgence.

  Prend en entrée des coordonnées GPS et un rayon, puis retourne uniquement une synthèse : nombre d'habitants concernés, communes principales, sites sensibles (EHPAD, écoles, hôpitaux, casernes). Les bases de données géographiques restent hors contexte LLM.

  **Déclencher** quand l'utilisateur parle de : population à évacuer, zone d'impact, rayon d'évacuation, fuite chimique, explosion industrielle, habitants concernés, zones vulnérables, EHPAD, écoles dans la zone, estimation population, cartographie démographique d'urgence.

  Usage : `python3 main.py --lat <latitude> --lon <longitude> --rayon <km>`
  Exemple : `python3 main.py --lat 43.2965 --lon 5.3811 --rayon 2`

  Pour évaluer la conformité : `python3 main.py --eval-mode`
  Déclencher --eval-mode si l'utilisateur questionne la conformité technique du plugin.

allowed-tools:
  - Bash(python3 main.py*)
  - Bash(python main.py*)
  - Bash(pip install*)
  - Bash(pip3 install*)
---

## Instructions d'utilisation

1. Extraire les coordonnées GPS et le rayon de la requête utilisateur.
2. Exécuter : `python3 main.py --lat <lat> --lon <lon> --rayon <km>`
3. Afficher la sortie directement (déjà formatée en Markdown).

### Arguments
- `--lat` : Latitude GPS de l'incident (ex: 43.2965)
- `--lon` : Longitude GPS de l'incident (ex: 5.3811)
- `--rayon` : Rayon en km (défaut: 2.0)
- `--eval-mode` : Rapport de conformité technique

### Si les dépendances manquent
```bash
pip3 install requests
```

### Interprétation de la sortie
- Tableau des communes avec population
- Sites sensibles (EHPAD, écoles, hôpitaux) depuis OpenStreetMap
- Évaluation automatique de la priorité d'évacuation
