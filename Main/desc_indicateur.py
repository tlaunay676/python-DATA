def desc_missing(df, var, country_col):
    """
    Description textuelle d'un DataFrame et des valeurs manquantes
    """

    # Infos générales
    n_countries = df[country_col].nunique()

    # Missing values
    n_missing = df[var].isna().sum()
    n_obs = n_countries - n_missing
    pct_missing = (n_missing / n_countries) * 100

    # Affichage formaté
    print(f"The dataframe includes {n_countries} countries.\n"
          f"There are {n_obs} observations and {n_missing} missing values.\n"
          f"The percentage of missing values for {var} in the dataset is {pct_missing:.2f}%.")
