import pandas as pd

# Charger les deux fichiers
df_gpw = pd.read_csv('Données_OMS/WHO_SDG_GPW_standardisé.csv')
df_sdg3 = pd.read_csv('Données_OMS/WHO_SDG3_standardisé.csv')

print('=== WHO_SDG_GPW_standardisé.csv ===')
print(f'Shape: {df_gpw.shape}')
print(f'Colonnes: {list(df_gpw.columns)}')
print()
print(df_gpw.head())
print()

print('=== WHO_SDG3_standardisé.csv ===')
print(f'Shape: {df_sdg3.shape}')
print(f'Colonnes: {list(df_sdg3.columns)}')
print()
print(df_sdg3.head())
print()

# Fusionner les deux tables côte à côte (par l'index)
df_fusionne = pd.concat([df_gpw, df_sdg3], axis=1)

print('=== Table fusionnée ===')
print(f'Shape: {df_fusionne.shape}')
print(f'Colonnes: {list(df_fusionne.columns)}')
print()
print(df_fusionne.head())

# Sauvegarder la table fusionnée
df_fusionne.to_csv('Données_OMS/WHO_SDG_GPW_SDG3_fusionne.csv', index=False)
print('\n✓ Table fusionnée sauvegardée dans: Données_OMS/WHO_SDG_GPW_SDG3_fusionne.csv')
