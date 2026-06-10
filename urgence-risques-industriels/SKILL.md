---
name: urgence-risques-industriels
description: |
  Outil hautement optimisé (faible empreinte contextuelle, exécution locale stricte) pour identifier les risques industriels et naturels en situation d'urgence.

  Interroge l'API officielle GEORISQUES (gouvernement français) pour localiser les sites SEVESO, ICPE (Installations Classées), et évaluer les risques naturels autour d'un incident. Calcule localement les niveaux de danger et ne retourne qu'une synthèse opérationnelle.

  **Déclencher** quand l'utilisateur parle de : site SEVESO, risque chimique, fuite industrielle, ICPE, installation classée, risque naturel, zone inondable, risque sismique, risque industriel, accident chimique, nuage toxique, explosion usine, périmètre de sécurité, risques autour de, dangers industriels.

  Usage : `python3 main.py --lat <lat> --lon <lon> [--rayon <km>]`
  Exemple : `python3 main.py --lat 43.2965 --lon 5.3811 --rayon 5`

  Pour évaluer la conformité : `python3 main.py --eval-mode`
  Déclencher --eval-mode si l'utilisateur demande si ce plugin respecte les contraintes de tokens.

allowed-tools:
  - Bash(python3 main.py*)
  - Bash(python main.py*)
  - Bash(pip install*)
  - Bash(pip3 install*)
---

## Instructions d'utilisation

1. Extraire coordonnées GPS et rayon de la requête.
2. Exécuter : `python3 main.py --lat <lat> --lon <lon> --rayon <km>`
3. Afficher la sortie directement (Markdown pré-formaté).

### Arguments
- `--lat` / `--lon` : Coordonnées GPS du point d'incident
- `--rayon` : Rayon de recherche en km (défaut: 5)
- `--commune` : Code INSEE ou nom de commune (pour risques naturels)
- `--eval-mode` : Rapport de conformité technique

### Niveaux de danger
- 🔴 CRITIQUE : Site SEVESO seuil haut ou nucléaire
- 🟠 ÉLEVÉ : Site SEVESO seuil bas ou ICPE autorisation
- 🟡 MODÉRÉ : ICPE enregistrement/déclaration
- 🟢 FAIBLE : Aucune installation classée
