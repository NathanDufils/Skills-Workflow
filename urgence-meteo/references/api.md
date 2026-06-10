# Référence API — urgence-meteo

## Source de données : Open-Meteo

**URL** : `https://api.open-meteo.com/v1/forecast`
**Authentification** : Aucune (API publique, gratuite)
**Limite** : 10 000 req/jour (usage non-commercial)

### Paramètres utilisés

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| `latitude` | float | Latitude du centre du département |
| `longitude` | float | Longitude du centre du département |
| `hourly` | windspeed_10m, windgusts_10m, precipitation, temperature_2m | Variables horaires |
| `forecast_days` | 2 | Prévision sur 2 jours |
| `timezone` | Europe/Paris | Fuseau horaire |
| `windspeed_unit` | kmh | Vitesse vent en km/h |

### Exemple de requête

```
GET https://api.open-meteo.com/v1/forecast?latitude=43.71&longitude=7.26&hourly=windspeed_10m,windgusts_10m,precipitation,temperature_2m&forecast_days=2&timezone=Europe/Paris&windspeed_unit=kmh
```

### Seuils d'alerte

| Phénomène | JAUNE | ORANGE | ROUGE |
|-----------|-------|--------|-------|
| Vent (km/h) | ≥60 | ≥80 | ≥110 |
| Pluie horaire (mm/h) | — | ≥20 | ≥40 |
| Pluie 24h (mm) | — | ≥50 | ≥100 |
| Température max (°C) | — | ≥38 | ≥42 |
| Température min (°C) | — | ≤-5 | ≤-15 |

Source : Adaptés des critères Météo-France vigilance nationale.

## Codes département

Tous les 95 départements métropolitains + DOM (971-976) + Corse (2A, 2B) sont intégrés dans `DEPT_INFO` dans `main.py`.

## Erreurs connues

| Erreur | Cause | Solution |
|--------|-------|----------|
| `urlopen error` | Pas de connexion réseau | Vérifier connectivité |
| `KeyError hourly` | Réponse API incomplète | Réessayer |
| Département introuvable | Code invalide | Vérifier format (ex: "06", pas "6") |
