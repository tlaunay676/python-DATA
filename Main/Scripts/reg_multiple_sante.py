import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def analyse_sante_vers_pib(df, annee_pib='2021'):
    """
    Régression multiple : Y = PIB, X = [Espérance de vie, Mortalité, Dépenses santé]
    Montre l'effet SIMULTANÉ des 3 indicateurs sur le PIB.
    """
    indicateurs = ['Espérance de vie totale', 'Taux mortalité brute', 'Dépenses publiques santé']
    
    df_reg = df.dropna(subset=[annee_pib] + indicateurs).copy()
    df_reg = df_reg[df_reg[annee_pib] > 0]
    
    Y = np.log(df_reg[annee_pib])
    X = df_reg[indicateurs]
    X = sm.add_constant(X)
    
    model = sm.OLS(Y, X).fit(cov_type='HC1')
    
    print(f"\n--- REGRESSION MULTIPLE : SANTE -> PIB ({annee_pib}) ---")
    print(f"Nombre de pays : {len(df_reg)}")
    print(f"\nModèle : Log(PIB) = β0 + β1×Espérance + β2×Mortalité + β3×Dépenses\n")
    print(model.summary())
    
    return model, df_reg


def graphique_valeurs_predites_vs_reelles(model, df_reg, annee_pib='2021'):
    """
    Graphique unique : Valeurs prédites vs réelles
    Montre la qualité de la régression multiple.
    """
    Y_obs = np.log(df_reg[annee_pib])
    Y_pred = model.fittedvalues
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    ax.scatter(Y_pred, Y_obs, alpha=0.6, color='#2ecc71', s=80, edgecolors='#1e8449', linewidth=0.5)
    
    min_val = min(Y_obs.min(), Y_pred.min())
    max_val = max(Y_obs.max(), Y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Prédiction parfaite')
    
    ax.set_xlabel('Log(PIB) prédit par le modèle', fontsize=12)
    ax.set_ylabel('Log(PIB) réel observé', fontsize=12)
    ax.set_title('Qualité de la régression multiple\nSanté → PIB', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    r2 = model.rsquared
    ax.text(0.05, 0.95, f'R² = {r2:.3f}', transform=ax.transAxes, 
            fontsize=12, verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.show()


def graphique_coefficients(model):
    """
    Graphique en barres des coefficients β avec leurs intervalles de confiance.
    """
    params = model.params.drop('const')
    conf_int = model.conf_int().drop('const')
    errors = conf_int[1] - params
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x_pos = np.arange(len(params))
    colors = ['#27ae60' if p > 0 else '#e74c3c' for p in params]
    
    ax.bar(x_pos, params, yerr=errors, capsize=5, alpha=0.7, 
           color=colors, edgecolor='black', linewidth=1.2)
    
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(params.index, rotation=15, ha='right')
    ax.set_ylabel('Coefficient β', fontsize=12)
    ax.set_title('Impact des indicateurs de santé sur le PIB\n(avec intervalles de confiance à 95%)', 
                 fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()