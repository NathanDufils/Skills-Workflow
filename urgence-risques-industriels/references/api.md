# Référence API — urgence-risques-industriels

## Source principale : GEORISQUES API v1

**URL base** : `https://georisques.gouv.fr/api/v1/`
**Documentation** : `https://georisques.gouv.fr/api/swagger-ui.html`
**Authentification** : Aucune (API publique française)
**Maintenu par** : BRGM / Ministère de la Transition Écologique

## Endpoint 1 : Installations Classées (ICPE/SEVESO)

```
GET /installations_classees?latlon={lon},{lat}&rayon={rayon_m}&page={n}&page_size=50&etat_activite=En activite
```

⚠️ Format `latlon` : **longitude d'abord**, puis latitude.

### Régimes ICPE

| Code | Label | Danger |
|------|-------|--------|
| `S` | SEVESO Seuil Haut | 🔴 CRITIQUE |
| `SB` | SEVESO Seuil Bas | 🟠 ÉLEVÉ |
| `A` | Autorisation | 🟠 ÉLEVÉ |
| `AS` | Autorisation Simplifiée | 🟡 MODÉRÉ |
| `E` | Enregistrement | 🟡 MODÉRÉ |
| `D` | Déclaration | 🟡 FAIBLE |

### Champs réponse clés

| Champ | Description |
|-------|-------------|
| `nomEtablissement` | Nom de l'établissement |
| `adresseEtablissement` | Adresse |
| `commune` | Nom commune |
| `codePostal` | Code postal |
| `regime` | Code régime (S/SB/A/E/D) |
| `seveso` | "Seuil haut", "Seuil bas" ou null |
| `etatActivite` | "En activité", "En cours de cessation"... |
| `coordonneeXBasiasEtablissement` | Longitude (Lambert/WGS84) |
| `coordonneeYBasiasEtablissement` | Latitude |

## Endpoint 2 : Risques par commune

```
GET /resultats_rapport_risque_commune?code_insee={code_commune}
```

Retourne les risques naturels et technologiques officiels de la commune :
- Inondations (PPRi)
- Mouvement de terrain
- Séisme (zone 1-5)
- Retrait-gonflement argiles
- Radon (catégories 1-3)
- Plans de Prévention des Risques (PPR)

## Plans d'urgence SEVESO

| Type de plan | Déclencheur | Autorité |
|-------------|-------------|----------|
| **POI** (Plan d'Opérations Interne) | Tout incident sur site | Exploitant |
| **PPI** (Plan Particulier d'Intervention) | Risque externe SEVESO SH | Préfet |
| **PCS** (Plan Communal de Sauvegarde) | Activation PPI | Maire |

## Contacts urgence industrielle

| Organisme | Rôle | Contact |
|-----------|------|---------|
| SDIS | Premiers secours | 18 |
| SAMU | Victimes chimiques | 15 |
| DREAL | Inspection ICPE | Via préfecture |
| INERIS | Expertise technique NRBC | 03 44 55 66 77 |
| Cellule NRBC SDIS | Risque chimique/radiologique | Via CODIS 18 |
