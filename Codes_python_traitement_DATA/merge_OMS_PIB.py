import pandas as pd

# Chargement des trois fichiers
df_gpw = pd.read_csv('/home/onyxia/python-DATA/Données_OMS/WHO_SDG_GPW_standardisé_avec_code_pays_complet.csv')
df_sdg3 = pd.read_csv('/home/onyxia/python-DATA/Données_OMS/WHO_SDG3_standardisé_avec_code_pays_complet.csv')
df_PIB = pd.read_csv('/home/onyxia/python-DATA/Données_PIB/Données_PIB_habitant_2015_2024.csv')

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
        how='outer',
        suffixes=('_gpw', '_sdg3')
    )

# MERGE avec le PIB

key_pib_left = 'Pays_code_iso3'
key_pib_right = 'Country Code'

df_final = pd.merge(
    df_fusion_oms,
    df_PIB,        
    left_on=key_pib_left,
    right_on=key_pib_right,
    how='inner',
    suffixes=('', '_pib'))

print(f'Shape finale: {df_final.shape}')

# Sauvegarde finale
df_final.to_csv('/home/onyxia/python-DATA-1/Table_fusion_OMS_PIB.csv', index=False)