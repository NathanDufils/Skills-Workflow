# Référence API — urgence-reseaux

## Source 1 : geo.api.gouv.fr (localisation commune)

**URL** : `https://geo.api.gouv.fr/communes`
**Authentification** : Aucune
**Paramètres** : `nom` / `lat+lon` / `codeDepartement` + `fields=nom,population,codesPostaux,departement`

## Source 2 : Enedis Open Data (qualité fourniture électrique)

**URL** : `https://data.enedis.fr/api/explore/v2.1/catalog/datasets/bilan-de-la-qualite-de-fourniture-delectricite/records`
**Authentification** : Aucune (données publiques annuelles)
**Note** : Les données sont agrégées annuellement par département. Les coupures en temps réel nécessitent l'API privée Enedis (non publique).

### Indicateurs clés

| Champ | Description |
|-------|-------------|
| `cri_b` / `critere_b` | Critère B : nombre moyen de coupures longues par client/an |
| `cri_a` / `critere_a` | Critère A : durée cumulée des coupures en minutes/client/an |
| `departement` | Code département |
| `annee` | Année de référence |

## Source 3 : Estimation couverture réseau (ARCEP référentiel)

Profils estimatifs basés sur la densité de population, cohérents avec les données ARCEP :

| Profil | Population | 4G | 3G | 2G | Fibre |
|--------|------------|----|----|-----|-------|
| Métropole | > 100 000 | 99% | 99% | 99% | 85% |
| Urbain | 20 000–100 000 | 97% | 99% | 99% | 70% |
| Périurbain | 5 000–20 000 | 92% | 96% | 99% | 45% |
| Rural | 500–5 000 | 78% | 88% | 95% | 20% |
| Rural isolé | < 500 | 55% | 72% | 85% | 5% |

Source : Observatoire du déploiement des réseaux mobiles ARCEP (rapport annuel).

## Source 4 : Test connectivité opérateurs

Le script effectue un HEAD request vers les portails des 4 opérateurs principaux pour détecter les pannes majeures :
- Orange : `https://www.orange.fr`
- SFR : `https://www.sfr.fr`
- Bouygues : `https://www.bouyguestelecom.fr`
- Free : `https://www.free.fr`

Un échec de connexion peut indiquer : panne nationale, maintenance, ou simple blocage réseau local.

## Ressources de secours en cas de panne totale

| Ressource | Usage |
|-----------|-------|
| Satellite Starlink / Eutelsat | Connexion haut-débit en zone sans réseau |
| Radios VHF/UHF TETRA (réseau ANTARES) | Communication sécurisée secours |
| France Bleu locale + France Info | Diffusion d'alertes, fréquences secours |
| Points d'accès WiFi de crise | Mairies, casernes, gendarmeries |
