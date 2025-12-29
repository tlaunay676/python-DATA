import pandas as pd

def onu(list):
    """
    Renvoie les codes pays qui font partie de la liste ONU mais qui sont absents de la liste fournie.

    Paramètres
    ----------
    list : list
        Liste de codes pays à comparer avec la liste officielle de l'ONU.

    Sortie
    ------
    list
        Liste triée des codes pays présents dans la liste ONU mais absents de la liste fournie.
    """

    # Liste officielle des codes ISO3 des pays membres de l'ONU
    onu = ["AFG","ALB","DZA","AND","AGO","ATG","ARG","ARM","AUS","AUT","AZE",
           "BHS","BHR","BGD","BRB","BLR","BEL","BLZ","BEN","BTN","BOL","BIH",
           "BWA","BRA","BRN","BGR","BFA","BDI","CPV","KHM","CMR","CAN","CAF",
           "TCD","CHL","CHN","COD","COL","COM","COG","CRI","CIV","HRV","CUB",
           "CYP","CZE","PRK","KOR","DNK","DJI","DMA","DOM","ECU","EGY","SLV",
           "ERI","ESP","EST","SWZ","ETH","FJI","FIN","FRA","GAB","GMB","GEO",
           "DEU","GHA","GRC","GRD","GTM","GIN","GNB","GNQ","GUY","HTI","HND",
           "HUN","ISL","IND","IDN","IRN","IRQ","IRL","ISR","ITA","JAM","JPN",
           "JOR","KAZ","KEN","KIR","KWT","KGZ","LAO","LVA","LBN","LSO","LBR",
           "LBY","LIE","LTU","LUX","MDG","MWI","MYS","MDV","MLI","MLT","MAR",
           "MHL","MUS","MRT","MEX","FSM","MDA","MCO","MNG","MNE","MOZ","MMR",
           "NAM","NRU","NPL","NLD","NZL","NIC","NER","NGA","MKD","NOR","OMN",
           "PAK","PLW","PAN","PNG","PRY","PER","PHL","POL","PRT","QAT","ROU",
           "GBR","RUS","RWA","KNA","LCA","VCT","WSM","SMR","STP","SAU","SEN",
           "SRB","SYC","SLE","SGP","SVK","SVN","SLB","SOM","ZAF","SSD","LKA",
           "SDN","SUR","SWE","CHE","SYR","TJK","TZA","THA","TLS","TGO","TON",
           "TTO","TUN","TUR","TKM","TUV","UGA","UKR","URY","USA","UZB","VUT",
           "VEN","VNM","YEM","ZMB","ZWE","ARE"]

    # Calcul de la différence : éléments de l'ONU absents de la liste fournie
    # set(onu) - set(list) renvoie un ensemble des codes manquants
    return sorted(set(onu) - set(list))


def pas_onu(list):
    """
    Renvoie les codes pays présents dans la liste fournie mais absents de la liste ONU.

    Paramètres
    ----------
    list : list
        Liste de codes pays à comparer avec la liste officielle de l'ONU.

    Sortie
    ------
    list
        Liste triée des codes pays présents dans la liste fournie mais non membres de l'ONU.
    """

    # Liste officielle des codes ISO3 des pays membres de l'ONU
    onu = ["AFG","ALB","DZA","AND","AGO","ATG","ARG","ARM","AUS","AUT","AZE",
           "BHS","BHR","BGD","BRB","BLR","BEL","BLZ","BEN","BTN","BOL","BIH",
           "BWA","BRA","BRN","BGR","BFA","BDI","CPV","KHM","CMR","CAN","CAF",
           "TCD","CHL","CHN","COD","COL","COM","COG","CRI","CIV","HRV","CUB",
           "CYP","CZE","PRK","KOR","DNK","DJI","DMA","DOM","ECU","EGY","SLV",
           "ERI","ESP","EST","SWZ","ETH","FJI","FIN","FRA","GAB","GMB","GEO",
           "DEU","GHA","GRC","GRD","GTM","GIN","GNB","GNQ","GUY","HTI","HND",
           "HUN","ISL","IND","IDN","IRN","IRQ","IRL","ISR","ITA","JAM","JPN",
           "JOR","KAZ","KEN","KIR","KWT","KGZ","LAO","LVA","LBN","LSO","LBR",
           "LBY","LIE","LTU","LUX","MDG","MWI","MYS","MDV","MLI","MLT","MAR",
           "MHL","MUS","MRT","MEX","FSM","MDA","MCO","MNG","MNE","MOZ","MMR",
           "NAM","NRU","NPL","NLD","NZL","NIC","NER","NGA","MKD","NOR","OMN",
           "PAK","PLW","PAN","PNG","PRY","PER","PHL","POL","PRT","QAT","ROU",
           "GBR","RUS","RWA","KNA","LCA","VCT","WSM","SMR","STP","SAU","SEN",
           "SRB","SYC","SLE","SGP","SVK","SVN","SLB","SOM","ZAF","SSD","LKA",
           "SDN","SUR","SWE","CHE","SYR","TJK","TZA","THA","TLS","TGO","TON",
           "TTO","TUN","TUR","TKM","TUV","UGA","UKR","URY","USA","UZB","VUT",
           "VEN","VNM","YEM","ZMB","ZWE","ARE"]

    # Calcul de la différence : éléments de la liste fournie absents de l'ONU
    return sorted(set(list) - set(onu))