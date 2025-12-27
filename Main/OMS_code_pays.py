import requests
import pandas as pd
import pycountry

BASE_URL = "https://xmart-api-public.who.int/DEX_CMS/"

def get_headers(grp, loc_type="COUNTRY", version="2025"):
    url = (f"{BASE_URL}WHSA_HEADER?"
           f"$filter=14 eq 14 and IND_GRP_CODE eq '{grp}' and LOCATION_TYPE_CODE eq '{loc_type}' and VERSION_CODE eq '{version}'"
           f"&$orderby=SORT asc")
    resp = requests.get(url)
    resp.raise_for_status()
    return pd.DataFrame(resp.json()["value"])

def get_facts(grp, loc_type="COUNTRY", version="2025"):
    url = (f"{BASE_URL}WHSA_FACT_DISPLAY?"
           f"$filter=14 eq 14 and IND_GRP_CODE eq '{grp}' and LOCATION_TYPE_CODE eq '{loc_type}' and VERSION_CODE eq '{version}'"
           f"&$orderby=LOCATION_SORT asc")
    resp = requests.get(url)
    resp.raise_for_status()
    return pd.DataFrame(resp.json()["value"])

def build_wide_table(headers_df, facts_df):
    wide_records = {}
    for _, fact in facts_df.iterrows():
        loc = fact["LOCATION_CODE"]
        if loc not in wide_records:
            wide_records[loc] = {"LOCATION": fact["LOCATION"]}
        dim_label = fact["FACT_IND"]
        if fact.get("DIM_MEMBER_1"):
            dim_label += f"_{fact['DIM_MEMBER_1']}"
        wide_records[loc][dim_label] = fact["VALUE_STRING"]
    return pd.DataFrame.from_records(list(wide_records.values()))

def get_iso3(country_name):
    """Convertit le nom du pays en code ISO-3"""
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_3
    except LookupError:
        return None

def get_data_health_with_iso():
    """
    Récupère les données OMS SDG3 et SDG_GPW et ajoute la colonne Pays_code_iso3
    """
    # SDG3
    headers_sdg3 = get_headers("SDG3")
    facts_sdg3 = get_facts("SDG3")
    df_sdg3 = build_wide_table(headers_sdg3, facts_sdg3)
    df_sdg3["Pays_code_iso3"] = df_sdg3["LOCATION"].apply(get_iso3)
    cols = df_sdg3.columns.tolist()
    cols.insert(1, cols.pop(cols.index("Pays_code_iso3")))
    df_sdg3 = df_sdg3[cols]

    # SDG_GPW
    headers_sdg_gpw = get_headers("SDG_GPW")
    facts_sdg_gpw = get_facts("SDG_GPW")
    df_sdg_gpw = build_wide_table(headers_sdg_gpw, facts_sdg_gpw)
    df_sdg_gpw["Pays_code_iso3"] = df_sdg_gpw["LOCATION"].apply(get_iso3)
    cols = df_sdg_gpw.columns.tolist()
    cols.insert(1, cols.pop(cols.index("Pays_code_iso3")))
    df_sdg_gpw = df_sdg_gpw[cols]
    df_sdg_gpw = df_sdg_gpw[['LOCATION','Pays_code_iso3','NUTOVERWEIGHTPREV','GHED_GGHE_DGGE_SHA2011','NUTSTUNTINGPREV']]

    return {"SDG3": df_sdg3, "SDG_GPW": df_sdg_gpw}

# Exécution

if __name__ == "__main__":
    dfs = get_data_health_with_iso()

    df_sdg3 = dfs["SDG3"]
    df_sdg_gpw = dfs["SDG_GPW"]
    df_sdg3.to_csv("/home/onyxia/python-DATA/Données_OMS/WHO_SDG3_standardisé_avec_code_pays.csv", index = False)
    df_sdg_gpw.to_csv("/home/onyxia/python-DATA/Données_OMS/WHO_SDG_GPW_standardisé_avec_code_pays.csv", index = False)