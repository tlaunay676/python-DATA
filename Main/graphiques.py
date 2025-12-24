import pandas as pd
import matplotlib.pyplot as plt
import sys

# ==========================================
#               CONFIGURATION
# ==========================================

# Le nom de ton fichier (doit être dans le même dossier)
FICHIER_CSV = 'Données_taux_pauvreté/Table_groupes_pays_richesse.csv'

# Argument 1 : La colonne pour faire les groupes (ex: Pays riches, pauvres...)
COLONNE_GROUPE = 'IncomeGroup'

# Argument 2 : La colonne dont on veut la moyenne
COLONNE_VALEUR = 'Espérance de vie en bonne santé totale'

# Le titre de l'axe vertical (Y)
TITRE_AXE_Y = 'Espérance de vie moyenne en bonne santé (années)'

# ==========================================

def esperancetotale():
    print("--- Démarrage du programme ---")

    # 1. Chargement des données
    try:
        # On essaie de lire le CSV. 
        # Si ton fichier CSV sépare les colonnes par des points-virgules, remplace sep=',' par sep=';'
        df = pd.read_csv(FICHIER_CSV, sep=',') 
        print(f"--> Fichier '{FICHIER_CSV}' chargé avec succès ({len(df)} lignes).")
    except FileNotFoundError:
        print(f"ERREUR : Le fichier '{FICHIER_CSV}' est introuvable.")
        print("Vérifie que le fichier est bien dans le même dossier que ce script Python.")
        sys.exit(1)

    # 2. Vérification que les colonnes existent
    # On nettoie les espaces potentiels dans les noms de colonnes du fichier pour éviter des erreurs bêtes
    df.columns = df.columns.str.strip() 
    
    if COLONNE_GROUPE not in df.columns or COLONNE_VALEUR not in df.columns:
        print(f"ERREUR : Une des colonnes demandées n'existe pas dans le fichier.")
        print(f"Tu as demandé : '{COLONNE_GROUPE}' et '{COLONNE_VALEUR}'")
        print(f"Colonnes trouvées dans le fichier : {list(df.columns)}")
        sys.exit(1)

    # 3. Nettoyage et Calculs
    print("--> Nettoyage des données...")
    
    # On retire les lignes où la colonne de groupe est vide
    df_clean = df.dropna(subset=[COLONNE_GROUPE]).copy()
    
    # On convertit la colonne valeur en nombres (au cas où il y ait du texte qui gêne)
    df_clean[COLONNE_VALEUR] = pd.to_numeric(df_clean[COLONNE_VALEUR], errors='coerce')
    
    # Groupement et calcul de la moyenne
    print(f"--> Calcul de la moyenne de '{COLONNE_VALEUR}' par groupe...")
    resultat = df_clean.groupby(COLONNE_GROUPE)[COLONNE_VALEUR].mean().sort_values()

    print("\nRésultats :")
    print(resultat)

    # 4. Création du graphique
    plt.figure(figsize=(10, 6))
    
    # Création des bâtons
    plt.bar(resultat.index, resultat.values, color='#4c72b0', edgecolor='black')

    # Mises en forme
    plt.xlabel(COLONNE_GROUPE, fontsize=12, fontweight='bold')
    plt.ylabel(TITRE_AXE_Y, fontsize=12, fontweight='bold')
    plt.title(f"Graphique : {TITRE_AXE_Y} selon le niveau de richesse", fontsize=14)
    
    # Rotation des étiquettes en bas pour qu'elles soient lisibles
    plt.xticks(rotation=45, ha='right')
    
    # Grille
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    print("--> Affichage du graphique.")
    plt.show()

if __name__ == "__main__":
    esperancetotale()