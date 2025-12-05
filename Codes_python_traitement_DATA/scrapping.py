import requests
import pandas as pd

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

        # Enregistrement des notes de bas de page (métadonnées)
        wide_records[loc][f"{dim_label}-footnote"] = fact.get("FACT_FOOTNOTE", "")
        wide_records[loc][f"{dim_label}-footnote-short"] = fact.get(
            "FACT_FOOTNOTE_SHORT", fact.get("FACT_FOOTNOTE", "")
        )

    # Comme dans le cours : dict --> DataFrame
    wide_df = pd.DataFrame.from_records(list(wide_records.values()))
    return wide_df



# ---------------------------------------------------------
# PARTIE PRINCIPALE : correspond à la section du cours
# « Structurer son scraping dans un main ».
# ---------------------------------------------------------

if __name__ == "__main__":

    # 1. Scraping du groupe SDG3 (OMS Objectifs de développement durable)
    headers_df_sdg3 = get_headers("SDG3")
    facts_df_sdg3 = get_facts("SDG3")

    # Transformation en tableau large
    table_df_sdg3 = build_wide_table(headers_df_sdg3, facts_df_sdg3)

    # Sélection des colonnes (comme dans la section du cours sur le filtrage pandas)
    table_df_sdg3_select = table_df_sdg3[
        ['LOCATION', 'HWF_0010', 'HWF_0006', 'HWF_0001', 'MDG_0000000003_15_19',
         'SDGSUICIDE', 'FINPROTECTION_CATA_TOT_10_POP', 'FINPROTECTION_CATA_TOT_25_POP',
         'MDG_0000000003_10_14', 'SDGFPALL', 'SDGHEPHBSAGPRV', 'SDGPOISON',
         'WHOSIS_000002_BTSX', 'WHOSIS_000002_FMLE', 'WHOSIS_000002_MLE', 'HWF_0014',
         'M_Est_tob_curr_std', 'MDG_0000000025', 'WHS4_100', 'MDG_0000000020',
         'SDGWSHBOD', 'SDGHIV', 'MALARIA_EST_INCIDENCE', 'NCDMORT3070',
         'SA_0000001688', 'MDG_0000000007', 'MCV2', 'SDGAIRBODA', 'WHOSIS_000003',
         'UHC_INDEX_REPORTED', 'SDGIHR2021', 'PCV3', 'MDG_0000000026', 'RS_198',
         'SDGNTDTREATMENT', 'WHOSIS_000001_BTSX', 'WHOSIS_000001_FMLE',
         'WHOSIS_000001_MLE', 'SDGODA01', 'SDGHPVRECEIVED',
         'SUD_TREATMENTSERVICES_COVERAGE_ALCOHOL', 'AMR_INFECT_MRSA',
         'AMR_INFECT_ECOLI', 'SUD_TREATMENTSERVICES_COVERAGE_DRUGS',
         'SDGHEALTHFACILITIESESSENTIALMEDS']
    ]

    # Export CSV (cours : "écrire un fichier après scraping")
    table_df_sdg3_select.to_csv("/home/onyxia/python-DATA-1/Données_OMS/WHO_SDG3_SELECT_COUNTRY_2025.csv", index=False)



    # 2. Scraping du groupe SDG_GPW (global programme of work)
    headers_df_sdg_gpw = get_headers("SDG_GPW")
    facts_df_sdg_gpw = get_facts("SDG_GPW")

    table_df_sdg_gpw = build_wide_table(headers_df_sdg_gpw, facts_df_sdg_gpw)

    table_df_sdg_gpw_select = table_df_sdg_gpw[
        ['LOCATION', 'NUTOVERWEIGHTPREV', 'GHED_GGHE_DGGE_SHA2011',
         'NUTRITION_ANAEMIA_REPRODUCTIVEAGE_PREV', 'SDGPM25', 'SDGODAWS',
         'WSH_WATER_SAFELY_MANAGED', 'PHE_HHAIR_PROP_POP_CLEAN_FUELS',
         'SDGIPV12M', 'VIOLENCE_HOMICIDERATE', 'NUTRITION_WH_2',
         'NUTSTUNTINGPREV', 'WSH_HYGIENE_BASIC', 'SDGIPVLT',
         'WSH_DOMESTIC_WASTE_SAFELY_TREATED', 'WSH_SANITATION_SAFELY_MANAGED']
    ]

    # Export CSV
    table_df_sdg_gpw_select.to_csv("WHO_SDG_GPW_SE/home/onyxia/python-DATA-1/Données_OMS/WHO_SDG_GPW_SELECT_COUNTRY_2025.csv", index=False)
