import requests
import pandas as pd

def fetch_worldbank_indicator(indicator_code, start_year=None, end_year=None, format="json"):
    """
    Récupère les données d'un indicateur de la Banque mondiale pour tous les pays.
    
    indicator_code: code de l'indicateur (ex. "NY.GDP.PCAP.CD")
    start_year, end_year: plage de dates souhaitée (optionnel)
    """
    base_url = "https://api.worldbank.org/v2/country/all/indicator/"
    params = {
        "format": format,
        "per_page": 20000  # suffisamment grand pour obtenir tous les pays / années
    }
    
    if start_year:
        params["date"] = f"{start_year}:{end_year or ''}"

    url = f"{base_url}{indicator_code}"
    response = requests.get(url, params=params)
    response.raise_for_status()

    # la réponse JSON vient en deux parties : 
    # - index 0 : métadonnées,
    # - index 1 : données
    data = response.json()
    if len(data) < 2:
        raise ValueError("Pas de données retournées par l'API.")
    
    return pd.DataFrame(data[1])

# Exemple : récupérer le PIB par habitant (NY.GDP.PCAP.CD)
df_gdp_per_capita = fetch_worldbank_indicator("NY.GDP.PCAP.CD", start_year=2015, end_year=2024)

# Nettoyage / sélection de colonnes utiles
df_gdp_per_capita = df_gdp_per_capita[[
    "countryiso3code", "country", "date", "value"
]].rename(columns={
    "countryiso3code": "ISO3",
    "country": "Country",
    "date": "Year",
    "value": "GDP_per_capita_USD"
})

# Affichage propre
print(df_gdp_per_capita.head())
