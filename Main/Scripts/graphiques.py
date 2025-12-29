import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

def afficher_graphiques(liste_indicateurs, df, disposition="1"):
    """
    Affiche plusieurs graphiques selon la disposition choisie.
    
    liste_indicateurs : Liste de tuples (nom_colonne, titre, type_graphique)
    disposition : "1", "2"
    """
    
    nb_graphiques = len(liste_indicateurs)
    
    if disposition == "1" and nb_graphiques != 1:
        print("Disposition '1' : fournir exactement 1 indicateur")
        return
    elif disposition == "2" and nb_graphiques != 2:
        print("Disposition '2' : fournir exactement 2 indicateurs")
        return
    
    if disposition == "1":
        fig = plt.figure(figsize=(10, 7))
        axes = [fig.add_subplot(1, 1, 1)]
    elif disposition == "2":
        fig = plt.figure(figsize=(16, 6))
        axes = [fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)]
    else:
        print("Disposition invalide")
        return
    
    resultats_list = []
    
    for idx, (nom_col, titre, type_graph) in enumerate(liste_indicateurs):
        try:
            
            df = df.dropna(subset=['2021', nom_col])
            df = df[df['2021'] > 0]
            df['log_PIB'] = np.log(df['2021'])
            df = df.dropna(subset=['log_PIB', nom_col])

            Y = df[nom_col]
            X = sm.add_constant(df['log_PIB'])
            resultats = sm.OLS(Y, X).fit(cov_type='HC1')
            resultats_list.append((titre, resultats))

            ax = axes[idx]
            
            if type_graph == "regression":
                ax.scatter(df['log_PIB'], df[nom_col], alpha=0.5, color='#2ecc71')
                ax.plot(df['log_PIB'], resultats.predict(), color='red', linewidth=2)
                ax.set_xlabel("Richesse (Log PIB)", fontsize=9)
                ax.set_ylabel(titre, fontsize=9)
                ax.grid(True, linestyle='--', alpha=0.6)
                
            elif type_graph == "barres":
                df.columns = df.columns.str.strip()
                df[nom_col] = pd.to_numeric(df[nom_col], errors='coerce')
                resultat_moyen = df.groupby('IncomeGroup')[nom_col].mean().sort_values()
                
                bars = ax.bar(resultat_moyen.index, resultat_moyen.values, color='#87CEEB', 
                             edgecolor='#5A9AB4', linewidth=1.5, alpha=0.85)
                ax.set_ylabel(titre, fontsize=9)
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
                ax.grid(axis='y', linestyle='--', alpha=0.7)
            
            ax.set_title(f"{titre}", fontsize=11, fontweight='bold')
            
        except Exception as e:
            print(f"Erreur pour {titre}: {e}")

    plt.tight_layout()
    plt.show()
    
    print("\n" + "="*70)
    print("RESUME DES REGRESSIONS")
    print("="*70)
    for titre, res in resultats_list:
        print(f"\n{titre}")
        print("-" * 70)
        print(res.summary())
        print()