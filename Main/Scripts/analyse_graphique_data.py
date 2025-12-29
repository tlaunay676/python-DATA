import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

def afficher_graphiques(liste_indicateurs, df,disposition="1"):
    """
    Affiche plusieurs graphiques selon la disposition choisie,
    Effectue soit une régression linéaire par rapport au PIB par habitant soit un histogramme par groupe de revenu.

    Paramètres
    ----------
    liste_indicateurs : list of tuples
        Liste contenant des tuples de la forme (nom_colonne, var, titre, type_graphique, année_des_données) où :
        - nom_colonne : str, nom de la colonne à analyser
        - var : str, description de la variable
        - titre : str, titre du graphique
        - type_graphique : str, "regression" pour un nuage de points avec régression,
                           "barres" pour un histogramme par groupe de revenu
        - année_des_données : str, pour avoir les données de PIB par habitant de l'année correspondante
    df : pandas.DataFrame
        DataFrame contenant les données à visualiser.
    disposition : str, optional
        Choix de la disposition des graphiques : 
        - "1" pour un seul graphique,
        - "2" pour deux graphiques côte à côte.

    Sortie
    ------
    Affiche les graphiques demandés et, si applicable, résume les résultats des régressions dans la console.
    """

    # Nombre de graphiques à afficher
    nb_graphiques = len(liste_indicateurs)

    # Vérification de la cohérence entre le nombre de graphiques et la disposition
    if disposition == "1" and nb_graphiques != 1:
        print("Disposition '1' : fournir exactement 1 indicateur")
        return
    elif disposition == "2" and nb_graphiques != 2:
        print("Disposition '2' : fournir exactement 2 indicateurs")
        return

    # Création de la figure et des axes selon la disposition
    if disposition == "1":
        fig = plt.figure(figsize=(10, 7))
        axes = [fig.add_subplot(1, 1, 1)]
    elif disposition == "2":
        fig = plt.figure(figsize=(16, 6))
        axes = [fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)]
    else:
        print("Disposition invalide")
        return

    # Liste pour stocker les résultats de régressions
    resultats_list = []

    # Boucle sur chaque indicateur à visualiser
    for idx, (nom_col, var, titre, pib, type_graph) in enumerate(liste_indicateurs):
        try:
            # Nettoyage des données : suppression des lignes avec NaN et valeurs <= 0 pour pib et la variable
            df = df.dropna(subset=[pib, nom_col])
            df = df[df[pib] > 0]

            # Transformation logarithmique du PIB pour linéariser la relation
            df['log_PIB'] = np.log(df[pib])

            # Suppression des éventuelles lignes encore NaN après transformation
            df = df.dropna(subset=['log_PIB', nom_col])

            # Préparation des variables pour la régression
            Y = df[nom_col]
            X = sm.add_constant(df['log_PIB'])
            resultats = sm.OLS(Y, X).fit(cov_type='HC1')  # Régression linéaire avec correction d'hétéroscédasticité
            resultats_list.append((var, resultats))

            # Récupération de l'axe correspondant au graphique courant
            ax = axes[idx]

            # Nuage de points avec régression
            if type_graph == "regression":
                ax.scatter(df['log_PIB'], df[nom_col], alpha=0.5, color='#2ecc71')
                ax.plot(df['log_PIB'], resultats.predict(), color='red', linewidth=2)
                ax.set_xlabel(f"Richesse (Log PIB par habitant de {pib})", fontsize=9)
                ax.set_ylabel(var, fontsize=9)
                ax.grid(True, linestyle='--', alpha=0.6)

            # Histogramme moyen par groupe de revenu
            elif type_graph == "barres":
                # Nettoyage et conversion en numérique
                df.columns = df.columns.str.strip()
                df[nom_col] = pd.to_numeric(df[nom_col], errors='coerce')

                # Calcul de la moyenne par groupe de revenu
                resultat_moyen = df.groupby('IncomeGroup')[nom_col].mean().sort_values()

                # Création du graphique en barres
                bars = ax.bar(resultat_moyen.index, resultat_moyen.values, color='#87CEEB',
                             edgecolor='#5A9AB4', linewidth=1.5, alpha=0.85)
                ax.set_ylabel(var, fontsize=9)
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
                ax.grid(axis='y', linestyle='--', alpha=0.7)

            # Ajout du titre du graphique
            ax.set_title(f"{titre}", fontsize=11, fontweight='bold')

        except Exception as e:
            print(f"Erreur pour {titre}: {e}")

    # Ajustement automatique des espacements et affichage des graphiques
    plt.tight_layout()
    plt.show()

    # Affichage résumé des résultats de régressions
    print("\n" + "="*70)
    print("RESUME DES REGRESSIONS")
    print("="*70)
    for var, res in resultats_list:
        print(f"\n{var}")
        print("-" * 70)
        print(res.summary())
