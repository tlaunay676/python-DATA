import pandas as pd
import sys
import subprocess

def restructure_data(input_path):
    """
    Transforme un fichier CSV de données de DALYs en format large pour analyse par pays et maladie.

    Paramètres
    ----------
    input_path : str
        Chemin vers le fichier CSV contenant les données brutes. 
        Le CSV doit inclure au moins les colonnes 'LOCATION', 'cause' et 'val'.

    Sortie
    ------
    pandas.DataFrame
        DataFrame transformé au format large :
        - Chaque ligne correspond à un pays unique.
        - Chaque colonne correspond à une maladie (cause).
        - Les valeurs sont le nombre de DALYs.
    """

    # Étape 1 : Lecture du fichier CSV
    df = pd.read_csv(input_path)

    # Sélection des colonnes essentielles pour le pivot
    # 'LOCATION' : nom du pays
    # 'cause'    : maladie ou cause de DALYs
    # 'val'      : nombre de DALYs
    df_reduced = df[['LOCATION', 'cause', 'val']]

    # Transformation en format large (pivot)
    # - index='LOCATION' : chaque pays devient une ligne unique
    # - columns='cause' : chaque cause devient une colonne
    # - values='val'    : remplit les cases avec le nombre de DALYs
    df_wide = df_reduced.pivot(index='LOCATION', columns='cause', values='val')

    # Remise à plat de l'index pour avoir une colonne 'LOCATION' normale
    df_wide = df_wide.reset_index()

    # Nettoyage des noms de colonnes
    # Remplace les espaces et caractères spéciaux pour rendre les noms compatibles avec pandas
    df_wide.columns = [
        str(col).replace(' ', '_')      # Remplace espace par underscore
                .replace('-', '_')      # Remplace tiret par underscore
                .replace('/', '_')      # Remplace slash par underscore
                .replace('(', '')       # Supprime parenthèse ouvrante
                .replace(')', '')       # Supprime parenthèse fermante
                .replace("'", "")       # Supprime apostrophe
        for col in df_wide.columns
    ]

    df_wide = df_wide.rename(columns={'location_name': 'Country'})

    return df_wide
