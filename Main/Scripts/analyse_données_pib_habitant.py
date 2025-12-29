import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans

def plot_missing_gdp(data, col="GDP_per_capita"):
    """
    Trace les valeurs manquantes annuelles du PIB par habitant

    Paramètres
    ----------
    data : pandas.DataFrame
        DataFrame contenant les données.
    col : str, optional
        Colonne pour laquelle les valeurs manquantes doivent être tracées (par défaut "GDP_per_capita").

    Sortie
    ------
    Affiche un graphique combinant histogramme annuel des valeurs manquantes et courbe des pourcentages des valeurs manquantes.
    """

    # Calcul du nombre de valeurs manquantes par année
    missing_values_per_year = data.groupby('Year')[col].apply(lambda x: x.isnull().sum())

    # Calcul du pourcentage des valeurs manquantes par an
    missing_values_per_year_percentage = (missing_values_per_year / data.shape[0]) * 100 * 10
    # Remarque : multiplication par 10 car le tableau long multiplie le nombre de pays par le nombre d'années (=10)

    # Création de la figure
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Création de l'histogramme des valeurs manquantes annuelles
    bars = ax1.bar(missing_values_per_year.index, missing_values_per_year.values, color='skyblue', label='Valeurs manquantes annuelles')
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center')  # Annotation au-dessus des barres

    ax1.set_xlabel('Année')
    ax1.set_ylabel('Nombre de valeurs manquantes par an', color='skyblue')
    ax1.set_title('Valeurs manquantes annuelles dans le PIB par habitant')
    ax1.set_xticks(missing_values_per_year.index)
    ax1.set_xticklabels(missing_values_per_year.index, rotation=90)

    # Création d'un second axe y pour afficher le pourcentage
    ax2 = ax1.twinx()
    ax2.plot(missing_values_per_year_percentage.index, missing_values_per_year_percentage.values,
            color='orange', marker='o', label='Pourcentage de valeurs manquantes')
    ax2.set_ylabel('Valeurs manquantes annuelles dans le PIB par habitant (%)', color='orange')

    plt.show()


def world_map_gdp(dataframe, y_col='GDP_per_capita', data_name='PIB par habitant', width=900, height=500):
    """
    Crée une carte du monde animée montrant la distribution du PIB par habitant par pays et par année.

    Paramètres
    ----------
    dataframe : pandas.DataFrame
        DataFrame contenant les données par pays et par année.
    y_col : str, optional
        Colonne à représenter sur la carte (par défaut 'GDP_per_capita').
    data_name : str, optional
        Nom des données pour le titre de la carte (par défaut 'PIB par habitant').
    width : int, optional
        Largeur de la figure (par défaut 900).
    height : int, optional
        Hauteur de la figure (par défaut 500).

    Sortie
    ------
    Affiche une carte animée par année du PIB par habitant.
    """

    # Détermination des valeurs min et max pour la palette de couleurs
    min_value = dataframe[y_col].min()
    max_value = 125000  # Max ponctuel pour éviter que les valeurs extrêmes écrasent la visualisation

    # Création de la carte
    fig = px.choropleth(
        dataframe, 
        locations='Country Code',  # Colonne contenant les codes pays ISO3
        color=y_col,
        hover_name='Country Code',
        color_continuous_scale="turbo",
        projection='natural earth',
        animation_frame='Year',  # Animation par année
        range_color=(min_value, max_value)  # Étendue des couleurs
    )

    # Retirer le titre de la colorbar
    fig.update_coloraxes(colorbar_title_text='')

    # Mise en page pour sous-plots (histogrammes, sliders)
    fig.update_layout(
        xaxis2=dict(domain=[0, 0.45], anchor='y2'),
        xaxis3=dict(domain=[0.55, 1], anchor='y3'),
        yaxis2=dict(domain=[0, 1], anchor='x2'),
        yaxis3=dict(domain=[0, 1], anchor='x3'),
        title_text=f'{data_name} par pays, 2015-2024',
    )

    # Configuration du slider pour choisir l'année
    fig.update_layout(sliders=[{"steps": [{"args": [[f"{year}"], {"frame": {"duration": 500, "redraw": True},"mode": "immediate","transition": {"duration": 500}}],
                                           "label": f"{year}",
                                           "method": "animate"} for year in sorted(dataframe['Year'].unique())],
                                "active": 0,
                                "yanchor": "top",
                                "xanchor": "left",
                                "transition": {"duration": 300, "easing": "cubic-in-out"},}],
                      updatemenus=[{"type": "buttons", "showactive": False, "buttons": [{"label": "Play", "method": "animate",
                                                                                        "args": [None, {"frame": {"duration": 500, "redraw": True}, 
                                                                                        "fromcurrent": True,
                                                                                        "transition": {"duration": 300, "easing": "quadratic-in-out"}}]}]},
                                   {"type": "buttons", "showactive": False, "buttons": [{"label": "Quick", "method": "animate",
                                                                                        "args": [None, {"frame": {"duration": 0, "redraw": True},
                                                                                        "transition": {"duration": 0}}]}]}])

    # Configuration de l'affichage géographique
    fig.update_layout(
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="white",
        ),
        width=width,
        height=height
    )

    fig.show()


def quantiles_gdp(data_frame, k=int, y_col='GDP_per_capita'):
    """
    Trace les quantiles de PIB par habitant par année.

    Paramètres
    ----------
    data_frame : pandas.DataFrame
        DataFrame contenant les colonnes 'Year' et y_col.
    k : int
        Nombre de quantiles à calculer.
    y_col : str, optional
        Colonne contenant le PIB par habitant (par défaut 'GDP_per_capita').

    Sortie
    ------
    None
        Affiche un graphique des moyennes de PIB par décile et par année, ainsi que la moyenne globale.
    """

    # Calcul des quantiles du PIB par habitant
    quantiles = pd.qcut(data_frame[y_col], q=k, labels=False)

    # Création d'un DataFrame pour le tracé avec Year, décile et PIB
    plot_data = pd.DataFrame({'Year': data_frame['Year'], 'quantile': quantiles, 'GDP_per_capita': data_frame[y_col]})

    # Calcul de la moyenne par année et par décile
    grouped_data = plot_data.groupby(['Year', 'quantile'])['GDP_per_capita'].mean().unstack()

    # Calcul de la moyenne globale par année
    overall_mean = plot_data.groupby('Year')['GDP_per_capita'].mean()

    # Création du graphique
    plt.figure(figsize=(11, 6))
    for quantile in range(k):
        plt.plot(grouped_data.index, grouped_data[quantile], label=f'Décile {quantile + 1}')
        plt.text(grouped_data.index[-1] + str(2), grouped_data[quantile].iloc[-1],
                 f'Q{quantile + 1} mean: {grouped_data[quantile].mean():.2f}',
                 va='center', ha='left', color=plt.gca().get_lines()[-1].get_color())

    # Tracé de la moyenne globale en ligne pointillée noire
    plt.plot(overall_mean.index, overall_mean, label='Moyenne globale', linestyle='--', color='black')
    plt.text(overall_mean.index[-1] + str(2), overall_mean.iloc[-1] + 13,
             f'Moyenne globale: {overall_mean.mean():.2f}',
             va='center', ha='left', color='black')

    plt.ylabel('PIB moyen par habitant')
    plt.title('PIB moyen par habitant par année')
    plt.show()

    # Suppression du DataFrame temporaire
    del plot_data
