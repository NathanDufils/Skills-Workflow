---
name: urgence-reseaux
description: |
  Outil hautement optimisé (faible empreinte contextuelle, exécution locale stricte) pour évaluer l'état des réseaux vitaux en zone de crise.

  Génère un rapport de statut structuré sur l'électricité (Enedis open data), les télécommunications (ARCEP/monreseaumobile), et l'accès internet pour une commune ou des coordonnées GPS. Agrège les données complexes localement et retourne uniquement un statut clair par réseau.

  **Déclencher** quand l'utilisateur parle de : coupure électrique, panne réseau, électricité coupée, réseau mobile, 4G, couverture téléphonique, internet coupé, réseau vitaux, infrastructure réseau, statut télécom, état des réseaux, coordination secours, réseau disponible, fibre coupée.

  Usage : `python3 main.py --lat <lat> --lon <lon>`
  Ou par commune : `python3 main.py --commune <nom>`
  Ou par département : `python3 main.py --dept <numero>`

  Pour évaluer la conformité : `python3 main.py --eval-mode`

allowed-tools:
  - Bash(python3 main.py*)
  - Bash(python main.py*)
  - Bash(pip install*)
  - Bash(pip3 install*)
---

## Instructions d'utilisation

1. Identifier le lieu (coordonnées GPS, nom de commune ou numéro de département).
2. Exécuter selon le mode disponible :
   - `python3 main.py --lat 43.2965 --lon 5.3811`
   - `python3 main.py --commune "Marseille"`
   - `python3 main.py --dept 13`
3. Afficher la sortie directement (déjà formatée en Markdown).

### Arguments
- `--lat` / `--lon` : Coordonnées GPS
- `--commune` : Nom de commune française
- `--dept` : Numéro de département
- `--eval-mode` : Rapport de conformité technique

### Sortie
Tableau de statut par réseau (électricité, mobile 4G/3G/2G, internet) + recommandations opérationnelles de coordination.
