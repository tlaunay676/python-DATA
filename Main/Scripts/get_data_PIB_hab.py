import requests
import pandas as pd

def check_api_availability(indicator="NY.GDP.PCAP.CD"):
    """
    Vérifie la disponibilité de l'API de la Banque mondiale pour un indicateur donné.

    Paramètres
    ----------
    indicator : str, optional
        Code de l'indicateur de la Banque mondiale (par défaut "NY.GDP.PCAP.CD" pour le PIB par habitant).

    Sortie
    ------
    bool
        True si l'API est disponible, False sinon.
    """

    # Construction de l'URL pour accéder à l'indicateur
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
    
    try:
        # Envoi d'une requête GET avec timeout de 60 secondes
        r = requests.get(url, timeout=60)
        # Vérification du statut HTTP
        r.raise_for_status()
        return True
    except requests.exceptions.RequestException as api_exception:
        # Gestion des exceptions en cas d'indisponibilité de l'API
        print("L'API n'est pas disponible, la sauvegarde locale a été utilisée")
        return False


def get_gdp_per_capita_wide(start_year=2015, end_year=2024, indicator="NY.GDP.PCAP.CD"):
    """
    Récupère le PIB par habitant depuis la Banque mondiale et retourne un DataFrame au format large.

    Paramètres
    ----------
    start_year : int, optional
        Année de début de la période (par défaut 2015).
    end_year : int, optional
        Année de fin de la période (par défaut 2024).
    indicator : str, optional
        Code de l'indicateur de la Banque mondiale (par défaut "NY.GDP.PCAP.CD").

    Sortie
    ------
    pandas.DataFrame
        DataFrame au format large : Country Name | Country Code | 2015 | ... | 2024
    """

    # Construction de l'URL et des paramètres pour la requête API
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
    params = {
        "format": "json",
        "per_page": 20000,
        "date": f"{start_year}:{end_year}"
    }

    # Requête GET vers l'API
    r = requests.get(url, params=params)
    r.raise_for_status()  # Vérifie que la requête a réussi

    # Conversion de la réponse JSON en DataFrame
    data = r.json()[1]
    df = pd.DataFrame(data)

    # Extraction du nom des pays depuis le dictionnaire renvoyé
    df["Country Name"] = df["country"].apply(
        lambda x: x["value"] if isinstance(x, dict) else None
    )

    # Sélection des colonnes pertinentes
    df = df[["Country Name", "countryiso3code", "date", "value"]]
    df.columns = ["Country Name", "Country Code", "Year", "GDP_per_capita"]

    # Transformation du format long (Year, Value) en format large (colonnes années)
    df_wide = (
        df.pivot(
            index=["Country Name", "Country Code"],
            columns="Year",
            values="GDP_per_capita"
        )
        .reset_index()
    )

    # Tri des colonnes années par ordre croissant
    year_cols = sorted(
        [c for c in df_wide.columns if c.isdigit()],
        key=int
    )
    df_wide = df_wide[["Country Name", "Country Code"] + year_cols]

    # Supprime le nom de la hiérarchie des colonnes
    df_wide.columns.name = None

    return df_wide


def get_gdp_per_capita(start_year=2015, end_year=2024, indicator="NY.GDP.PCAP.CD"):
    """
    Récupère le PIB par habitant depuis la Banque mondiale et retourne un DataFrame au format long.

    Paramètres
    ----------
    start_year : int, optional
        Année de début de la période (par défaut 2015).
    end_year : int, optional
        Année de fin de la période (par défaut 2024).
    indicator : str, optional
        Code de l'indicateur de la Banque mondiale (par défaut "NY.GDP.PCAP.CD").

    Sortie
    ------
    pandas.DataFrame
        DataFrame au format long : Country Name | Country Code | Year | GDP_per_capita
    """

    # Construction de l'URL et des paramètres pour la requête API
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
    params = {
        "format": "json",
        "per_page": 20000,
        "date": f"{start_year}:{end_year}"
    }

    # Requête GET vers l'API
    r = requests.get(url, params=params)
    r.raise_for_status()

    # Conversion de la réponse JSON en DataFrame
    data = r.json()[1]
    df = pd.DataFrame(data)

    # Extraction du nom des pays depuis le dictionnaire renvoyé
    df["Country Name"] = df["country"].apply(
        lambda x: x["value"] if isinstance(x, dict) else None
    )

    # Sélection des colonnes pertinentes et renommage
    df = df[["Country Name", "countryiso3code", "date", "value"]]
    df.columns = ["Country Name", "Country Code", "Year", "GDP_per_capita"]

    return df
