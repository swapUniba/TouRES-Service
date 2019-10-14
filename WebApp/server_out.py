# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 18:11:12 2019

@author: Utente
"""

from flask import Flask, request,jsonify
from flask_cors import CORS
import socket
import csv

global graph

app = Flask(__name__)
CORS(app, supports_credentials = True)

if __name__ == "main":
    app.run(threaded = True)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Server IP Address is:" + IPAddr)

@app.route('/', methods=['POST'])
def html_creation():
    print("\n-----------------------Connection with:" + request.remote_addr + "-----------------------")

    result = request.get_json(force = True)
    
    f = open("raccomandazioni.html",'w')
    
    message = """<html>
    <head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="dynamicPage.css">
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
	<script src="http://code.jquery.com/jquery-latest.js"></script>
    <script src="script.js"></script>
    <body>
    <header><h1>Secondo me potrebbero interessarti</h1>
    <h3>(metti la spunta ai suggerimenti che ti piacciono)</h3></header>					
    {div1}
    {div2}
    {div3}
    {div4}
    <footer>
    <br>
    <input type="submit" id= "button0" onClick="send()" value="Fatto!"/>
    </footer>
    </body>
    </html>"""
    
    with open('sessions_tmp.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([result['interests'], result['output'][0], result['age'], result['gender'], result['details'], result['city'], result['position'],result['meal'],result['cost'],result['personality'],result['sleep'],result['health'],result['humor'],result['physical_activity']])  
    csvfile.close
            
    new_divisore2 = ""
    new_divisore3 = ""
    new_divisore4 = ""
    
    
    try:    
        if (result['output'][0][0]['image'] == '-'):
            img_src = "noimageavailable.jpg"
        else:
            img_src = result['output'][0][0]['image']
            
        divisore1 = """<div><input style='display:none' type="text" id = 'url1' value={url}/><img id= photo src= {img}><br><b><a href={url}>{luogo}</a></b>: <br><br>Si trova in {via} {città}. <br><br> Ha le seguenti info: {mot}<br><br> Mi interessa: <input style="width: 40px; height: 40px;" type="checkbox" id= "one"></div>"""
        new_divisore1 = divisore1.format(url = result['output'][0][0]['url'], img = img_src, luogo = result['output'][0][0]['name'], via = result['output'][0][0]['address'], città = result['output'][0][0]['city'], mot = result['output'][0][0]['info'])
     
        try:    
            if (result['output'][0][1]['image'] == '-'):
                img_src = "noimageavailable.jpg"
            else:
                img_src = result['output'][0][1]['image']
            
            divisore2 = """<div><input style='display:none' type="text" id = 'url2' value={url}/><img id= photo src= {img}><br><b><a href={url}>{luogo}</a></b>: <br><br>Si trova in {via} {città}. <br><br>Ha le seguenti info: {mot}<br><br> Mi interessa: <input style="width: 40px; height: 40px;" type="checkbox" id= "two"></div>"""
            new_divisore2 = divisore2.format(url = result['output'][0][1]['url'], img = img_src, luogo = result['output'][0][1]['name'], via = result['output'][0][1]['address'],città = result['output'][0][1]['city'], mot = result['output'][0][1]['info'])
            try:   
                if (result['output'][0][2]['image'] == '-'):
                    img_src = "noimageavailable.jpg"
                else:
                    img_src = result['output'][0][2]['image']
            
                divisore3 = """<div><input style='display:none' type="text" id = 'url3' value={url}/><img id= photo src= {img}><br><b><a href={url}>{luogo}</a></b>: <br><br>Si trova in {via} {città}. <br><br>Ha le seguenti info: {mot}<br><br> Mi interessa: <input style="width: 40px; height: 40px;" type="checkbox" id= "three"></div>"""
                new_divisore3 = divisore3.format(url = result['output'][0][2]['url'], img = img_src, luogo = result['output'][0][2]['name'], via = result['output'][0][2]['address'], città = result['output'][0][2]['city'],mot = result['output'][0][2]['info'])
            except: 
                new_divisore3 = ""  
                try:                        
                    divisore4 = """<div><img id= photo src= {img}><br><b><a href={url}>{luogo}</a></b>: <br><br>Si trova in {via} {città}. <br><br>Ha le seguenti info: {mot}<br><input type="submit" id= "button0" onClick="like()" value=" Mi interessa!"></div>"""
                    new_divisore4 = divisore4.format(luogo = result['output'][0][3]['name'], via = result['output'][0][3]['address'], città = result['output'][0][3]['city'],mot = result['output'][0][3]['info'])
                except: 
                    new_divisore4 = ""  
        except: 
            new_divisore2 = ""    
    except: 
        new_divisore1 ="""<div>Mi dispiace, non sono riuscito a trovare alcun luogo che soddisfa le tue necessita :(</div>"""
    
     
    
    new_message = message.format(div1 = new_divisore1, div2 = new_divisore2, div3 = new_divisore3, div4 = new_divisore4)
    
    f.write(new_message)
    f.close()
    return jsonify({'success': True}), 200
