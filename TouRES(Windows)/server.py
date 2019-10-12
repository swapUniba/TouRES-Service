# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 18:11:12 2019

@author: Utente
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from services import parser as ps, utilities as util, csv_operations as csv_op, ranking_operations as ro
import numpy 
from keras.models import load_model
import tensorflow as tf
import socket
   
global graph

app = Flask(__name__)
CORS(app, supports_credentials = True)
tf.logging.set_verbosity (tf.logging.ERROR)

if __name__ == "main":
    app.run(threaded = True)
    
    
#this method loads the .h5 files that describe the structure of the three networks
def getModels():
    global hotels_network, graph
    hotels_network = load_model('neural_networks/h5/hotels network.h5')
    graph = tf.get_default_graph()

    global restaurants_network
    restaurants_network = load_model('neural_networks/h5/restaurants network.h5')
  
    global places_network
    places_network = load_model('neural_networks/h5/places network.h5')
    print("\n ***Models loaded!***\n")  
#_____________________________________________________________________________________
    
print("Loading Keras models...\n")
getModels()
hotel_csv = 'dataset/HOTEL BARI E PROVINCIA.csv'
restaurants_csv = 'dataset/RISTORANTI BARI E PROVINCIA.csv'
places_csv = 'dataset/LUOGHI D\'INTERESSE BARI E PROVINCIA.csv'
max_n_ratings_hotels = csv_op.maxRatings(hotel_csv, 4)
max_n_ratings_restaurants = csv_op.maxRatings(restaurants_csv, 6)
max_n_ratings_places = csv_op.maxRatings(places_csv, 4)
DEFAULT_VALUE = -1
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname) 
print("Server IP Address is:" + IPAddr) 
 

#this method will be executed every time a request is received 
#returns result of operation required from client  
@app.route('/', methods=['POST'])
def predict():                 
    if (request.method == 'POST'):
        some_json = request.get_json(force = True)
        if(util.checkTypeOfInputs(some_json)):
            interests = ps.parserInterests(some_json['interests']  if('interests' in some_json)  else "")          
            age = ps.parserAge(some_json['age']  if('age' in some_json)  else DEFAULT_VALUE)
            gender = ps.parserGender(some_json['gender']  if('gender' in some_json)  else "")
            humor = ps.parserHumor(some_json['humor']  if('humor' in some_json)  else DEFAULT_VALUE)
            sleep = ps.parserSleep(some_json['sleep']  if('sleep' in some_json)  else "")
            physical_activity = ps.parserPhysical_activity(some_json["physical activity"]  if('physical activity' in some_json)  else "")
            health = ps.parserHealth(some_json['health']  if('health' in some_json)  else "")
            if('personality' in some_json):
                extraversion, agreeableness, conscientiousness, neuroticism, openness = ps.parserPersonality(some_json['personality'])  
            else:
                personality = []
                for i in range(0, 5):
                    personality.append(DEFAULT_VALUE)
                extraversion = personality[0]
                agreeableness = personality[1]
                conscientiousness = personality[2]
                neuroticism = personality[3]
                openness = personality[4]
        else:
            print("\n------------------------CONNECTION WITH " + request.remote_addr + "------------------------")
            print("Message: one or more inputs are in an invalid format!")
            return jsonify({'success': False, 'message': "Invalid type of inputs!"}) , 400
        
        #if the features field has no elements or does not exist, proceed with the recommendation
        if('features' not in some_json or (not some_json['features'])):
            print("\n------------------------RECOMMENDATION FOR " + request.remote_addr + "------------------------")
            cost = ps.parserCost(some_json['cost'])  if('cost' in some_json)  else ""
            meal = some_json['meal']  if('meal' in some_json)  else ""
            details = some_json['details']   if('details' in some_json)  else []  
            city = some_json['city']  if('city' in some_json) else ""
            position = some_json['position'] if('position' in some_json)  else []

            user_data = numpy.array([[age, gender, humor, physical_activity, sleep, health, extraversion, agreeableness, conscientiousness, neuroticism, openness]])
            if interests == 1:
                with graph.as_default():
                    prediction = hotels_network.predict(user_data)
                rounded_prediction = numpy.around(prediction)
                print("[HOTELS] output neural network: ", end = " ")
                hotels, explanations_list, weight_list = csv_op.findHotels(rounded_prediction)
                ranked_hotels = ro.rankingHotels(hotels, weight_list, details, city, position, max_n_ratings_hotels)    
                print("Message: recommendation sent correctly!")
                return util.createOutJson(ranked_hotels, explanations_list, interests)
            elif interests == 2:
                with graph.as_default():
                    prediction = restaurants_network.predict(user_data)
                rounded_prediction = numpy.around(prediction)
                print("[RESTAURANTS] output neural network: ", end = " ")
                restaurants, explanations_list, weight_list = csv_op.findRestaurants(rounded_prediction) 
                ranked_restaurants = ro.rankingRestaurants(restaurants, weight_list, cost, meal, details, city, position, max_n_ratings_restaurants)
                print("Message: recommendation sent correctly!")
                return util.createOutJson(ranked_restaurants, explanations_list, interests)
            elif interests == 3:
                with graph.as_default():
                    prediction = places_network.predict(user_data)
                rounded_prediction = numpy.around(prediction)
                print("[PLACES] output neural network: ", end = " ")
                places, explanations_list, weight_list = csv_op.findPlaces(rounded_prediction)
                ranked_places = ro.rankingPlaces(places, weight_list, details, city, position, max_n_ratings_places)
                print("Message: recommendation sent correctly!")
                return util.createOutJson(ranked_places, explanations_list, interests)
            else:
                with graph.as_default():
                    prediction1 = hotels_network.predict(user_data)
                with graph.as_default():
                    prediction2 = restaurants_network.predict(user_data)
                with graph.as_default():
                    prediction3 = places_network.predict(user_data)
                rounded_prediction1 = numpy.around(prediction1)
                print("[HOTELS] output neural network: ", end = " ")
                hotels, explanations_hotels, weight_list1 = csv_op.findHotels(rounded_prediction1)
                ranked_hotels = ro.rankingHotels(hotels, weight_list1, details, city, position, max_n_ratings_hotels)
                
                rounded_prediction2 = numpy.around(prediction2)
                print("[RESTAURANTS] output neural network:", end = " ")
                restaurants, explanations_restaurants, weight_list2 = csv_op.findRestaurants(rounded_prediction2) 
                ranked_restaurants = ro.rankingRestaurants(restaurants, weight_list2, cost, meal, details, city, position, max_n_ratings_restaurants)
                
                rounded_prediction3 = numpy.around(prediction3)
                print("[PLACES] output neural network: ", end = " ")
                places, explanations_places, weight_list3 = csv_op.findPlaces(rounded_prediction3) 
                ranked_places = ro.rankingPlaces(places, weight_list3, details, city, position,max_n_ratings_places)
                print("Message: recommendation sent correctly!")
                return util.aggregationPlaces(ranked_hotels, ranked_restaurants, ranked_places, explanations_hotels, explanations_restaurants, explanations_places)        
        elif(some_json["features"]):
            print("\n--------------------DATA FOR OPTIMIZATION FROM " + request.remote_addr + "--------------------")
            if(util.checkFeatures(some_json)):
                features = some_json["features"]
                if(interests == 1):
                    stereotype = [age, gender, humor, physical_activity, sleep, health, extraversion, agreeableness, conscientiousness, neuroticism, openness, features[0], features[1], features[2], features[3], features[4], features[5], features[6], features[7], features[8]]
                    csv_stereotypies = 'neural_networks/stereotypies/hotels stereotypies.csv'
                    csv_op.addStereotype(csv_stereotypies, stereotype)
                elif(interests == 2):
                    stereotype = [age, gender, humor, physical_activity, sleep, health, extraversion, agreeableness, conscientiousness, 
                              neuroticism, openness, features[0], features[1], features[2], features[3], features[4], features[5], features[6], 
                              features[7], features[8], features[9], features[10], features[11], features[12], features[13], features[14], features[15], features[16], features[17], features[17], features[18]]
                    csv_stereotypies = 'neural_networks/stereotypies/restaurants stereotypies.csv'
                    csv_op.addStereotype(csv_stereotypies, stereotype)
                elif(interests == 3):
                    stereotype = [age, gender, humor, physical_activity, sleep, health, extraversion, agreeableness, conscientiousness, 
                              neuroticism, openness, features[0], features[1], features[2], features[3], features[4], features[5], features[6], 
                              features[7], features[8], features[9], features[10], features[11], features[12], features[13], features[14], features[15], features[16], features[17], features[17], features[18]]
                    csv_stereotypies = 'neural_networks/stereotypies/places stereotypies.csv'
                    csv_op.addStereotype(csv_stereotypies, stereotype)
                else:
                    print("Message: not specified interests!")
                    return jsonify({'success': False, 'message': "Not specified interests! "}), 400
            else:
                print("Message: invalid features!")
                return jsonify({'success': False, 'message': "Invalid features!"}), 400  
            print("Message: stereotype added!")
            return jsonify({'success': True}), 200             
    else:
        print("\n------------------------CONNECTION WITH " + request.remote_addr + "------------------------")
        print("Message: invalid request!")
        return jsonify({'success': False, 'message': "Invalid request!"}), 400    