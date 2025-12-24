import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def analyse_sante_vers_pib(df, annee_pib='2021'):
    indicateurs = ['Espérance de vie totale', 'Taux mortalité brute', 'Dépenses publiques santé']
    
    # Nettoyage
    df_reg = df.dropna(subset=[annee_pib] + indicateurs).copy()
    df_reg = df_reg[df_reg[annee_pib] > 0]
    
    Y = np.log(df_reg[annee_pib])
    X = df_reg[indicateurs]
    X = sm.add_constant(X)
    
    model = sm.OLS(Y, X).fit(cov_type='HC1')
    return model, df_reg


def graphique_regression_multiple(model, df_reg, indicateurs, annee_pib='2021'):
    n_vars = len(indicateurs)
    fig, axes = plt.subplots(1, n_vars, figsize=(6*n_vars, 5))
    
    if n_vars == 1: axes = [axes]
    
    Y_obs = np.log(df_reg[annee_pib])
    
    for idx, var in enumerate(indicateurs):
        ax = axes[idx]
        
        # On trace les points réels
        ax.scatter(df_reg[var], Y_obs, alpha=0.4, color='#2ecc71', label='Données réelles')
        
        # Ligne de tendance simplifiée (pente de la régression)
        # On ajuste l'ordonnée à l'origine pour que la ligne passe au milieu des points
        pente = model.params[var]
        intercept_visuel = Y_obs.mean() - pente * df_reg[var].mean()
        
        x_range = np.linspace(df_reg[var].min(), df_reg[var].max(), 100)
        y_range = intercept_visuel + pente * x_range
        
        ax.plot(x_range, y_range, color='red', linewidth=2, label=f'Pente: {pente:.2f}')
        
        ax.set_xlabel(var)
        ax.set_ylabel(f'Log(PIB {annee_pib})')
        ax.set_title(f'Influence de {var}')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

# --- SI TU LANCES CE FICHIER DIRECTEMENT ---
if __name__ == "__main__":
    try:
        chemin = "/home/onyxia/work/python-DATA/données_sante_mentale/Table_complète.csv"
        df = pd.read_csv(chemin)
        
        indicateurs = ['Espérance de vie totale', 'Taux mortalité brute', 'Dépenses publiques santé']
        model, df_clean = analyse_sante_vers_pib(df)
        
        print(model.summary())
        graphique_regression_multiple(model, df_clean, indicateurs)
    except FileNotFoundError:
        print("Erreur : Le fichier CSV est introuvable. Vérifie le chemin.")
    except KeyError as e:
        print(f"Erreur : La colonne {e} n'existe pas dans le CSV.")