# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 11:53:33 2019

@author: Utente
"""

from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import pandas
import tensorflow as tf
from sklearn.model_selection import train_test_split, cross_val_score
#from keras.wrappers.scikit_learn import KerasClassifier
#from matplotlib import pyplot
#import matplotlib.pyplot as plt

np.random.seed(7)
tf.logging.set_verbosity (tf.logging.ERROR)

#_______________________________________________________________________________________________
def createModel():
    model = Sequential()
    model.add(Dense(30, input_dim=11, activation='relu'))
    model.add(Dense(30, activation='relu'))
    model.add(Dense(9, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

#________________________________________________________________________________________________ 

def hotelsNetwork():
    dataset = pandas.read_csv("neural_networks/stereotypies/hotels stereotypies.csv", sep=";", names=["eta", "sesso", "umore", "attivita", "riposo", "salute", "Estroversione", "Amicalita", "Coscienziosita", "Stabilità emotiva", "Apertura mentale", "ristorante", "bar", "piscina", "parcheggio", "spa", "animali ammessi", "centro fitness", "wifi", "servizio in camera"], 
                              dtype={'eta':np.int32, 'sesso':np.int32, 'umore':np.int32, 'attivita':np.int32, 'riposo':np.int32, 'salute':np.int32, 'Estroversione': np.int32, 'Amicalita': np.int32, 'Coscienziosita': np.int32, 'Stabilità emotiva': np.int32, 'Apertura mentale': np.int32, 'ristorante':np.int32, 'bar':np.int32, 'piscina':np.int32, 'parcheggio':np.int32, 'spa':np.int32, 'animali ammessi':np.int32, 'centro fitness':np.int32, 'wifi':np.int32, 'servizio in camera':np.int32})

    X = dataset
    X = X.drop(["ristorante", "bar", "piscina", "parcheggio", "spa", "animali ammessi", "centro fitness", "wifi", "servizio in camera"], axis = 1)
    Y = dataset.drop(["eta", "sesso", "umore", "attivita", "riposo", "salute", "Estroversione", "Amicalita", "Coscienziosita", "Stabilità emotiva", "Apertura mentale"], axis = 1)


    X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size = 0.90, random_state = 13)

    network = createModel()
    network.fit(X, Y, epochs=100, batch_size=5)

    # Salvataggio del modello
    network.save('neural_networks/h5/hotels network.h5')

    scores = network.evaluate(X, Y)
    print("\n%s: %.2f%%" % (network.metrics_names[1], scores[1]*100))

    """
    predictions = network.predict(X)
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
    
#__________________________________________________________________________________________________

hotelsNetwork()