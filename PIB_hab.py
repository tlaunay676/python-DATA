import requests
import pandas as pd

def get_gdp_per_capita(start_year=2015, end_year=2024, indicator="NY.GDP.PCAP.CD"):
    """
    Récupère le PIB par habitant (Banque mondiale)
    et retourne un DataFrame au format :
    Country Name | Country Code | 2015 | ... | 2024
    """

    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
    params = {
        "format": "json",
        "per_page": 20000,
        "date": f"{start_year}:{end_year}"
    }

    r = requests.get(url, params=params)
    r.raise_for_status()

    data = r.json()[1]
    df = pd.DataFrame(data)

    df["Country Name"] = df["country"].apply(
        lambda x: x["value"] if isinstance(x, dict) else None
    )

    df = df[["Country Name", "countryiso3code", "date", "value"]]
    df.columns = ["Country Name", "Country Code", "Year", "GDP_per_capita"]

    # Pivot années → colonnes
    df_wide = (
        df.pivot(
            index=["Country Name", "Country Code"],
            columns="Year",
            values="GDP_per_capita"
        )
        .reset_index()
    )

    # Trier les colonnes années
    year_cols = sorted(
        [c for c in df_wide.columns if c.isdigit()],
        key=int
    )

    df_wide = df_wide[["Country Name", "Country Code"] + year_cols]

    df_wide.columns.name = None

    return df_wide
