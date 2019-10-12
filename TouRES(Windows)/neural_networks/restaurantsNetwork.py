# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:28:39 2019

@author: Utente
"""

from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split, cross_val_score
from keras.wrappers.scikit_learn import KerasClassifier
from keras.models import load_model
import numpy as np
import pandas
import tensorflow as tf

#from matplotlib import pyplot
#mport matplotlib.pyplot as plt


np.random.seed(7)
tf.logging.set_verbosity (tf.logging.ERROR)

#_______________________________________________________________________________________________
def createModel():
    model = Sequential()
    model.add(Dense(70, input_dim = 11, activation = 'relu'))
    model.add(Dense(40, activation = 'relu'))
    model.add(Dense(40, activation = 'relu'))
    model.add(Dense(20, activation = 'sigmoid'))
    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    return model

#________________________________________________________________________________________________ 

def restaurantsNetwork():
    dataset = pandas.read_csv("neural_networks/stereotypies/restaurants stereotypies.csv", sep=";", names=["eta", "sesso", "umore", "attivita", "riposo", "salute", "Estroversione", "Amicalita", "Coscienziosita", "Stabilità emotiva", "Apertura mentale", "italiana", "pizza", "pesce", "mediterranea", "fusion", 
                              "pasticcerie", "gelaterie", "bar", "greca", "pub", "giapponese", "fast food", "steakhouse", "francese", "birreria", "europea", "americana", "cinese", "asiatica", "gastronomia"], 
                              dtype={'eta':np.int32, 'sesso':np.int32, 'umore':np.int32, 'attivita':np.int32, 'riposo':np.int32, 'salute':np.int32, 'Estroversione': np.int32, 'Amicalita': np.int32, 'Coscienziosita': np.int32, 'Stabilità emotiva': np.int32, 'Apertura mentale': np.int32, 'italiana':np.int32, 'pizza':np.int32, 'pesce':np.int32, 'maditerranea':np.int32, 'fusion':np.int32, 'pasticcerie':np.int32, 
                                     'gelaterie':np.int32, 'bar':np.int32, 'greca':np.int32, 'pub':np.int32, 'giapponese':np.int32, 'fast food':np.int32, 'steakhouse':np.int32, 'francese':np.int32, 'birreria':np.int32, 'europea':np.int32, 'americana':np.int32, 'cinese':np.int32, 'asiatica':np.int32, 'gastronomia':np.int32})

    X = dataset
    X = X.drop(["italiana", "pizza", "pesce", "mediterranea", "fusion", "pasticcerie", "gelaterie", "bar", "greca", "pub", "giapponese", "fast food", "steakhouse", "francese", "birreria", "europea", "americana", "cinese", "asiatica", "gastronomia"], axis = 1)
    Y = dataset.drop(["eta", "sesso", "umore", "attivita", "riposo", "salute", "Estroversione", "Amicalita", "Coscienziosita", "Stabilità emotiva", "Apertura mentale"], axis = 1)

    X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size = 0.90, random_state = 13)

    network = createModel()
    network.fit(X_train, y_train, epochs=100, batch_size=5)
    
    # Salvataggio del modello
    network.save('neural_networks/h5/restaurants network.h5')
    
    scores = network.evaluate(X_train, y_train)
    print("\n%s: %.2f%%" % (network.metrics_names[1], scores[1]*100))
    

    """
    predictions = network.predict(X_test)
    rounded = np.around(predictions)
    
    
    #evaluation
    network_model = KerasClassifier(build_fn=createModel, epochs=100, batch_size=5, verbose=0)
    cv_scores = cross_val_score(network_model, X, Y, cv = 5)
    print('\ncv_scores mean:{}'.format(np.mean(cv_scores)))
    print('\ncv_score variance:{}'.format(np.var(cv_scores)))
    print('\ncv_score dev standard:{}'.format(np.std(cv_scores)))
    
    data = {'variance': np.var(cv_scores), 'standard dev': np.std(cv_scores)}
    names = list(data.keys())
    values = list(data.values())
    fig,axs = plt.subplots(1, 1, figsize=(6, 3), sharey=True)
    axs.bar(names, values)"""
    
#____________________________________________________________________________________________________
    
restaurantsNetwork()