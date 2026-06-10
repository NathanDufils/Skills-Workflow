# Référence API — urgence-demographie

## Source 1 : geo.api.gouv.fr (population)

**URL** : `https://geo.api.gouv.fr/communes`
**Authentification** : Aucune (API publique française)
**Maintenu par** : Etalab / DINUM

### Paramètres clés

| Paramètre | Description |
|-----------|-------------|
| `lat` + `lon` | Centre de recherche |
| `distance` | Rayon en mètres |
| `fields` | `nom,code,population,codesPostaux,centre` |

### Exemple

```
GET https://geo.api.gouv.fr/communes?lat=43.2965&lon=5.3811&distance=2000&fields=nom,population,codesPostaux
```

### Réponse (extrait)
```json
[
  {"nom": "Marseille", "code": "13055", "population": 870731, "codesPostaux": ["13001",...]}
]
```

## Source 2 : OpenStreetMap / Overpass API (sites sensibles)

**URL** : `https://overpass-api.de/api/interpreter`
**Authentification** : Aucune (usage raisonnable requis)

### Requête Overpass utilisée
```
[out:json][timeout:20];
(
  node["amenity"~"school|hospital|nursing_home|clinic|kindergarten|fire_station|police"](around:{radius},{lat},{lon});
  way[...](around:{radius},{lat},{lon});
);
out tags;
```

### Correspondance amenity → catégorie

| Valeur OSM | Catégorie affichée |
|------------|-------------------|
| `school`, `kindergarten` | Écoles/établissements scolaires |
| `hospital`, `clinic` | Hôpitaux/cliniques |
| `nursing_home` | EHPAD/maisons de retraite |
| `fire_station` | Pompiers |
| `police` | Police/gendarmerie |

## Logique d'évaluation de priorité

| Condition | Priorité |
|-----------|----------|
| Population > 100 000 OU (EHPAD > 0 ET pop > 50 000) OU hôpitaux ≥ 2 | CRITIQUE 🔴 |
| Population > 20 000 OU EHPAD > 0 OU hôpital > 0 | HAUTE 🟠 |
| Population > 5 000 OU écoles > 0 | MODÉRÉE 🟡 |
| Autre | FAIBLE 🟢 |
