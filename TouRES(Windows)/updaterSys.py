# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 09:44:51 2019

@author: Utente
"""

import datetime
import subprocess
import psutil


while(True):
    now = datetime.datetime.now()
    hour = now.hour
    minutes = now.minute
    second = now.second
    if(hour == 0 and minutes == 0 and second == 0):
        #daily update neural networks
        subprocess.call('runNetworks.bat', creationflags = subprocess.CREATE_NEW_CONSOLE)
        
        #follow code useful to server refresh
        PROCNAME = "flask.exe"
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == PROCNAME:
                proc.kill()           
        subprocess.Popen('activate_server.bat', creationflags = subprocess.CREATE_NEW_CONSOLE)              