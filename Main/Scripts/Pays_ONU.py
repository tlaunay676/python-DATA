import pandas as pd

def onu(list):
    """
    Renvoie les éléments présents dans onu mais absents de list
    """
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
    
    return sorted(set(onu) - set(list))

def pas_onu(list):
    """
    Renvoie les éléments présents dans list mais absents de onu
    """
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
    
    return sorted(set(list) - set(onu))

