import pandas as pd
import sys
import subprocess

def restructure_data(input_path):

    df = pd.read_csv(input_path)
    
    # On ne garde que les 3 colonnes essentielles pour le pivot
    # 'val' contient le nombre de DALYs, 'cause' la maladie, 'location' le pays
    df_reduced = df[['LOCATION', 'cause', 'val']]
    

    # - index='location_' : Chaque pays devient une ligne unique
    # - columns='cause' : Chaque maladie devient une colonne
    # - values='val' : On remplit les cases avec le nombre de DALYs
    df_wide = df_reduced.pivot(index='LOCATION', columns='cause', values='val')
    
    # Après un pivot, l'index est complexe, on le remet à plat pour avoir une colonne 'Pays' normale
    df_wide = df_wide.reset_index()
    
    # 3. Nettoyage des noms de colonnes)
    df_wide.columns = [
        str(col).replace(' ', '_')      # Remplace espace par _
                .replace('-', '_')      # Remplace tiret par _
                .replace('/', '_')      # Remplace slash par _
                .replace('(', '')       # Enlève parenthèse ouvrante
                .replace(')', '')       # Enlève parenthèse fermante
                .replace("'", "")       # Enlève apostrophe
        for col in df_wide.columns
    ]
    
    # On renomme la colonne pays pour que le tableau de données soit clair
    df_wide = df_wide.rename(columns={'location_name': 'Country'})
    
    return df_wide