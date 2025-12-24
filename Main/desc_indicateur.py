def desc_missing_pib(df, var, country_col):
    """
    Description textuelle d'un DataFrame et des valeurs manquantes
    """

    # Infos générales
    n_countries = df[country_col].nunique()

    # Missing values
    n_missing = df[var].isna().sum()
    pct_missing = (n_missing / n_countries) * 100

    # Affichage formaté
    print(f"The dataframe includes {n_countries} countries and {n_missing} missing values.\n"
          f"The percentage of missing values for the GDP per capita of {var} in the dataset is {pct_missing:.2f}%.")

def desc_missing_health(df, var, country_col):
    """
    Description textuelle d'un DataFrame et des valeurs manquantes
    """

    # Infos générales
    n_countries = df[country_col].nunique()

    # Missing values
    n_missing = df[var].isna().sum()
    pct_missing = (n_missing / n_countries) * 100

    # Affichage formaté
    print(f"The dataframe includes {n_countries} countries and {n_missing} missing values.\n"
          f"The percentage of missing values for {var} in the dataset is {pct_missing:.2f}%.")