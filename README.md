# Croissance économique et Santé
---

##### Projet réalisé par Thibaut LAUNAY, Jeanne LEMASSON et Christophe REY
---

## I. Définitions

Dans ce projet, la **croissance économique** est appréhendée à travers le **Produit Intérieur Brut (PIB) par habitant**.  
Le PIB par habitant correspond au **PIB total d’un pays rapporté à sa population**. Il constitue un indicateur synthétique couramment utilisé pour mesurer le **niveau moyen de richesse économique** et le **niveau de vie potentiel** d’un pays.

Cet indicateur est largement mobilisé dans la littérature économique et par les institutions internationales, notamment la **Banque mondiale**, comme proxy du développement économique, bien qu’il ne rende pas compte des inégalités internes ni de l’ensemble des dimensions du bien-être.

## II. Objectifs

L’objectif principal de ce projet est d’**étudier les relations entre différents indicateurs de santé et la croissance économique**, mesurée par le **PIB par habitant**.  
L’analyse vise à identifier d’éventuelles corrélations, disparités ou tendances entre le niveau de richesse économique des pays et leurs performances en matière de santé.

## III. Sources des données

Les données utilisées proviennent de sources suivantes :

 - des **indicateurs de santé issus des bases SDG et SDG3**, fournis par l’**Organisation Mondiale de la Santé (OMS)**, relatifs notamment à la mortalité, à la nutrition et à l’accès aux soins ;

 - des **données de santé mentale issues de l’Institute for Health Metrics and Evaluation (IHME)**. L’IHME est un centre de recherche international spécialisé dans la mesure comparative de la charge mondiale des maladies. Les indicateurs mobilisés sont exprimés en **DALYs (Disability-Adjusted Life Years)**, qui mesurent la charge totale de morbidité en combinant les années de vie perdues par mortalité prématurée et les années vécues avec incapacité ;

 - des **données de PIB par habitant** provenant de la **World Bank**, utilisées comme mesure standardisée de la richesse économique des pays.

## IV. Présentation du dépôt 

Notre production est essentiellement localisée dans un fichier **main.ipynb**.

Ce fichier utilise des sauvegardes locales afin de pouvoir présenter les résultats même en cas  d'inaccessibilité temporaire des sources. En effet, une des API  a été indisponibles pendant quelques jours durant le projet, ce qui nous a contraint à trouver une solution pour que cela ne soit pas le cas durant la correction.

Cependant, le code a été pensé pour que dans le cas où les sources sont disponibles, ce soit les API qui soient utilisés.

Ce fichier **main.ipynb** tient lieu de **rapport final**.

Les sauvegardes locales des données et les données apportées sous format csv sont stockées dans les dossiers : 
 - **Données Income group**
 - **Données_fusionnées**
 - **Données_IHME**
 - **Données OMS**
 - **Données_PIB**


Le dossier Scripts contient une multitude de fonctions, afin de rendre notre main plus lisible.

Enfin, une cellule de préparation des données  installe la bibliothèque **pycountry**, puis importe l’ensemble des packages Python nécessaires à l’analyse, la manipulation de données, la visualisation graphique, le clustering et les appels à des API externes.
Elle charge également les fonctions et modules développés dans le projet permettant d’exécuter les traitements, analyses et visualisations dans les cellules suivantes du main.