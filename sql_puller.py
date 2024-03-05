import mysql.connector

import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
print("Loading SQL Static Data Pull Package")
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