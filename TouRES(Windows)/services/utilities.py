# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:33:24 2019

@author: Utente
"""

from flask import jsonify
import math as m 
from services import csv_operations as csv_op
 

def checkInput(some_json, field, type_field):
    if(field in some_json):
        if(type(some_json[field]) != type_field):
            return False
    return True


def checkInputTypeList(some_json, field, type_elem):
    if(field in some_json):
            if(type(some_json[field]) != list):
                return False
            else:
                for elem in some_json[field]:
                    if(type(elem) != type_elem):
                        return False
    return True
        

def checkTypeOfInputs(some_json):
    check = (checkInput(some_json, 'interests', str) and checkInput(some_json, 'age', int) and checkInput(some_json, 'gender', str) and checkInput(some_json,'humor', int) 
        and checkInput(some_json, 'sleep', str) and checkInput(some_json, 'physical activity', str) and checkInput(some_json, 'health', str) 
        and checkInput(some_json, 'cost', str) and checkInput(some_json, 'meal', str) and checkInput(some_json, 'city', str))
    if(check): 
        check = (checkInputTypeList(some_json, 'personality', int) and checkInputTypeList(some_json, 'features', int) and checkInputTypeList(some_json, 'details', str))
        if(check):
            if('position' in some_json):
                if(type(some_json['position']) != list):
                    return False
                else:
                    if(len(some_json['position']) != 2):
                        return False
                    else:
                        for elem in some_json['position']:
                            if(type(elem) != float):
                                return False 
    else:
        return False
    return True
    
    
def findUrlIntoWeightsList(url, weight_list):
    for value, elem in enumerate(weight_list):
        if(elem[0] == url):
            return value
    return -1


def checkLen(features, features_len):
    if(len(features) == features_len):
        return True
    else:
        return False

    
def checkFeatures(some_json):
    field = "features"
    type_elem = int
    features = some_json[field]
    if(field in some_json):
            if(type(features) != list):
                return False
            else:
                for elem in features:
                    if(type(elem) != type_elem):
                        return False
                    if(elem != 0 and elem != 1):
                        return False
    if('interests' in some_json):
        if(validationFeatures(features)):
            if(some_json['interests'] == "hotel"):
                return checkLen(features, 9)
            if(some_json['interests'] == "ristoranti"):
                return checkLen(features, 20)    
            if(some_json['interests'] == "altro"):
                return checkLen(features, 20) 
    return True
            
 
#Check that at least one value is 1
def validationFeatures(features):
    flag = False
    for feature in features:
        if(feature == 1):
            return True
    return flag


def createOutput(places_filtered, explan_list_filtered, interests):
    output = []
    places_explan = []
    for place in places_filtered:
        url = place[0]
        for explanation in explan_list_filtered:
            if(url in explanation):
                explanation.pop(0)
                places_explan = explanation
                break
        if(interests == 1):
            category = "hotels"
            info = place[7]
            column_weight = 9
        elif(interests == 2):
            category = "ristoranti"
            info = place[4]
            column_weight = 11
        else:
            category = "luoghi da visitare"
            info = place[6]
            column_weight = 9
        image = csv_op.findImage(place[0])
        res = {"category": category, "url": place[0], "name": place[1], "address": place[2], "city": place[3], "weight": place[column_weight], "info": info, "explanations": places_explan, "image": image}
        output.append(res)
    return output
    
    
def createOutJson(places_filtered, explan_list, interests):
    output = createOutput(places_filtered, explan_list, interests)
    return jsonify({'success': True, 'result': output}), 200


def findRelevantPlace(places):
    max = -m.inf
    relevant_place = []
    for place in places:
        if(place['weight'] > max):
            max = place['weight']
            relevant_place = place
    places.remove(relevant_place)
    return relevant_place   
 
    
def orderingPlaces(places, weight_list):             
      ranked_places = []
      n_places = 0
      MAX_PLACES = 10
      while(weight_list and n_places < MAX_PLACES):
          weight_max = findMaxWeight(weight_list)
          url = weight_max[0]
          place = findPlace(places, url)
          if(place):
              place.append(weight_max[1])
              ranked_places.append(place)
              n_places += 1
      return ranked_places
  

def orderingAggregatedPlaces(places):             
      ranked_places = []
      n_places = 0
      MAX_PLACES = 10
      while((places) and n_places < MAX_PLACES):
          place = findRelevantPlace(places)
          if(place):
              ranked_places.append(place)
              n_places += 1
      return ranked_places


#This method builds output json when the tourist does not specify the interests
def aggregationPlaces(hotels, restaurants, places, explan_hotels, explan_restaurants, explan_places):
    out_hotels = createOutput(hotels, explan_hotels, 1)
    out_restaurants = createOutput(restaurants, explan_restaurants, 2)
    out_places = createOutput(places, explan_places, 3)
    output = out_hotels + out_restaurants + out_places
    return jsonify({'succes':  True, 'result': orderingAggregatedPlaces(output)}), 200 

    
def degreesToRadians(degrees):
  return degrees * m.pi / 180;


def calculateDistance(lat1, lon1, lat2, lon2):    
    earthRadiusKm = 6371
    dLat = degreesToRadians(lat2 - lat1)
    dLon = degreesToRadians(lon2 - lon1)
     
    lat1 = degreesToRadians(lat1)
    lat2 = degreesToRadians(lat2)

    a = m.sin(dLat / 2) * m.sin(dLat / 2) + m.sin(dLon / 2) * m.sin(dLon / 2) * m.cos(lat1) * m.cos(lat2) 
    c = 2 * m.atan2(m.sqrt(a), m.sqrt(1 - a))
    return round(earthRadiusKm * c * 1000, 3)  #distanza espressa in metri


def findCoordinate(coordinates, url):
    for coordinate in coordinates:
        if(coordinate[0] == url):
            return coordinate
    return []


def findCoordinateCity(coordinates, city):
    for coordinate in coordinates:
        if(coordinate[0] == city):
            return coordinate
    return []


#This method is used to calculate ranking
def findMaxWeight(weight_list):
    max = -m.inf
    weight_max = []
    for elem in weight_list:
        if(elem[1] > max):
            max = elem[1]
            weight_max = elem
    weight_list.remove(weight_max)
    return weight_max


def findPlace(places, url):
    for place in places:
        if(place[0] == url):
            return place
    return []