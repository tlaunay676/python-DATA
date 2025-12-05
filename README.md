# Santé & Croissance Économique

## Introduction 

Ce projet vise à **étudier les liens entre différents indicateurs de santé et la croissance économique**, mesurée via le PIB.  
Pour cela, nous avons récupéré :
- des **données de santé SDG et SDG3** issues de l’**Organisation Mondiale de la Santé (OMS)** ;
- des **données de PIB par habitant** provenant de l’**OCDE**.

Le premier objectif est de créer un jeu de données propre, harmonisé et exploitable pour des analyses statistiques ou des modèles prédictifs.

---
## Rendre les données exploitables

1. **Récupérer automatiquement** des indicateurs clés de santé depuis le portail de l’OMS (scraping).
2. **Nettoyer et harmoniser** les données de PIB téléchargées depuis l’OCDE (à terme essayer d'utiliser l'API de l'OCDE) et les données de l'OMS.
3. **Fusionner les deux sources** dans un jeu de données prêt pour l'analyse.

---

## 1. Scraping des données OMS

### Étapes
- Requête HTTP vers les pages ou endpoints contenant les tables OMS.
- Extraction automatique des tableaux via **BeautifulSoup**.
- Standardisation des colonnes (noms, formats, types numériques). (à faire car tableau illisible pour quelqu'un n'ayant pas travailler dessus)
- Nettoyage :
  - gestion des valeurs manquantes,
  - conversion en format numérique,
  - harmonisation des codes pays.
