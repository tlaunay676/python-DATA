import plotly.express as px

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