# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 16:16:10 2019

@author: Utente
"""

import utilities as util, csv_operations as c_op
import math as m
import random


def rankingForPrediction(weight_list, w):
    for weight in weight_list:
        weight[1] = w * weight[1]  
        

def rankingForCost(restaurants, weight_list, cost, w):
    #ranking for cost
    if((cost == "$") or (cost == "$$") or (cost == "$$$")):
        for restaurant in restaurants:
            category = restaurant[4]
            first_index = category.find(cost)
            if(first_index) > -1:
                if(cost == "$$$"):
                    if(category.find("$$$$") > -1):
                        index = util.findUrlIntoWeightsList(restaurant[0], weight_list)
                        updateWeight(index, restaurant[0], weight_list, (w * 1))                         
                last_index = first_index + len(cost)
                if((first_index - 1) < 0):
                    if(last_index == len(category)):
                        controls = True
                    else:
                        controls = (category[last_index] != '$')
                else:
                    controls = (category[first_index - 1] != '$' and category[last_index] != '$')
                if(controls):
                    index = util.findUrlIntoWeightsList(restaurant[0], weight_list)
                    updateWeight(index, restaurant[0], weight_list, (w * 1))
    
    
def rankingForMeal(restaurants, weight_list, meal, w):
    meal_up = meal.upper()
    if((meal_up == "COLAZIONE") or (meal_up == "PRANZO") or (meal_up == "CENA")):
        for restaurant in restaurants:
            if(restaurant[9].upper().find(meal_up) != -1):
                index = util.findUrlIntoWeightsList(restaurant[0], weight_list)
                updateWeight(index, restaurant[0], weight_list, (w * 1))
                    
                    
def updateWeight(index, url, weight_list, increment):
    if(index != -1):
        weight_list_elem = weight_list[index]
        weight_list.remove(weight_list[index])
        weight_list_elem[1] += increment
        weight_list.append(weight_list_elem)
    else:
        weight_list_elem = [url, increment]
        weight_list.append(weight_list_elem)
		

def calculateDF(places, about, column):
    df_list = []
    for value, elem in enumerate(about):
        df = [elem, 0]
        for place in places:
           details = place[column].upper() 
           if(details.find(elem.upper()) != -1):   
               df[1] += 1
        df_list.insert(value, df)
    return df_list
        
            
def calculateWeightForAbout(places, weight_list, about, column, w):
    df_list = calculateDF(places, about, column)
    for place in places:
        details = place[column].upper()
        for value, elem in enumerate(about):
            if(details.find(elem.upper()) != -1):
                index= util.findUrlIntoWeightsList(place[0], weight_list)
                num_places = len(places)
                df = df_list[value][1]
                increment = m.log10(num_places / df)
                updateWeight(index, place[0], weight_list, (w * increment))
                
                
def rankingForDetails(interests, places, weight_list, about, w):
    if(about):
        if(interests == 1): 
            column = 7
            calculateWeightForAbout(places, weight_list, about, column, w)
            column = 8
            calculateWeightForAbout(places, weight_list, about, column, w)
        elif(interests == 2):
            column = 8
            calculateWeightForAbout(places, weight_list, about, column, w)
        else:
            column = 6
            calculateWeightForAbout(places, weight_list, about, column, w)
    
    
def rankingForPosition(places, weight_list, city, position, w):
    if(position or city):
        csv_name1 = "dataset/coordinates places.csv"
        coordinates_places = c_op.readCoordinateCsv(csv_name1)
        MAX_DISTANCE = 60000 #metri
        if((not city) and position):
            i = 0
            for place in places:
                if(i != 0):
                    coordinate_place = util.findCoordinate(coordinates_places, place[0])
                    if(coordinate_place):
                        lat1 = float(coordinate_place[1])
                        lon1 = float(coordinate_place[2])
                        lat2 = position[0]
                        lon2 = position[1]
                        distance = util.calculateDistance(lat1, lon1, lat2, lon2)
                        increment = 1 - (distance / MAX_DISTANCE)
                        index= util.findUrlIntoWeightsList(place[0], weight_list)
                        updateWeight(index, place[0], weight_list, (w * increment))
                i += 1
        elif(city):
            csv_name2 = "dataset/coordinates cities.csv"
            coordinates_cities = c_op.readCoordinateCsv(csv_name2)
            i = 0
            for place in places:
                if(i != 0):
                    coordinate_place = util.findCoordinate(coordinates_places, place[0]) 
                    coordinate_city = util.findCoordinateCity(coordinates_cities, city)                 
                    if(coordinate_place and coordinate_city):
                        lat1 = float(coordinate_place[1])
                        lon1 = float(coordinate_place[2])
                        lat2 = float(coordinate_city[1])
                        lon2 = float(coordinate_city[2])
                        distance = util.calculateDistance(lat1, lon1, lat2, lon2) 
                        if(distance > 0):
                            increment = 1 - (distance / MAX_DISTANCE)
                            index= util.findUrlIntoWeightsList(place[0], weight_list)
                            updateWeight(index, place[0], weight_list, (w * increment) ) 
                i += 1
                    
                    
def rankingForRatings(places, weight_list, column_avg, column_ratings, max_n_ratings, w):
    i = 0
    for place in places:
        if(i != 0):
            n_ratings = float(place[column_ratings].replace('.', ''))      
            if(n_ratings != 0 and place[column_avg] != '-'):
                avg = float(place[column_avg])
                increment = (avg / 5) * (n_ratings / max_n_ratings)
                index= util.findUrlIntoWeightsList(place[0], weight_list)
                updateWeight(index, place[0], weight_list, (w * increment))
        i += 1

       
def rankingRestaurants(restaurants, weight_list_pred, cost, meal, about_restaurants, city, position, max_n_ratings):
    w0 = 0.1
    w1 = 0.15
    w2 = 0.25
    w3 = 0.25
    w4 = 0.2
    w5 = 0.05
    rankingForPrediction(weight_list_pred, w0)
    restaurants = c_op.CsvToFile("ristoranti")
    weight_list = []
    rankingForCost(restaurants, weight_list, cost, w1)
    rankingForMeal(restaurants, weight_list, meal.upper(), w2)
    interests = 2
    rankingForDetails(interests, restaurants, weight_list, about_restaurants, w3)
    rankingForPosition(restaurants, weight_list, city, position, w4)
    column_avg = 7
    column_ratings = 6
    rankingForRatings(restaurants, weight_list, column_avg, column_ratings, max_n_ratings, w5)
    intersectWeight(weight_list, weight_list_pred)
    return util.orderingPlaces(restaurants, weight_list)


def intersectWeight(weight_list, weight_list_pred):
	for elem in weight_list_pred:
		url = elem[0]
		for elem2 in weight_list:
			if(elem2[0] == url):
				elem2[1] += elem[1]
				break;
				

def rankingHotels(hotels, weight_list_pred, about_hotels, city, position,max_n_ratings):
    w0 = 0.2
    w1 = 0.4
    w2 = 0.35
    w3 = 0.05
    configuration = random.randint(0,2)
    rankingForPrediction(weight_list_pred, w0)
    hotels = c_op.CsvToFile("hotel")
    weight_list = []
    interests = 1
    rankingForDetails(interests, hotels, weight_list, about_hotels, w1)
    rankingForPosition(hotels, weight_list, city, position, w2)
    column_avg = 6
    column_ratings = 4
    rankingForRatings(hotels, weight_list, column_avg, column_ratings, max_n_ratings, w3)
    intersectWeight(weight_list, weight_list_pred)
    return util.orderingPlaces(hotels, weight_list)
    
    
    
def rankingPlaces(places, weight_list_pred, about_places, city, position, max_n_ratings):
    w0 = 0.2
    w1 = 0.4
    w2 = 0.3
    w3 = 0.1

    rankingForPrediction(weight_list_pred, w0)
    places = c_op.CsvToFile("altro")
    weight_list = []
    interests = 3
    rankingForDetails(interests, places, weight_list, about_places, w1)
    rankingForPosition(places, weight_list, city, position, w2)
    column_avg = 5
    column_ratings = 4
    rankingForRatings(places, weight_list, column_avg, column_ratings, max_n_ratings, w3)
    intersectWeight(weight_list, weight_list_pred)
    return util.orderingPlaces(places, weight_list)