import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def analyse_sante_vers_pib(df, annee_pib='2021'):
    """
    Réalise une régression multiple pour étudier l'effet simultané de plusieurs indicateurs de santé sur le PIB.

    Paramètres
    ----------
    df : pandas.DataFrame
        DataFrame contenant les colonnes suivantes :
        - PIB pour l'année spécifiée (annee_pib)
        - Espérance de vie totale
        - Taux mortalité brute
        - Dépenses publiques santé
    annee_pib : str, optional
        Année du PIB à utiliser (par défaut '2021').

    Sortie
    ------
    model : statsmodels.regression.linear_model.RegressionResultsWrapper
        Objet contenant les résultats de la régression OLS.
    df_reg : pandas.DataFrame
        DataFrame filtré utilisé pour la régression (sans valeurs manquantes et PIB > 0).
    """

    # Définition des variables explicatives
    indicateurs = ['Espérance de vie totale', 'Taux mortalité brute', 'Dépenses publiques santé']
    
    # Suppression des lignes avec valeurs manquantes pour le PIB et les indicateurs
    df_reg = df.dropna(subset=[annee_pib] + indicateurs).copy()
    # On ne garde que les pays dont le PIB est strictement positif
    df_reg = df_reg[df_reg[annee_pib] > 0]
    
    # Variable dépendante : logarithme du PIB
    Y = np.log(df_reg[annee_pib])
    # Variables explicatives
    X = df_reg[indicateurs]
    # Ajout de la constante pour le modèle OLS
    X = sm.add_constant(X)
    
    # Ajustement du modèle de régression OLS avec estimation robuste (HC1)
    model = sm.OLS(Y, X).fit(cov_type='HC1')
    
    # Affichage d’un résumé clair
    print(f"\n--- REGRESSION MULTIPLE : SANTE -> PIB ({annee_pib}) ---")
    print(f"Nombre de pays : {len(df_reg)}")
    print(f"\nModèle : Log(PIB) = β0 + β1×Espérance + β2×Mortalité + β3×Dépenses\n")
    print(model.summary())
    
    return model, df_reg


def graphique_valeurs_predites_vs_reelles(model, df_reg, annee_pib='2021'):
    """
    Affiche un graphique comparant les valeurs de PIB prédites par le modèle et les valeurs réelles observées.

    Paramètres
    ----------
    model : statsmodels.regression.linear_model.RegressionResultsWrapper
        Résultats de la régression multiple.
    df_reg : pandas.DataFrame
        DataFrame utilisé pour la régression.
    annee_pib : str, optional
        Année du PIB à utiliser pour les valeurs réelles (par défaut '2021').

    Sortie
    ------
    Affiche un graphique de dispersion et la ligne de prédiction parfaite.
    """

    # Valeurs observées (log du PIB réel)
    Y_obs = np.log(df_reg[annee_pib])
    # Valeurs prédites par le modèle
    Y_pred = model.fittedvalues
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Nuage de points prédit vs réel
    ax.scatter(Y_pred, Y_obs, alpha=0.6, color='#2ecc71', s=80, edgecolors='#1e8449', linewidth=0.5)
    
    # Ligne représentant la prédiction parfaite
    min_val = min(Y_obs.min(), Y_pred.min())
    max_val = max(Y_obs.max(), Y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Prédiction parfaite')
    
    # Paramètres d'affichage
    ax.set_xlabel('Log(PIB) prédit par le modèle', fontsize=12)
    ax.set_ylabel('Log(PIB) réel observé', fontsize=12)
    ax.set_title('Qualité de la régression multiple\nSanté → PIB', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Affichage du R² sur le graphique
    r2 = model.rsquared
    ax.text(0.05, 0.95, f'R² = {r2:.3f}', transform=ax.transAxes, 
            fontsize=12, verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.show()


def graphique_coefficients(model):
    """
    Affiche un graphique en barres des coefficients de la régression avec leurs intervalles de confiance à 95%.

    Paramètres
    ----------
    model : statsmodels.regression.linear_model.RegressionResultsWrapper
        Résultats de la régression multiple.

    Sortie
    ------
    Affiche un graphique en barres des coefficients β.
    """

    # Extraction des coefficients et des intervalles de confiance, excluant la constante
    params = model.params.drop('const')
    conf_int = model.conf_int().drop('const')
    errors = conf_int[1] - params  # Calcul des erreurs pour les barres d'erreur
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Positions des barres
    x_pos = np.arange(len(params))
    # Couleur : vert si coefficient positif, rouge si négatif
    colors = ['#27ae60' if p > 0 else '#e74c3c' for p in params]
    
    # Création du graphique en barres avec intervalles de confiance
    ax.bar(x_pos, params, yerr=errors, capsize=5, alpha=0.7, 
           color=colors, edgecolor='black', linewidth=1.2)
    
    # Ligne horizontale à 0
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(params.index, rotation=15, ha='right')
    ax.set_ylabel('Coefficient β', fontsize=12)
    ax.set_title('Impact des indicateurs de santé sur le PIB\n(avec intervalles de confiance à 95%)', 
                 fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()