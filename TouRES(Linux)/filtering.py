# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 13:02:05 2019

@author: Utente
"""

def filteringAbout(places, explanations_list, interests, about, column):
    if not about:
        return places
    else:
        places_filtered = []
        for place in places:
            place_in = False
            details = place[column].upper()
            for elem in about:
                if((details.find(elem.upper()) != -1) and place_in == False):
                    places_filtered.append(place)
                    place_in = True
            if(place_in == False):
                removeExplain(place[0], explanations_list)
        return places_filtered
        
        
def detailsFiltering(places, explanations_list, interests, about):
    if interests == 1:
        column = 7
        places_filtered = filteringAbout(places, explanations_list, interests, about, column)
        column = 8
        places_filtered = filteringAbout(places, explanations_list, interests, about, column)
    elif interests == 2:
        column = 8
        places_filtered = filteringAbout(places, explanations_list, interests, about, column)
    elif interests == 3:
        column = 6
        places_filtered = filteringAbout(places, explanations_list, interests, about, column)
    return places_filtered


def cityFiltering(places, explanations_list, city_name):
    if not city_name:
        return places
    else:
        places_filtered = []
        for place in places:
            city = place[3].upper()
            if(city.find(city_name.upper()) != -1):
                    places_filtered.append(place)
            else:
                removeExplain(place[0], explanations_list)
        return places_filtered        


def restaurantsFiltering(restaurants, cost, meal, explanations_list, about, city):
    restaurants_filtered = costFiltering(restaurants, cost, explanations_list)
    restaurants_filtered = hourFiltering(restaurants_filtered, meal.upper(), explanations_list)
    restaurants_filtered = cityFiltering(restaurants_filtered, explanations_list, city)
    restaurants_filtered = detailsFiltering(restaurants_filtered, explanations_list, 2, about)
    print("restaurants:",len(restaurants_filtered))
    print("exp:",len(explanations_list))
    return restaurants_filtered, explanations_list


def hotelsFiltering(hotels, explanations_list, about, city):
    hotels_filtered = cityFiltering(hotels, explanations_list, city)
    hotels_filtered = detailsFiltering(hotels_filtered, explanations_list, 1, about)
    print("hotels:",len(hotels_filtered))
    print("exp:",len(explanations_list))
    return hotels_filtered, explanations_list


def placesFiltering(places, explanations_list, about, city):
    places_filtered = cityFiltering(places, explanations_list, city)
    places_filtered = detailsFiltering(places_filtered, explanations_list, 3, about)
    print("places:",len(places_filtered))
    print("exp:",len(explanations_list))
    return places_filtered, explanations_list
    

def removeExplain(url, explanations_list):
    for explanation in explanations_list:
        if(url in explanation):
            explanations_list.remove(explanation)
            
    
def hourFiltering(restaurants, meal, explanations_list):
    if((meal == "COLAZIONE") or (meal == "PRANZO") or (meal == "CENA")):
        rest_filtered = []
        for restaurant in restaurants:
            meals = restaurant[9].upper()
            if(meals.find(meal) != -1):
                rest_filtered.append(restaurant)
            else:
                if(meals == '-'):
                    rest_filtered.append(restaurant)
                else:
                    if(meal == "CENA"):
                        if(meals.find("DOPO MEZZANOTTE") != -1):
                            rest_filtered.append(restaurant)
                        else:
                            removeExplain(restaurant[0], explanations_list)
                    else:
                        removeExplain(restaurant[0], explanations_list)    
    else:
        rest_filtered = restaurants
    return rest_filtered
    

def costFiltering(restaurants, cost, explanations_list):
    rest_filtered = []
    if((cost == "$") or (cost == "$$") or (cost == "$$$")):
        for restaurant in restaurants:
            category = restaurant[4]
            first_index = category.find(cost)
            if(first_index) > -1:
                if(cost == "$$$"):
                    if(category.find("$$$$") > -1):
                        rest_filtered.append(restaurant)
                last_index = first_index + len(cost)
                if((first_index - 1) < 0):
                    controls = (category[last_index] != '$')
                else:
                    controls = (category[first_index - 1] != '$' and category[last_index] != '$')
                if(controls):
                    if(restaurant not in rest_filtered):
                        rest_filtered.append(restaurant)
                elif(restaurant not in rest_filtered):
                    removeExplain(restaurant[0], explanations_list)
            else:
                removeExplain(restaurant[0], explanations_list)
    else:
        rest_filtered = restaurants    
    return rest_filtered