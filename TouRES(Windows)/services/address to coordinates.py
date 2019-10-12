# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 18:00:23 2019

@author: Utente
"""

import csv
import googlemaps


def getCoordinates(gmaps, csv_name, filewriter):
    with open(csv_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';') 
        i = 0
        for value, row in enumerate(reader, 1):
            if(i != 0):
                address = row[2] + ", " + row[3] 
                result = gmaps.geocode(address)
                filewriter.writerow([row[0], result[0]["geometry"]["location"]["lat"], result[0]["geometry"]["location"]["lng"]])
            elif(i == 0):
                i += 1
#_________________________________________________________________________________                

gmaps = googlemaps.Client(key = 'YOUR KEY')
with open('../dataset/coordinates.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL )
    filewriter.writerow(["URL", "LAT", "LON"])
    hotel_csv = '../dataset/HOTEL BARI E PROVINCIA.csv'
    restaurants_csv = '../dataset/RISTORANTI BARI E PROVINCIA.csv'
    places_csv = '../dataset/LUOGHI D\'INTERESSE BARI E PROVINCIA.csv'  
    getCoordinates(gmaps, hotel_csv, filewriter)
    getCoordinates(gmaps, restaurants_csv, filewriter)
    getCoordinates(gmaps, places_csv, filewriter)
    

    



    

        


        