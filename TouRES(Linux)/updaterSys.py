# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 09:44:51 2019

@author: Utente
"""

import datetime
import subprocess
import psutil
import os


while(True):
    now = datetime.datetime.now()
    hour = now.hour
    minutes = now.minute
    second = now.second
    if(hour == 12 and minutes == 42 and second == 0):
        #daily update neural networks
        """subprocess.call('sh runNetworks.sh', shell=True)
        os.system("echo $(date '+%Y-%m-%d') Update completed! ")"""
        
        #follow code useful to server refresh         
        #subprocess.call(['open', '--force', '-a', 'Terminal.app', 'bash', 'activate_server.sh'])              
