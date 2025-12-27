import pandas as pd
from PIB_hab import get_gdp_per_capita_wide

def merge():

# Chargement des trois fichiers
df_gpw = pd.read_csv('Données_OMS/WHO_SDG_GPW_standardisé_avec_code_pays_complet.csv')
df_sdg3 = pd.read_csv('Données_OMS/WHO_SDG3_standardisé_avec_code_pays_complet.csv')
df_PIB = get_gdp_per_capita_wide()
df_ihme = pd.read_csv('Données_IHME/IHME_Mental_Health_WIDE.csv')
df_ihme = df_ihme[['Eating_disorders', 'Mental_disorders']]

# MERGE GPW + SDG3

keys_oms = ['LOCATION','Pays_code_iso3']

missing_keys = [k for k in keys_oms if k not in df_gpw.columns or k not in df_sdg3.columns]
if missing_keys:
    print(f"Colonnes clés absentes : {missing_keys}")
else:
    df_fusion_oms = pd.merge(
        df_gpw,
        df_sdg3,
        on=keys_oms,
        how='inner'
    )

# MERGE avec IHME

key = 'LOCATION'

df_fusion_health = pd.merge(
        df_fusion_oms,
        df_ihme,
        on=key,
        how='inner'
    )

# MERGE avec le PIB

key_pib_left = 'Pays_code_iso3'
key_pib_right = 'Country Code'

df_final = pd.merge(
    df_fusion_oms,
    df_PIB,        
    left_on=key_pib_left,
    right_on=key_pib_right,
    how='inner')

# Sauvegarde finale
df_final.to_csv('Table_fusion.csv', index=False)