import requests
import pandas as pd

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
    """
    Reconstruit le tableau complet en suivant la construction du code source.
    """
    wide_records = {}

    for _, fact in facts_df.iterrows():
        loc = fact["LOCATION_CODE"]
        if loc not in wide_records:
            wide_records[loc] = {"LOCATION": fact["LOCATION"]}

        # Générer le nom de colonne comme dans le JS
        dim_label = fact["FACT_IND"]
        if fact.get("DIM_MEMBER_1"):
            dim_label += f"_{fact['DIM_MEMBER_1']}"
        
        wide_records[loc][dim_label] = fact["VALUE_STRING"]
        wide_records[loc][f"{dim_label}-footnote"] = fact.get("FACT_FOOTNOTE", "")
        wide_records[loc][f"{dim_label}-footnote-short"] = fact.get("FACT_FOOTNOTE_SHORT", fact.get("FACT_FOOTNOTE", ""))

    wide_df = pd.DataFrame.from_records(list(wide_records.values()))
    return wide_df

if __name__ == "__main__":

    headers_df_sdg3 = get_headers("SDG3")
    facts_df_sdg3 = get_facts("SDG3")
    table_df_sdg3 = build_wide_table(headers_df_sdg3, facts_df_sdg3)

    # Sauvegarder
    table_df_sdg3.to_csv(f"WHO_SDG3_COUNTRY_2025.csv", index=False)

    headers_df_sdg_gpw = get_headers("SDG_GPW")
    facts_df_sdg_gpw = get_facts("SDG_GPW")
    table_df_sdg_gpw = build_wide_table(headers_df_sdg_gpw, facts_df_sdg_gpw)
    table_df_sdg_gpw_select = table_df_sdg_gpw[['LOCATION', 'NUTOVERWEIGHTPREV', 'GHED_GGHE_DGGE_SHA2011', 'NUTRITION_ANAEMIA_REPRODUCTIVEAGE_PREV', 'SDGPM25', 'SDGODAWS', 'WSH_WATER_SAFELY_MANAGED', 'PHE_HHAIR_PROP_POP_CLEAN_FUELS', 'SDGIPV12M', 'VIOLENCE_HOMICIDERATE', 'NUTRITION_WH_2', 'NUTSTUNTINGPREV', 'WSH_HYGIENE_BASIC', 'SDGIPVLT', 'WSH_DOMESTIC_WASTE_SAFELY_TREATED', 'WSH_SANITATION_SAFELY_MANAGED']]
    # Sauvegarder
    table_df_sdg_gpw_select.to_csv(f"WHO_SDG_GPW_SELECT_COUNTRY_2025.csv", index=False)



    
