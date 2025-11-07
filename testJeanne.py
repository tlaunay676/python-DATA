import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("/home/onyxia/work/python-DATA/API_NY.GDP.PCAP.CD_DS2_fr_csv_v2_11820.csv", skiprows=4)

# 2. Garder uniquement les colonnes utiles
colonnes_utiles = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'] + [str(annee) for annee in range(1960, 2025)]
df = df[colonnes_utiles]

# 3. Filtrer pour garder uniquement le PIB par habitant
# (le code de l'indicateur pour le PIB par habitant est NY.GDP.PCAP.CD)
df_pib = df[df['Indicator Code'] == 'NY.GDP.PCAP.CD']

# 4. Supprimer les colonnes inutiles maintenant
df_pib = df_pib.drop(columns=['Indicator Name', 'Indicator Code'])

# 5. Réorganiser le tableau : on veut un format long (facile pour les graphiques)
df_long = df_pib.melt(id_vars=['Country Name', 'Country Code'], 
                      var_name='Year', 
                      value_name='GDP_per_capita_USD')

# 6. Nettoyer les données : convertir l’année en nombre et le PIB en float
df_long['Year'] = df_long['Year'].astype(int)
df_long['GDP_per_capita_USD'] = pd.to_numeric(df_long['GDP_per_capita_USD'], errors='coerce')

# 7. supprimer les lignes sans valeur
df_long = df_long.dropna(subset=['GDP_per_capita_USD'])

df_long.to_csv("PIB_par_habitant_nettoye.csv", index=False)

print(df_long.head(20))

# Graphique 
pays_selectionnes = ['France', 'United States', 'China', 'Japan', 'Germany', 'Brazil', 'India', 'South Africa', 'Canada', 'Australia']

plt.figure(figsize=(12, 7))

for pays in pays_selectionnes:
    data_pays = df_long[df_long['Country Name'] == pays]
    plt.plot(data_pays['Year'], data_pays['GDP_per_capita_USD'], label=pays)

plt.title("Évolution du PIB par habitant (USD courants)")
plt.xlabel("Année")
plt.ylabel("PIB par habitant ($ US)")
plt.legend(title="Pays")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
