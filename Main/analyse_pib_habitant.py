import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans

def plot_missing_gdp(data, col = "GDP_per_capita"):
    """
    Plots the yearly and cumulative missing values for a specific column.
    Parameters:
    - data (DataFrame): The input dataframe containing the data.
    - col (str): The column for which missing values are plotted.
    """
    missing_values_per_year = data.groupby('Year')[col].apply(lambda x: x.isnull().sum())
    missing_values_per_year_percentage = (missing_values_per_year/data.shape[0])*100*10 # Because hear we use the long table so shape[0] give us the number of country x the number of years (=10)
    fig, ax1 = plt.subplots(figsize=(12, 6))
    bars = ax1.bar(missing_values_per_year.index, missing_values_per_year.values, color='skyblue', label='Yearly Missing Values')
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of Missing Values per Year', color='skyblue')
    ax1.set_title('Yearly Missing in GDP')
    ax1.set_xticks(missing_values_per_year.index)
    ax1.set_xticklabels(missing_values_per_year.index, rotation=90)
    ax2 = ax1.twinx()
    ax2.plot(missing_values_per_year_percentage.index, missing_values_per_year_percentage.values, color='orange', marker='o', label='Missing Values (%)')
    ax2.set_ylabel('Missing Values since 2015 in %', color='orange')
    plt.show()


def world_map_gdp(dataframe, y_col = 'GDP_per_capita', data_name = 'PIB par habitant', width=900, height=500):
    """
    Creates an animated world map showing the distribution of a specific data column across countries and years.
    Parameters:
    - dataframe (DataFrame): The input dataframe containing country-level data.
    - y_col (str): The column to be visualized on the map
    - data_name (str): A label for the data being visualized
    - width (int): The width of the map figure.
    - height (int): The height of the map figure.
    Notes:
    - Assumes the dataframe has columns 'Country Code', 'Year', and the specified y_col.
    """
    min_value = dataframe[y_col].min()
    max_value = 125000 # We don't take the max because he is too high and not visible on the map
    # Création d'une carte du monde avec Plotly
    fig = px.choropleth(dataframe, 
                        locations='Country Code',
                        color=y_col,
                        hover_name='Country Code',
                        color_continuous_scale="turbo",
                        projection='natural earth',
                        animation_frame='Year',
                        range_color=(min_value, max_value))
    fig.update_coloraxes(colorbar_title_text='')
    # Mise en page des sous-plots pour les barres d'histogramme
    fig.update_layout(
        xaxis2=dict(domain=[0, 0.45], anchor='y2'),
        xaxis3=dict(domain=[0.55, 1], anchor='y3'),
        yaxis2=dict(domain=[0, 1], anchor='x2'),
        yaxis3=dict(domain=[0, 1], anchor='x3'),
        title_text= f'{data_name} par pays, 2015-2024',
    )
    # Ajout d'un slider pour choisir l'année
    slider = go.layout.Slider(
        currentvalue=dict(prefix="Année: "),
        font=dict(size=16),
        len=0.9,
        pad=dict(t=50, b=10),
        steps=[
            {"args": [f"slider{i}.value", {"duration": 400, "frame": {"duration": 400, "redraw": True}, "mode": "immediate"}],
             "label": str(i),
             "method": "animate",
            } for i in range(2015, 2024)
        ],
    )
    fig.update_layout(
    sliders=[
        {
            "steps": [
                {"args": [[f"{year}"], {"frame": {"duration": 500, "redraw": True}, "mode": "immediate", "transition": {"duration": 500}}], "label": f"{year}", "method": "animate"} 
                for year in sorted(dataframe['Year'].unique())
            ],
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "transition": {"duration": 300, "easing": "cubic-in-out"},
        }
    ],
    updatemenus=[{"type": "buttons", "showactive": False, "buttons": [{"label": "Play", "method": "animate", "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True, "transition": {"duration": 300, "easing": "quadratic-in-out"}}]}]},
                 {"type": "buttons", "showactive": False, "buttons": [{"label": "Quick", "method": "animate", "args": [None, {"frame": {"duration": 0, "redraw": True}, "transition": {"duration": 0}}]}]}]
)
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