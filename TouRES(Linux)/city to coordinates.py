# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:41:02 2019

@author: Utente
"""

import csv
import googlemaps


def getCoordinates(gmaps, cities, filewriter): 
        for elem in cities:
            city = elem
            result = gmaps.geocode(city)
            filewriter.writerow([city, result[0]["geometry"]["location"]["lat"], result[0]["geometry"]["location"]["lng"]])
                

gmaps = googlemaps.Client(key = 'YOUR KEY')
with open('dataset/coordinates cities.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL )
    filewriter.writerow(["CITY", "LAT", "LON"])
    cities = ["Acquaviva", "Adelfia", "Alberobello", "Altamura", "Bari", "Binetto", "Bitetto", "Bitonto", "Bitritto", "Capurso", "Casamassima", "Cassano", "Cellamare", "Conversano", "Corato", "Gioia", "Giovinazzo", "Gravina", "Locorotondo", "Modugno", "Mola", "Molfetta", "Monopoli", "Noci", "Noicattaro", "Poggiorsini", "Polignano", "Putignano", "Rutigliano", "Ruvo", "Terlizzi", "Toritto", "Triggiano", "Turi", "Valenzano"]
    res = getCoordinates(gmaps, cities, filewriter)
