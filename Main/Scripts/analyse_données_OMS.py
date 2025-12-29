import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def description_indicateurs(df, variables, disposition="1"):
    """
    Paramètres
    ----------
    df : pandas.DataFrame
        DataFrame contenant les données à analyser.
    variables : list
        Liste des colonnes numériques du DataFrame à analyser.
    disposition : str, optional
        "1" ou "2" pour déterminer la disposition des boxplots (par défaut "1").

    Sortie
    ------
    None
        Affiche les statistiques descriptives (moyenne, médiane, min, max, écart-type)
        et les boxplots des variables fournies, avec la disposition choisie.
    """

    # Filtrage des variables existantes dans le DataFrame
    variables = [v for v in variables if v in df.columns]

    # Calcul des statistiques descriptives pour chaque variable
    stats = pd.DataFrame({
        "Moyenne": df[variables].mean(),
        "Médiane": df[variables].median(),
        "Minimum": df[variables].min(),
        "Maximum": df[variables].max(),
        "Écart-type": df[variables].std()
    })

    # Affichage des statistiques arrondies à 2 décimales
    print("Statistiques descriptives :\n")
    print(stats.round(2))

    # Détermination de la disposition des boxplots
    if disposition == "1":
        ncols, nrows, figsize = 1, 1, (5, 4)  # 1 plot par figure
    elif disposition == "2":
        ncols, nrows, figsize = 2, 1, (10, 4)  # 2 plots côte à côte
    else:
        raise ValueError("Disposition invalide : choisir '1' ou '2'")

    # Boucle pour créer les boxplots par sous-ensemble de variables
    for i in range(0, len(variables), ncols * nrows):
        subset = variables[i:i + ncols * nrows]

        # Création de la figure et des axes
        fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
        axes = np.array(axes).reshape(-1)  # Conversion en tableau 1D pour faciliter l'itération

        # Pour chaque variable du sous-ensemble, création d'un boxplot
        for ax, var in zip(axes, subset):
            ax.boxplot(df[var].dropna(), vert=True)  # Suppression des NaN pour le plot
            ax.set_title(f"{var}", fontsize=10)  # Titre du boxplot
            ax.set_ylabel(var)  # Label de l'axe y
            ax.grid(axis="y", linestyle="--", alpha=0.6)

        plt.tight_layout()  # Ajustement automatique des espacements
        plt.show()


def world_map(dataframe, y_col, country_code_col="Pays_code_iso3", country_name_col="LOCATION", data_name=None, width=900, height=500):
    """
    Paramètres
    ----------
    dataframe : pandas.DataFrame
        DataFrame contenant les données à visualiser.
    y_col : str
        Nom de la colonne à représenter sur la carte.
    country_code_col : str, optional
        Colonne contenant les codes pays ISO3 (par défaut "Pays_code_iso3").
    country_name_col : str, optional
        Colonne contenant le nom des pays (par défaut "LOCATION").
    data_name : str, optional
        Titre de la carte (par défaut, utilise y_col).
    width : int, optional
        Largeur de la figure (par défaut 900).
    height : int, optional
        Hauteur de la figure (par défaut 500).

    Sortie
    ------
    Affiche une carte du monde avec la distribution des valeurs de y_col par pays.
    """

    # Détermination de l'étendue des couleurs selon les valeurs minimales et maximales
    min_value = dataframe[y_col].min()
    max_value = dataframe[y_col].max()

    # Création de la carte  avec Plotly Express
    fig = px.choropleth(
        dataframe,
        locations=country_code_col,  # Codes ISO3 pour identifier les pays
        color=y_col,
        hover_name=country_name_col,
        color_continuous_scale="turbo",
        projection="natural earth",
        range_color=(min_value, max_value)
    )

    # Personnalisation de la mise en page de la carte
    fig.update_layout(
        title_text=data_name if data_name else y_col,  # Titre de la carte
        geo=dict(
            showcoastlines=True,  # Afficher les côtes
            coastlinecolor="Black",  # Couleur des côtes
            showland=True,  # Afficher les terres
            landcolor="white",  # Couleur des terres
        ),
        width=width,
        height=height
    )

    # Retirer le titre de la colorbar
    fig.update_coloraxes(colorbar_title_text="")

    fig.show()

def desc_missing_health(df, var, country_col):
    """
    Description textuelle des valeurs manquantes d'une colonne de données de santé dans un DataFrame.

    Paramètres
    ----------
    df : pandas.DataFrame
        DataFrame contenant les données.
    var : str
        Nom de la colonne correspondant à la variable de santé.
    country_col : str
        Colonne contenant les noms ou codes des pays.

    Sortie
    ------
    Affiche le nombre de pays, le nombre de valeurs manquantes et le pourcentage de valeurs manquantes.
    """

    # Comptage du nombre de pays uniques
    n_countries = df[country_col].nunique()

    # Comptage du nombre de valeurs manquantes
    n_missing = df[var].isna().sum()

    # Calcul du pourcentage de valeurs manquantes par rapport au nombre de pays
    pct_missing = (n_missing / n_countries) * 100

    # Affichage formaté des informations
    print(f"The dataframe includes {n_countries} countries and {n_missing} missing values.\n"
          f"The percentage of missing values for {var} in the dataset is {pct_missing:.2f}%.")