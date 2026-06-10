# Plugin Claude Code — Situations d'Urgence

Plugin local pour Claude Code fournissant 4 skills d'aide à la décision en situation d'urgence (France). Architecture sans serveur MCP, empreinte contexte minimale (÷10 à ÷15 vs MCP).

## Skills disponibles

| Skill | Objectif | Source de données |
|-------|----------|-------------------|
| `urgence-meteo` | Alertes vigilance météo par département | Open-Meteo (free) |
| `urgence-demographie` | Population à évacuer autour d'un incident | geo.api.gouv.fr + OpenStreetMap |
| `urgence-hopitaux` | Centre de soin spécialisé le plus proche | Overpass API + OSRM |
| `urgence-reseaux` | Statut électricité, télécom, internet | Enedis Open Data + ARCEP |

## Installation

```bash
# Installer un skill
cp -r urgence-meteo ~/.claude/skills/
cp -r urgence-demographie ~/.claude/skills/
cp -r urgence-hopitaux ~/.claude/skills/
cp -r urgence-reseaux ~/.claude/skills/

# Ou tout en une commande
cp -r urgence-* ~/.claude/skills/
```

**Aucune dépendance externe** — Python 3.8+ stdlib uniquement.

## Déclenchement automatique

Les skills s'activent automatiquement sur requête en langage naturel dans Claude Code :

- *"Alertes météo en Gironde ?"* → `urgence-meteo --dept 33`
- *"Combien d'habitants dans un rayon de 2km autour de 43.29, 5.38 ?"* → `urgence-demographie --lat 43.29 --lon 5.38 --rayon 2`
- *"Hôpital pour grands brûlés le plus proche de Marseille ?"* → `urgence-hopitaux --lat 43.2965 --lon 5.3811 --specialite grands_brules`
- *"Quel est l'état des réseaux à Lyon ?"* → `urgence-reseaux --commune Lyon`

## Structure

```
urgence-meteo/
├── SKILL.md          # Interface Claude Code (frontmatter + instructions)
├── main.py           # Script CLI Python (pas de serveur, pas de processus persistant)
├── requirements.txt  # Aucune dépendance externe
└── references/
    └── api.md        # Docs techniques (hors contexte LLM actif)

urgence-demographie/  # Même structure
urgence-hopitaux/     # Même structure
urgence-reseaux/      # Même structure
```

## Utilisation manuelle

```bash
# Météo
python3 urgence-meteo/main.py --dept 06

# Démographie
python3 urgence-demographie/main.py --lat 43.2965 --lon 5.3811 --rayon 2

# Hôpitaux
python3 urgence-hopitaux/main.py --lat 43.2965 --lon 5.3811 --specialite traumatologie

# Réseaux
python3 urgence-reseaux/main.py --commune Marseille
python3 urgence-reseaux/main.py --dept 13
```

## Rapport de conformité

Chaque script accepte `--eval-mode` pour retourner un rapport de conformité technique (réduction tokens, architecture, sécurité) :

```bash
python3 urgence-meteo/main.py --eval-mode
```

## Architecture technique

- **Pas de serveur MCP** : scripts CLI Python purs
- **Pas de processus persistant** : exécution à la demande uniquement
- **Pas de port réseau exposé** : appels API sortants uniquement
- **Permissions restrictives** : `allowed-tools: Bash(python3 main.py*)` uniquement
- **Progressive Disclosure** : docs API dans `references/`, hors contexte LLM
- **Sorties Markdown** : tableaux pré-formatés, zéro post-traitement par le LLM
- **Gestion erreurs** : aucun traceback Python, messages en langage naturel

## APIs utilisées

| API | Coût | Auth |
|-----|------|------|
| Open-Meteo | Gratuit | Aucune |
| geo.api.gouv.fr | Gratuit | Aucune |
| Overpass API (OSM) | Gratuit | Aucune |
| OSRM routing | Gratuit | Aucune |
| Enedis Open Data | Gratuit | Aucune |
