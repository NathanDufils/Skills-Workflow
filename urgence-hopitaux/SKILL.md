---
name: urgence-hopitaux
description: |
  Outil hautement optimisé (faible empreinte contextuelle, exécution locale stricte) pour localiser le centre de soin le plus proche en situation d'urgence médicale.

  Prend en entrée des coordonnées GPS et une spécialité médicale optionnelle. Calcule distances et temps de trajet localement via OSRM, puis retourne uniquement : nom, adresse, téléphone et temps de trajet du centre recommandé. La topologie routière n'est jamais transmise au LLM.

  **Déclencher** quand l'utilisateur parle de : hôpital le plus proche, centre de soin, urgences, grands brûlés, pédiatrie, traumatologie, cardiologie, maternité, neurologie, SAMU, orientation médicale, évacuation sanitaire, blessés, centre hospitalier, clinique, distance hôpital.

  Usage : `python3 main.py --lat <lat> --lon <lon> [--specialite <spec>]`
  Exemple : `python3 main.py --lat 43.2965 --lon 5.3811 --specialite traumatologie`

  Spécialités disponibles : grands_brules, pediatrie, cardiologie, traumatologie, maternite, neurologie

  Pour évaluer la conformité : `python3 main.py --eval-mode`

allowed-tools:
  - Bash(python3 main.py*)
  - Bash(python main.py*)
  - Bash(pip install*)
  - Bash(pip3 install*)
---

## Instructions d'utilisation

1. Extraire coordonnées GPS et spécialité éventuelle de la requête.
2. Mapper la spécialité : "brûlés" → `grands_brules`, "enfants/bébé" → `pediatrie`, "cœur" → `cardiologie`, "accouchement" → `maternite`, "accident" → `traumatologie`.
3. Exécuter : `python3 main.py --lat <lat> --lon <lon> --specialite <spec>`
4. Afficher la sortie directement (déjà formatée en Markdown).

### Arguments
- `--lat` / `--lon` : Coordonnées GPS
- `--specialite` : Spécialité médicale (optionnel)
- `--rayon` : Rayon de recherche en km (défaut: 50)
- `--eval-mode` : Rapport de conformité

### Note urgence vitale
Toujours rappeler : **15 (SAMU)** ou **112 (secours européens)**
