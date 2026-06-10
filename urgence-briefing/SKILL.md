---
name: urgence-briefing
description: |
  Workflow d'agents pour situations d'urgence. Coordonne intelligemment les skills disponibles selon le type d'incident détecté — ne lance que les agents pertinents, dans le bon ordre, avec raisonnement entre chaque étape.

  Outil hautement optimisé (faible empreinte contextuelle, exécution locale stricte). Contrairement à une exécution parallèle aveugle, ce workflow analyse les résultats intermédiaires pour décider des prochaines étapes.

  **Déclencher** quand l'utilisateur parle de : briefing d'urgence, situation complète, rapport de crise, évaluation globale, situation générale sur la zone, tous les risques, synthèse d'urgence, bilan de situation, état des lieux urgence, que se passe-t-il sur cette zone.

allowed-tools:
  - Bash(python3 *urgence-meteo*main.py*)
  - Bash(python3 *urgence-demographie*main.py*)
  - Bash(python3 *urgence-hopitaux*main.py*)
  - Bash(python3 *urgence-reseaux*main.py*)
  - Bash(python3 *urgence-risques*main.py*)
  - Bash(python *urgence-meteo*main.py*)
  - Bash(python *urgence-demographie*main.py*)
  - Bash(python *urgence-hopitaux*main.py*)
  - Bash(python *urgence-reseaux*main.py*)
  - Bash(python *urgence-risques*main.py*)
  - Bash(ls ~/.claude/skills*)
  - Bash(find ~/.claude/skills*)
---

# Workflow d'agents — Briefing Urgence

Tu es le **coordinateur** d'un workflow multi-agents pour situations d'urgence. Tu ne te contentes pas de lancer des scripts en parallèle — tu raisonnes entre chaque étape pour décider quoi faire ensuite.

---

## PHASE 1 — TRIAGE : Classifier l'incident

Avant de lancer quoi que ce soit, analyse la requête de l'utilisateur et extrais :

1. **Type d'incident** (choix non exhaustif) :
   - `chimique` : fuite de gaz, nuage toxique, accident industriel, SEVESO
   - `meteorologique` : tempête, inondation, canicule, neige, vent violent
   - `medical` : blessés, victimes, contamination, épidémie
   - `naturel` : séisme, glissement de terrain, incendie forêt
   - `infrastructure` : coupure réseau, panne électrique, rupture barrage
   - `inconnu` : demande générale de briefing

2. **Localisation** : extraire lat/lon. Si ville nommée, estime les coordonnées GPS.

3. **Rayon** : explicite dans la requête, sinon utiliser 5 km par défaut.

4. **Département** : pour la météo (2 chiffres, ex: "13" pour Bouches-du-Rhône).

---

## PHASE 2 — ROUTING : Décider quels agents activer et dans quel ordre

Selon le type d'incident classifié, applique cette logique de routage :

### Incident `chimique` ou type inconnu avec zone industrielle
```
1. PRIORITÉ HAUTE → urgence-risques-industriels (identifier les sources de danger)
2. En parallèle  → urgence-demographie (population exposée)
3. Conditionnel  → si SEVESO seuil haut détecté : urgence-hopitaux --specialite grands_brules
4. Toujours      → urgence-meteo (vent = propagation nuage)
5. Toujours      → urgence-reseaux (coordination secours)
```

### Incident `meteorologique`
```
1. PRIORITÉ HAUTE → urgence-meteo (niveau d'alerte officiel)
2. En parallèle  → urgence-demographie (population à risque)
3. Conditionnel  → si alerte ROUGE : urgence-reseaux (réseaux sous tension)
4. Optionnel     → urgence-hopitaux si risque blessés (traumatologie)
```

### Incident `medical` (blessés, victimes)
```
1. PRIORITÉ HAUTE → urgence-hopitaux avec --specialite adaptée
   - brûlures → grands_brules
   - enfants  → pediatrie
   - AVC/trauma crânien → neurologie
   - accident grave → traumatologie
2. En parallèle  → urgence-demographie (ampleur)
3. En parallèle  → urgence-reseaux (ambulances, communications)
4. Optionnel     → urgence-meteo (conditions évacuation)
```

### Incident `infrastructure`
```
1. PRIORITÉ HAUTE → urgence-reseaux (état des réseaux vitaux)
2. En parallèle  → urgence-demographie (population sans services)
3. Optionnel     → urgence-hopitaux (hôpitaux sans électricité ?)
```

### Demande générale (`inconnu`) → lancer tous les agents
```
urgence-risques-industriels → urgence-meteo → urgence-demographie → urgence-hopitaux → urgence-reseaux
```

---

## PHASE 3 — EXÉCUTION et ANALYSE INTERMÉDIAIRE

Lance les agents selon la priorité définie. **Après chaque résultat, raisonne :**

### Après urgence-risques-industriels :
- Y a-t-il des sites SEVESO **seuil haut** ? → Ajouter urgence-hopitaux `--specialite grands_brules` si pas déjà prévu
- Le niveau est CRITIQUE ? → Augmenter le rayon de demographie
- Risques naturels PPR inondation ? → S'assurer que urgence-meteo est lancé

### Après urgence-demographie :
- Population > 50 000 ? → Signaler évacuation massive, vérifier urgence-hopitaux
- EHPAD détectés ? → Mentionner évacuation médicalisée prioritaire
- Écoles détectées ? → Mentionner coordination rectorat

### Après urgence-meteo :
- Alerte ROUGE vent ? → Le nuage toxique (si incident chimique) se propage plus vite
- Alerte ORANGE ou ROUGE ? → Mentionner impact sur les opérations de secours

### Après urgence-hopitaux :
- Aucun établissement avec urgences 24h dans les 30 min ? → Recommander hélicoptère SMUR
- Spécialité non trouvée en local ? → Signaler besoin de transfert inter-régional

---

## PHASE 4 — ROUTAGE CONDITIONNEL (si nécessaire)

Si les résultats révèlent un risque non anticipé en Phase 1, lancer les agents supplémentaires :

- Résultats risques montrent SEVESO + demographie montre EHPAD → urgence-hopitaux `--specialite grands_brules` ET signaler évacuation médicalisée
- Résultats météo ROUGE + incident chimique → doubler le rayon de sécurité, relancer demographie
- Résultats réseaux montrent 4G < 70% → recommander radios VHF pour coordination terrain

---

## PHASE 5 — SYNTHÈSE FINALE

Après avoir collecté et analysé tous les résultats, produit un rapport structuré :

```markdown
# BRIEFING URGENCE — [Lieu] · [Date/Heure]

## Niveau de danger global : [🔴 CRITIQUE / 🟠 ÉLEVÉ / 🟡 MODÉRÉ / 🟢 FAIBLE]
**Justification** : [1-2 phrases expliquant pourquoi ce niveau]

---
[Sections des agents activés, dans l'ordre de priorité]
---

## Actions immédiates (prochaines 30 minutes)
1. [Action la plus urgente avec responsable]
2. [...]
3. [...]

## Contacts prioritaires
- SAMU : 15 | Pompiers : 18 | Gendarmerie : 17 | Numéro européen : 112
- [Contacts spécifiques selon résultats : Préfet si SEVESO, DREAL, etc.]

## Points d'attention
- [Risques combinés identifiés pendant le workflow]
- [Populations vulnérables spécifiques]
- [Lacunes d'information à combler]
```

---

## Chemins des scripts

Les skills sont installés dans `~/.claude/skills/`. Utilise toujours les chemins absolus :

```
python3 ~/.claude/skills/urgence-meteo/main.py --dept <num>
python3 ~/.claude/skills/urgence-demographie/main.py --lat <lat> --lon <lon> --rayon <km>
python3 ~/.claude/skills/urgence-hopitaux/main.py --lat <lat> --lon <lon> --specialite <spec>
python3 ~/.claude/skills/urgence-reseaux/main.py --lat <lat> --lon <lon>
python3 ~/.claude/skills/urgence-risques-industriels/main.py --lat <lat> --lon <lon> --rayon <km>
```

Si `~` ne se résout pas (Windows PowerShell natif), utilise `$HOME` ou `$env:USERPROFILE` :
```
python $HOME/.claude/skills/urgence-meteo/main.py --dept <num>
```

En cas de doute sur l'emplacement exact, localise les scripts avec :
```bash
ls ~/.claude/skills/urgence-*/main.py
```
