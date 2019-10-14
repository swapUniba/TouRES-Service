# TouRES Service

# Install TouRES Service on Windows
* STEP1: Download Python3.6 from <https://www.python.org/downloads/>. Do not install version 3.7 as it may cause problems with the installation of Tensorflow.
* STEP2: open prompt and type: ```pip install virtualenv```

* STEP3: type: ```pip install numpy scipy keras tensorflow pandas flask flask-cors psutil sklearn```
* STEP4: go to the folder ***TouRES(Windows)***
* STEP5: double click on ***runNetworks.bat*** and wait for operation to complete
* STEP6: double click on ***activate_server.bat*** and double click on ***updater_system.bat***.


# Install TouRES Service on Linux

Copy the following commands in sequence

* STEP0:
```bash
$ sudo apt-get update
```
* STEP1: 
```bash
$ sudo apt-get install python3-pip
```
* STEP2:
```bash
$ sudo apt-get install python3-setuptools
```
* STEP3(to create a virtual environment):
```bash
$ pip3 install virtualenv
```
* STEP4:
```bash
$ sudo apt-get install python-psutil
$ sudo apt-get install python-dev
$ pip3 install wheel
$ sudo apt install python3-flask
$ pip3 install -U protobuf
```
* STEP5:
```bash
$ pip3 install numpy scipy keras tensorflow pandas flask flask-cors psutil sklearn
```
* STEP6:
```bash
$ sh runNetworks.sh
```
* STEP7:
```bash
$ sh activate_server.sh
```


# Alternative installation on Linux
* STEP0:
```bash
$ sudo apt-get update
```
* STEP1: 
```bash
$ sudo apt-get install python-virtualenv
```
* STEP2:
```bash
$ sudo apt-get install python3-pip
```
* STEP3(to create a virtual environment):
```bash
$ sudo pip install virtualenv
```
* STEP4:
```bash
$ cd /path/to/TouRES
```
* STEP5:
```bash
$ virtual Venv
```
* STEP6:
```bash
$ . Venv/bin/activate
```
* STEP7:
```bash
$ pip install numpy scipy keras tensorflow pandas flask flask-cors psutil sklearn
```
* STEP8:
```bash
$ sh runNetworks.sh
```
* STEP9:
```bash
$ sh activate_server.sh
```

# Testing
To test the system, you can use the web app. We need to run the batch script "activate_server_out.bat", then open the HTML page "web page Recommender.html"
