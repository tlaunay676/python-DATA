import plotly.express as px

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def description_indicateurs(df, variables, disposition="1"):
    """
    Décrit des indicateurs de santé à l'aide de statistiques simples
    et de boxplots avec disposition configurable.

    Paramètres
    ----------
    df : pandas.DataFrame
        DataFrame contenant les données
    variables : list
        Liste des colonnes numériques à analyser
    disposition : str
        "1" ou "2" pour la disposition des boxplots
    """

    # Vérification des variables
    variables = [v for v in variables if v in df.columns]
    if not variables:
        raise ValueError("Aucune variable valide fournie.")

    # Statistiques descriptives
    stats = pd.DataFrame({
        "Moyenne": df[variables].mean(),
        "Médiane": df[variables].median(),
        "Minimum": df[variables].min(),
        "Maximum": df[variables].max(),
        "Écart-type": df[variables].std()
    })

    print("Statistiques descriptives :\n")
    print(stats.round(2))

    # Définition des layouts
    if disposition == "1":
        ncols, nrows, figsize = 1, 1, (5, 4)
    elif disposition == "2":
        ncols, nrows, figsize = 2, 1, (10, 4)
    elif disposition == "3":
        ncols, nrows, figsize = 3, 1, (15, 4)
    else:
        raise ValueError("Disposition invalide : choisir '1', '2' ou '4'")

    # Boxplots avec disposition choisie
    for i in range(0, len(variables), ncols * nrows):
        subset = variables[i:i + ncols * nrows]

        fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
        axes = np.array(axes).reshape(-1)

        for ax, var in zip(axes, subset):
            ax.boxplot(df[var].dropna(), vert=True)
            ax.set_title(f"{var}", fontsize=10)
            ax.set_ylabel(var)
            ax.grid(axis="y", linestyle="--", alpha=0.6)

        # Supprimer les axes vides
        for ax in axes[len(subset):]:
            ax.axis("off")

        plt.tight_layout()
        plt.show()


def world_map(dataframe,y_col,country_code_col="Pays_code_iso3",country_name_col="LOCATION",data_name=None,width=900,height=500):
    """
    Creates a static world map showing the distribution of a specific column across countries.

    Parameters:
    - dataframe (DataFrame): Input dataframe
    - y_col (str): Column to visualize
    - country_code_col (str): ISO3 country code column
    - country_name_col (str): Country name column
    - data_name (str): Title label (optional)
    - width (int): Figure width
    - height (int): Figure height
    """

    min_value = dataframe[y_col].min()
    max_value = dataframe[y_col].max()

    fig = px.choropleth(
        dataframe,
        locations=country_code_col,
        color=y_col,
        hover_name=country_name_col,
        color_continuous_scale="turbo",
        projection="natural earth",
        range_color=(min_value, max_value)
    )

    fig.update_layout(
        title_text=data_name if data_name else y_col,
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="white",
        ),
        width=width,
        height=height
    )

    fig.update_coloraxes(colorbar_title_text="")

    fig.show()