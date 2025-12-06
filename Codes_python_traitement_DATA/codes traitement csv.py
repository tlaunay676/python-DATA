import pandas as pd

# Fichier d'entrée
input_file = "/home/onyxia/python-DATA/Données_PIB/Données_PIB_habitant_an.csv"
input_file1 = "/home/onyxia/python-DATA/Données_taux_pauvreté/Données_taux_pauvreté_an.csv"


# Colonnes à conserver
colonnes = ["Country Name","Country Code","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024"]

# Lecture du CSV
df = pd.read_csv(input_file)
df1 = pd.read_csv(input_file1)

# Filtrage des colonnes
df_filtered = df[colonnes]
df_filtered1 = df1[colonnes]

# Sauvegarde dans un nouveau fichier CSV
df_filtered.to_csv("/home/onyxia/python-DATA/Données_PIB/Données_PIB_habitant_2015_2024.csv", index=False)
df_filtered1.to_csv("/home/onyxia/python-DATA/Données_taux_pauvreté/Données_taux_pauvreté_2015_2024.csv", index=False)