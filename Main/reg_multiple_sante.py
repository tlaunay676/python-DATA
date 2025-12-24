import numpy as np
import statsmodels.api as sm

def analyse_sante_vers_pib(df, annee_pib='2021'):
    """
    Réaliser une régression multiple pour montrer l'impact de la santé sur le PIB.
    """
    indicateurs = ['Espérance de vie totale', 'Taux mortalité brute', 'Dépenses publiques santé']
    
    # Nettoyage des données pour cette analyse spécifique
    df_reg = df.dropna(subset=[annee_pib] + indicateurs)
    df_reg = df_reg[df_reg[annee_pib] > 0]
    
    # Variables
    Y = np.log(df_reg[annee_pib])
    X = df_reg[indicateurs]
    X = sm.add_constant(X)
    
    # Modèle
    model = sm.OLS(Y, X).fit(cov_type='HC1')
    
    print(f"\n--- ANALYSE : LA SANTÉ COMME MOTEUR DU PIB ({annee_pib}) ---")
    print(f"Nombre de pays analysés : {len(df_reg)}")
    print(model.summary())
    
    return model