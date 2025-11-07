import requests
import pandas as pd

BASE_URL = "https://xmart-api-public.who.int/DEX_CMS/"

def get_headers(grp="SDG3", loc_type="COUNTRY", version="2025"):
    url = (f"{BASE_URL}WHSA_HEADER?"
           f"$filter=14 eq 14 and IND_GRP_CODE eq '{grp}' and LOCATION_TYPE_CODE eq '{loc_type}' and VERSION_CODE eq '{version}'"
           f"&$orderby=SORT asc")
    resp = requests.get(url)
    resp.raise_for_status()
    return pd.DataFrame(resp.json()["value"])

def get_facts(grp="SDG3", loc_type="COUNTRY", version="2025"):
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
    headers_df = get_headers()
    facts_df = get_facts()
    table_df = build_wide_table(headers_df, facts_df)
    print(table_df.head())

    # Sauvegarder
    table_df.to_csv("WHO_SDG3_COUNTRY_2025.csv", index=False)
