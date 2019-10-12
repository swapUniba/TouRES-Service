# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 17:54:27 2019

@author: Utente
"""


from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split, cross_val_score
from keras.wrappers.scikit_learn import KerasClassifier
import numpy as np
import pandas
import tensorflow as tf

#from matplotlib import pyplot
#import matplotlib.pyplot as plt


np.random.seed(7)
tf.logging.set_verbosity (tf.logging.ERROR)

#_______________________________________________________________________________________________
def createModel():
    model = Sequential()
    model.add(Dense(60, input_dim=11, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(45, activation='relu'))
    model.add(Dense(20, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
#________________________________________________________________________________________________ 

def placesNetwork():
    dataset = pandas.read_csv("stereotypies/places stereotypies.csv", sep=";", names=["eta", "sesso", "umore", "attivita", "riposo", "salute", "Estroversione", "Amicalita", "Coscienziosita", "Stabilità emotiva", "Apertura mentale", 
                            "siti storici", "monumenti e statue", "luoghi e punti di interesse", "siti religiosi e luoghi sacri", "chiese e cattedrali",  "edifici architettonici", "musei", "tour", "shopping", "vita notturna", "attività all aperto", "spiagge",  "giochi e divertimento", "Spa e benessere", "parchi e natura",  
                            "torri e ponti di osservazione", "biblioteche", "parchi divertimenti e acquatici", "passeggiate in siti storici", "castelli"], 
                            dtype={'eta':np.int32, 'sesso':np.int32, 'umore':np.int32, 'attivita':np.int32, 'riposo':np.int32, 'salute':np.int32, 'Estroversione': np.int32, 'Amicalita': np.int32, 'Coscienziosita': np.int32, 'Stabilità emotiva': np.int32, 'Apertura mentale': np.int32, 'siti storici':np.int32, 'monumenti e statue':np.int32, 
                                   'luoghi e punti di interesse':np.int32, 'siti religiosi e luoghi sacri':np.int32, 'chiese e cattedrali':np.int32, 'edifici architettonici':np.int32, 'musei':np.int32, 'tour':np.int32, 'shopping':np.int32, 'vita notturna':np.int32, 'attività all aperto':np.int32, 'spiagge':np.int32, 'giochi e divertimento':np.int32, 'Spa e benessere':np.int32, 
                                   'parchi e natura':np.int32, 'torri e ponti di osservazione':np.int32, 'biblioteche':np.int32, 'parchi divertimenti e acquatici':np.int32, 'passeggiate in siti storici':np.int32, 'castelli':np.int32})

    X = dataset
    X = X.drop(["siti storici", "monumenti e statue", "luoghi e punti di interesse", "siti religiosi e luoghi sacri", "chiese e cattedrali",  "edifici architettonici", "musei", "tour", "shopping", "vita notturna", "attività all aperto", "spiagge",  "giochi e divertimento", "Spa e benessere", "parchi e natura", "torri e ponti di osservazione", "biblioteche", "parchi divertimenti e acquatici", "passeggiate in siti storici", "castelli"], axis = 1)
    Y = dataset.drop(["eta", "sesso", "umore", "attivita", "riposo", "salute", "Estroversione", "Amicalita", "Coscienziosita", "Stabilità emotiva", "Apertura mentale"], axis = 1)


    X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size = 0.90, random_state = 13)

    network = createModel()
    network.fit(X_train, y_train, epochs=150, batch_size=5)

    # Salvataggio del modello
    network.save('h5/places network.h5')

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
    
#___________________________________________________________________________________________________
    
placesNetwork()
