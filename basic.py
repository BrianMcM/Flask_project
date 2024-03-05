import json
import pandas as pd
from flask import Flask, jsonify
from flask import request
from flask import url_for
from flask import render_template
import os
from flask import send_file
import mysql.connector
import json


def static_data():
    print("Starting SQL Static Data Pull Package")
    HOST = "dublinbikes.c1ywqa2sojjb.eu-west-1.rds.amazonaws.com"
    USER = "admin"
    PASSWORD = "boldlynavigatingnature"
    DATABASE = "dublinbikes"


    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = connection.cursor()
    print("Connection Made")
    query = "SELECT * FROM dublinbikes.station;"
    cursor.execute(query)

    # Fetch all rows and convert to a list of dictionaries
    weather = cursor.fetchall()
    result = []

    for row in weather:
        d = {}
        for i, col in enumerate(cursor.description):
            d[col[0]] = row[i]

        result.append(d)
    print("finished")
    # Convert the list of dictionaries to JSON and print it
    json_result = json.dumps(result)
    connection.close()

    return json_result

#print(os.listdir('.'))
#print(sql_puller.static_data())

#load the relative path of website and json file
site_root = os.path.realpath(os.path.dirname(__file__))
json_name = 'dublin.json'
json_path = os.path.join(site_root, 'data', json_name)

#load json as data_json

#create a pandas dataframe of the json
df = pd.read_json(json_path)

#function which returns string from dataframe depending on which station you select(x)
def func(df,x):
    try:
        return str(df[df['number'] == x].to_string(header=None,index=False))
    except:
        return "Error"
    

def to_json2(df,orient='split'):
    df_json = df.to_json(orient = orient, force_ascii = False)
    return json.loads(df_json)



app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/index/<number>')
def index_station(number):
    return render_template('index.html',data = func(df,int(number)), station_number = number)

@app.route('/map/<number>')
def map_generator(number):
    return render_template('map_1.html')

@app.route('/get_json_data')
def get_json_data():
    try:
        #with open(json_path, 'r') as json_file:
        #    data = json.load(json_file)
        data = static_data()
        json_data = json.dumps(data)
        return json_data
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
