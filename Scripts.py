import requests
import pandas as pd


# Données OMS

# L'API utilisée correspond à une interface "REST" renvoyant du JSON.
# Comme dans le cours, on va envoyer une requête HTTP GET et convertir la réponse en DataFrame.
BASE_URL = "https://xmart-api-public.who.int/DEX_CMS/"

def get_headers(grp, loc_type="COUNTRY", version="2025"):
    """
    Récupère la table des 'headers' pour un groupe d'indicateurs (SDG3, SDG_GPW, etc.).
    --> Correspond au chapitre du cours : 'Interroger une API REST' avec requests.get.
    """

    # Construction dynamique de l'URL, comme montré dans le cours (paramètres + filtrage).
    url = (f"{BASE_URL}WHSA_HEADER?"
           f"$filter=14 eq 14 and IND_GRP_CODE eq '{grp}' and LOCATION_TYPE_CODE eq '{loc_type}' and VERSION_CODE eq '{version}'"
           f"&$orderby=SORT asc")

    # Envoi de la requête HTTP GET (exactement comme requests.get() dans le TP)
    resp = requests.get(url)

    # raise_for_status : méthode vue dans le cours pour détecter les erreurs HTTP
    resp.raise_for_status()

    # Conversion du JSON en DataFrame (cours : "json() --> dict --> pandas.DataFrame")
    return pd.DataFrame(resp.json()["value"])


def get_facts(grp, loc_type="COUNTRY", version="2025"):
    """
    Récupère la table des valeurs ('facts').
    Très similaire à get_headers --> structure répétée, comme recommandé dans le cours.
    """

    url = (f"{BASE_URL}WHSA_FACT_DISPLAY?"
           f"$filter=14 eq 14 and IND_GRP_CODE eq '{grp}' and LOCATION_TYPE_CODE eq '{loc_type}' and VERSION_CODE eq '{version}'"
           f"&$orderby=LOCATION_SORT asc")

    resp = requests.get(url)
    resp.raise_for_status()

    return pd.DataFrame(resp.json()["value"])


def build_wide_table(headers_df, facts_df):
    """
    Reconstruit le tableau 'pivoté' utilisé par l'interface WHO.
    Cette étape correspond dans le cours à :
    - la transformation des données
    - la restructuration à partir d'un format 'long' vers un format 'wide'

    Le cours recommande l’usage des dictionnaires avant conversion en DataFrame,
    ce que cette fonction fait aussi.
    """

    wide_records = {}

    # Parcours ligne par ligne des 'facts', comme dans les exemples du cours
    for _, fact in facts_df.iterrows():
        loc = fact["LOCATION_CODE"]

        # Création d'une entrée pour chaque pays si elle n'existe pas encore
        if loc not in wide_records:
            wide_records[loc] = {"LOCATION": fact["LOCATION"]}

        # Nom de colonne : reproduit fidèlement la logique JavaScript de l'API OMS
        dim_label = fact["FACT_IND"]

        # Ajout conditionnel d'une dimension secondaire (cours : nettoyage / enrichissement)
        if fact.get("DIM_MEMBER_1"):
            dim_label += f"_{fact['DIM_MEMBER_1']}"

        # Enregistrement de la valeur principale
        wide_records[loc][dim_label] = fact["VALUE_STRING"]

    # Comme dans le cours : dict --> DataFrame
    wide_df = pd.DataFrame.from_records(list(wide_records.values()))
    return wide_df

def get_data_health():
    """
    Récupère et construit les DataFrames OMS pour SDG3 et SDG_GPW.
    Renvoie un dictionnaire avec les DataFrames pour pouvoir les utiliser ailleurs.
    """

    # 1. Groupe SDG3
    headers_df_sdg3 = get_headers("SDG3")
    facts_df_sdg3 = get_facts("SDG3")
    table_df_sdg3 = build_wide_table(headers_df_sdg3, facts_df_sdg3)

    # 2. Groupe SDG_GPW
    headers_df_sdg_gpw = get_headers("SDG_GPW")
    facts_df_sdg_gpw = get_facts("SDG_GPW")
    table_df_sdg_gpw = build_wide_table(headers_df_sdg_gpw, facts_df_sdg_gpw)

    # Retourne les DataFrames dans un dictionnaire
    return table_df_sdg_gpw