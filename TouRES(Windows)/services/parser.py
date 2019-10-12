# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 17:03:23 2019

@author: Utente
"""

def parserInterests(interests):
    if interests.upper() == "HOTEL":
        return 1
    elif interests.upper() == "RISTORANTI":
        return 2
    elif interests.upper() == "ALTRO" or interests.upper() == "LUOGHI DA VISITARE":
        return 3
    else:
        return -1
    
    
def parserAge(age):
    if age < 0:
        return -1
    elif age < 18:
        return 1
    elif age >= 18 and age <= 24:
        return 2
    elif age >= 25 and age <= 32:
        return 3
    elif age >= 33 and age <= 45:
        return 4
    elif age >= 46 and age <= 58:
        return 5
    else:
        return 6
    
    
def parserGender(gender):
    if gender.upper() == "MASCHIO" or gender.upper() == "MALE" or gender.upper() == "UOMO":
        return 0
    elif gender.upper() == "FEMMINA" or gender.upper() == "FEMALE" or gender.upper() == "DONNA":
        return 1
    else:
        return -1
    
    
def parserHumor(humor):
    if(humor >= 0 or humor <= 1):
        return -1
    else:
        return humor
    
    
def parserPhysical_activity(physical_activity):
    if physical_activity.upper() == "MOLTA ATTIVITÀ":
        return 1
    elif physical_activity.upper() == "POCA ATTIVITÀ":
        return 0
    else:
        return -1  
    

def parserSleep(sleep):
    if sleep.upper() == "SUFFICIENTE":
        return 1
    elif sleep.upper() == "NON SUFFICIENTE":
        return 0
    else:
        return -1
    

def parserHealth(health):
    if health.upper() == "BUONA":
        return 1
    elif health.upper() == "NON BUONA":
        return 0
    else:
        return -1
    

def parserPersonality(personality):
    if not personality:
        return -1, -1, -1, -1, -1
    else:
        return personality[0], personality[1], personality[2], personality[3], personality[4]
    
   
def parserCost(cost):
    if cost.upper() == "ECONOMICO":
        return "$"
    elif cost.upper() == "MEDIO":
        return "$$"
    elif cost.upper() == "COSTOSO":
        return "$$$"
    else:
        return ""