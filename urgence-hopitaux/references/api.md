# Référence API — urgence-hopitaux

## Source 1 : OpenStreetMap / Overpass API (localisation hôpitaux)

**URL** : `https://overpass-api.de/api/interpreter`
**Authentification** : Aucune
**Limite** : Usage raisonnable (pas de scraping massif)

### Requête Overpass utilisée

```
[out:json][timeout:30];
(
  node["amenity"~"hospital|clinic"](around:{radius},{lat},{lon});
  way["amenity"~"hospital|clinic"](around:{radius},{lat},{lon});
  relation["amenity"~"hospital|clinic"](around:{radius},{lat},{lon});
);
out center tags;
```

### Tags OSM récupérés

| Tag | Utilisation |
|-----|-------------|
| `name` | Nom de l'établissement |
| `operator` | Opérateur (si pas de name) |
| `phone` / `contact:phone` | Numéro de contact |
| `emergency` | `yes`/`24/7` = urgences permanentes |
| `addr:*` | Adresse postale |

## Source 2 : OSRM (calcul temps de trajet)

**URL** : `http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false`
**Authentification** : Aucune (serveur public OSRM)
**Retourne** : `duration` (secondes) + `distance` (mètres)

### Exemple
```
GET http://router.project-osrm.org/route/v1/driving/5.3811,43.2965;5.4,43.31?overview=false
```

### Fallback si OSRM indisponible
Estimation : `distance_km / vitesse_moyenne * 60 minutes`
- > 10 km : vitesse 60 km/h
- ≤ 10 km : vitesse 40 km/h (urbain)

## Filtrage par spécialité

Le filtrage se fait sur les tags OSM + nom de l'établissement par mots-clés :

| Argument `--specialite` | Mots-clés recherchés |
|-------------------------|----------------------|
| `grands_brules` | burn, grands_brul, brulure |
| `pediatrie` | paediatric, pediatric, enfant, child, neonat |
| `cardiologie` | cardiac, cardio, cardiolog, coeur, heart |
| `traumatologie` | trauma, traumatolog, urgence, accident |
| `maternite` | maternit, obstetric, gynecolog, accouchement |
| `neurologie` | neurolog, neurochirurg, neuro, avc, stroke |

⭐ Les établissements avec correspondance spécialité apparaissent en premier.

## Numéros d'urgence (toujours rappeler)

| Numéro | Service |
|--------|---------|
| **15** | SAMU (urgences médicales) |
| **18** | Pompiers |
| **112** | Numéro d'urgence européen |
| **15** | Régulation médicale (orientation hôpital) |
