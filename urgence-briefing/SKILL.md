---
name: urgence-briefing
description: |
  Outil hautement optimisé (faible empreinte contextuelle, exécution locale stricte) pour générer un briefing de situation d'urgence complet en une seule commande.

  Orchestre tous les skills d'urgence disponibles en parallèle (météo, démographie, hôpitaux, réseaux, risques industriels) et produit un rapport unifié avec niveau de danger global. Un seul appel remplace 5 requêtes séparées.

  **Déclencher** quand l'utilisateur parle de : briefing d'urgence, situation complète, rapport de crise, évaluation globale, situation générale sur la zone, tous les risques, synthèse d'urgence, bilan de situation, tableau de bord crise, état des lieux urgence.

  Usage : `python3 main.py --lat <lat> --lon <lon> [--rayon <km>] [--dept <num>]`
  Exemple : `python3 main.py --lat 43.4377 --lon 4.9442 --rayon 5 --dept 13`

  Pour évaluer la conformité : `python3 main.py --eval-mode`

allowed-tools:
  - Bash(python3 main.py*)
  - Bash(python main.py*)
  - Bash(pip install*)
  - Bash(pip3 install*)
---

## Instructions d'utilisation

1. Extraire coordonnées GPS + rayon + département de la requête.
2. Exécuter : `python3 main.py --lat <lat> --lon <lon> --rayon <km> --dept <num>`
3. Afficher la sortie complète (rapport Markdown multi-sections).

### Arguments
- `--lat` / `--lon` : Coordonnées GPS de l'incident (obligatoires)
- `--rayon` : Rayon en km (défaut: 5)
- `--dept` : Numéro département pour météo (auto-détecté si absent)
- `--skills` : Skills à activer séparés par virgule (défaut: tous)
- `--eval-mode` : Rapport de conformité

### Comportement
Tous les skills s'exécutent en parallèle. Timeout par skill : 45 secondes.
Si un skill échoue, le briefing continue avec les autres.
