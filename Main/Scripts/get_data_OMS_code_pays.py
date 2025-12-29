import requests
import pandas as pd
import pycountry

# URL de base pour accéder aux API publiques de l'OMS
BASE_URL = "https://xmart-api-public.who.int/DEX_CMS/"

def get_headers(grp, loc_type="COUNTRY", version="2025"):
    """
    Récupère les en-têtes (headers) pour un groupe d'indicateurs spécifique.

    Paramètres
    ----------
    grp : str
        Code du groupe d'indicateurs (ex. "SDG3" ou "SDG_GPW").
    loc_type : str, optional
        Type de localisation, par défaut "COUNTRY".
    version : str, optional
        Version des données, par défaut "2025".

    Sortie
    ------
    pandas.DataFrame
        DataFrame contenant les informations des headers pour le groupe spécifié.
    """

    # Construction de l'URL avec filtres pour le groupe, le type de localisation et la version
    url = (f"{BASE_URL}WHSA_HEADER?"
           f"$filter=14 eq 14 and IND_GRP_CODE eq '{grp}' and LOCATION_TYPE_CODE eq '{loc_type}' and VERSION_CODE eq '{version}'"
           f"&$orderby=SORT asc")

    # Requête GET vers l'API
    resp = requests.get(url)
    # Vérification du succès de la requête
    resp.raise_for_status()
    # Conversion du résultat JSON en DataFrame pandas
    return pd.DataFrame(resp.json()["value"])


def get_facts(grp, loc_type="COUNTRY", version="2025"):
    """
    Récupère les valeurs (facts) pour un groupe d'indicateurs spécifique.

    Paramètres
    ----------
    grp : str
        Code du groupe d'indicateurs (ex. "SDG3" ou "SDG_GPW").
    loc_type : str, optional
        Type de localisation, par défaut "COUNTRY".
    version : str, optional
        Version des données, par défaut "2025".

    Sortie
    ------
    pandas.DataFrame
        DataFrame contenant les valeurs des indicateurs pour le groupe spécifié.
    """

    # Construction de l'URL avec filtres
    url = (f"{BASE_URL}WHSA_FACT_DISPLAY?"
           f"$filter=14 eq 14 and IND_GRP_CODE eq '{grp}' and LOCATION_TYPE_CODE eq '{loc_type}' and VERSION_CODE eq '{version}'"
           f"&$orderby=LOCATION_SORT asc")

    # Requête GET vers l'API
    resp = requests.get(url)
    resp.raise_for_status()
    # Conversion du résultat JSON en DataFrame pandas
    return pd.DataFrame(resp.json()["value"])


def build_wide_table(headers_df, facts_df):
    """
    Transforme les données en format large (wide) à partir des facts.

    Paramètres
    ----------
    headers_df : pandas.DataFrame
        DataFrame contenant les informations des headers.
    facts_df : pandas.DataFrame
        DataFrame contenant les valeurs des indicateurs.

    Sortie
    ------
    pandas.DataFrame
        DataFrame en format large avec une ligne par pays et une colonne par indicateur.
    """

    # Dictionnaire pour stocker les lignes transformées
    wide_records = {}

    # Boucle sur chaque ligne
    for _, fact in facts_df.iterrows():
        loc = fact["LOCATION_CODE"]
        # Si le pays n'existe pas encore dans le dictionnaire, on l'ajoute
        if loc not in wide_records:
            wide_records[loc] = {"LOCATION": fact["LOCATION"]}

        # Création du nom de la colonne
        dim_label = fact["FACT_IND"]
        if fact.get("DIM_MEMBER_1"):
            dim_label += f"_{fact['DIM_MEMBER_1']}"

        # Ajout de la valeur correspondante à la colonne dans le dictionnaire
        wide_records[loc][dim_label] = fact["VALUE_STRING"]

    # Conversion du dictionnaire en DataFrame pandas
    return pd.DataFrame.from_records(list(wide_records.values()))


def get_iso3(country_name):
    """
    Convertit le nom d'un pays en code ISO-3.

    Paramètres
    ----------
    country_name : str
        Nom du pays.

    Sortie
    ------
    str ou None
        Code ISO-3 du pays si trouvé, sinon None.
    """

    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_3
    except LookupError:
        # Si le pays n'est pas trouvé, retourner None
        return None


def get_data_health_with_iso():
    """
    Récupère les données OMS pour SDG3 et SDG_GPW, et ajoute une colonne 'Pays_code_iso3'.

    Paramètres
    ----------
    Aucun

    Sortie
    ------
    dict
        Dictionnaire avec deux DataFrames : {"SDG3": df_sdg3, "SDG_GPW": df_sdg_gpw}.
        Chaque DataFrame contient les données des indicateurs par pays, avec une colonne Pays_code_iso3.
    """

    # SDG3
    headers_sdg3 = get_headers("SDG3")
    facts_sdg3 = get_facts("SDG3")
    df_sdg3 = build_wide_table(headers_sdg3, facts_sdg3)
    df_sdg3["Pays_code_iso3"] = df_sdg3["LOCATION"].apply(get_iso3)
    # Réorganisation des colonnes pour mettre Pays_code_iso3 en deuxième position
    cols = df_sdg3.columns.tolist()
    cols.insert(1, cols.pop(cols.index("Pays_code_iso3")))
    df_sdg3 = df_sdg3[cols]
    # Sélection des colonnes spécifiques à conserver
    df_sdg3 = df_sdg3[['LOCATION','Pays_code_iso3',"HWF_0001","SDGSUICIDE","WHOSIS_000001_BTSX","WHOSIS_000003","MDG_0000000026"]]

    # SDG_GPW
    headers_sdg_gpw = get_headers("SDG_GPW")
    facts_sdg_gpw = get_facts("SDG_GPW")
    df_sdg_gpw = build_wide_table(headers_sdg_gpw, facts_sdg_gpw)
    df_sdg_gpw["Pays_code_iso3"] = df_sdg_gpw["LOCATION"].apply(get_iso3)
    cols = df_sdg_gpw.columns.tolist()
    cols.insert(1, cols.pop(cols.index("Pays_code_iso3")))
    df_sdg_gpw = df_sdg_gpw[cols]
    df_sdg_gpw = df_sdg_gpw[['LOCATION','Pays_code_iso3','NUTOVERWEIGHTPREV','GHED_GGHE_DGGE_SHA2011','NUTSTUNTINGPREV']]

    # Retourne un dictionnaire avec les deux DataFrames
    return {"SDG3": df_sdg3, "SDG_GPW": df_sdg_gpw}