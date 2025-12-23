import pandas as pd
import pycountry

# Charger le fichier CSV
df = pd.read_csv("/home/onyxia/python-DATA-1/Données_OMS/WHO_SDG_GPW_standardisé.csv")
df1 = pd.read_csv("/home/onyxia/python-DATA-1/Données_OMS/WHO_SDG3_standardisé.csv")

# Fonction pour convertir le nom du pays en code ISO-3
def get_iso3(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_3
    except LookupError:
        return None  # ou "UNK" si tu préfères

# Ajouter la nouvelle colonne
df["Pays_code_iso3"] = df["LOCATION"].apply(get_iso3)
cols = df.columns.tolist()
cols.insert(1, cols.pop(cols.index("Pays_code_iso3")))
df = df[cols]
df1["Pays_code_iso3"] = df["LOCATION"].apply(get_iso3)
cols = df1.columns.tolist()
cols.insert(1, cols.pop(cols.index("Pays_code_iso3")))
df1 = df1[cols]

# Sauvegarder le nouveau fichier
df.to_csv("/home/onyxia/python-DATA-1/Données_OMS/WHO_SDG_GPW_standardisé_avec_code_pays.csv", index=False)
df1.to_csv("/home/onyxia/python-DATA-1/Données_OMS/WHO_SDG3_standardisé_avec_code_pays.csv", index=False)