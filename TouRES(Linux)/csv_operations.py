# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 12:02:35 2019

@author: Utente
"""

import csv
import math as m


def CsvToFile(key):
    places = []
    if(key == "ristoranti"):
        csv_name = 'dataset/RISTORANTI BARI E PROVINCIA.csv'
    elif(key == "hotel"): 
        csv_name = 'dataset/HOTEL BARI E PROVINCIA.csv'
    else:
        csv_name = 'dataset/LUOGHI DA VISITARE BARI E PROVINCIA.csv'	  
    with open(csv_name, newline='', encoding='latin-1') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';')
        for value, row in enumerate(reader, 1):
            places.append(row)
    return places
		

def findImage(url):
    with open("dataset/images.csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';')
        for value, row in enumerate(reader, 1):
            if(row[0] == url):
                csvfile.close() 
                return row[1]
    return "-"
    
        

def maxRatings(csv_name, column):
    with open(csv_name, newline='', encoding='latin-1') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';')
        max_n_ratings = -999999
        for value, row in enumerate(reader, 1):
            if(value != 1):
                ratings = int(row[column])
                if(ratings > max_n_ratings):
                    max_n_ratings = ratings
    csvfile.close() 
    return max_n_ratings

  
def readCoordinateCsv(csv_name):
    with open(csv_name, newline='', encoding='latin-1') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';') 
        coordinates = []
        for value, coordinate in enumerate(reader, 1):
            coordinates.append(coordinate)
    return coordinates
        
        
        
def addStereotype(csv_stereotypes, stereotype):
    with open(csv_stereotypes, 'a', newline="", encoding='latin-1') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        filewriter.writerow(stereotype)
    csvfile.close()


#This method checks that a row contains the filter derived from the prediction
def checkRow(row, services, pred_filter, filter, list, explanations_row):
    occurrence_features = 0
    if(pred_filter == 1):
        if (services.find(filter)) >= 0:
            if(not(row in list)):
                list.append(row)
            explanations_row.append(filter.lower())
            occurrence_features =  occurrence_features + 1
    return occurrence_features


def iterateRows(csv_name, column, n_features, prediction, keys):
    list = []
    explanations_list = []
    weight_list = []
    filters = ""
    with open(csv_name, newline='', encoding='latin-1') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';') 
        for value, row in enumerate(reader, 1):
            services = row[column].upper()
            explanations_row = []
            occurrence_features = 0
            for i in range(n_features):
                pred = prediction.item(0, i)
                if(pred == 1 and value == 1):
                    filters = filters + keys[i] + ", "
                occurrence_features += checkRow(row, services, pred, keys[i], list, explanations_row) 
                weight = occurrence_features / n_features 
            if(row in list):
                if(occurrence_features != 0):
                    weight_list_elem = [row[0], weight]
                    weight_list.append(weight_list_elem)
                explanations_row.insert(0, row[0])
                explanations_list.append(explanations_row)    #in explanations_list ogni elemento è una lista il cui primo elem è l'url del luogo di riferimento e gli altri elem sono le spiegazioni
        csvfile.close()
        print("[", filters[0:-2], "]")
    return list, explanations_list, weight_list


def findHotels(prediction):
    hotel_csv = 'dataset/HOTEL BARI E PROVINCIA.csv'
    keys = ["RISTORANTE", "BAR", "PISCINA", "PARCHEGGIO", "SPA", "ANIMALI AMMESSI", "CENTRO FITNESS", "WIFI", "SERVIZIO IN CAMERA"]   
    column = 7
    n_features = 9
    hotels, explanations_list, weight_list = iterateRows(hotel_csv, column, n_features, prediction, keys)
    return hotels, explanations_list, weight_list
  

def findRestaurants(prediction):
    restaurants_csv = 'dataset/RISTORANTI BARI E PROVINCIA.csv'
    keys = ["ITALIANA", "PIZZA", "PESCE", "MEDITERRANEA", "FUSION", "PASTICCERIE", "GELATERIE", "BAR", "GRECA", "PUB", "GIAPPONESE", "FAST FOOD", "STEAKHOUSE", "FRANCESE", "BIRRERIA", "EUROPEA", "AMERICANA", "CINESE", "ASIATICA", "GASTRONOMIA"]
    column = 4
    n_features = 20
    restaurants, explanations_list, weight_list = iterateRows(restaurants_csv, column, n_features, prediction, keys) 
    return restaurants, explanations_list, weight_list


def findPlaces(prediction):
    places_csv = 'dataset/LUOGHI DA VISITARE BARI E PROVINCIA.csv'
    keys = ["SITI STORICI", "MONUMENTI E STATUE", "LUOGHI E PUNTI D'INTERESSE", "SITI RELIGIOSI E LUOGHI SACRI", "CHIESE E CATTEDRALI",  "EDIFICI ARCHITETTONICI", "MUSEI", "TOUR", "SHOPPING", "VITA NOTTURNA", "ATTIVITÀ ALL'APERTO", "SPIAGGE",  "GIOCHI E DIVERTIMENTO", "SPA E BENESSERE", "PARCHI E NATURA", "TORRI E PONTI DI OSSERVAZIONE", "BIBLIOTECHE", "PARCHI DIVERTIMENTI E ACQUATICI", "PASSEGGIATE IN SITI STORICI", "CASTELLI"]
    column = 6
    n_features = 20
    places, explanations_list, weight_list  = iterateRows(places_csv, column, n_features, prediction, keys) 
    return places, explanations_list, weight_list