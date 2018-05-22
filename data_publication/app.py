from flask import Flask, jsonify
from mongoengine import connect
from flask_pymongo import PyMongo

from data_publication.world_bank import create_countries_list

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'world-bank'
app.config['MONGO_URI'] = 'mongodb://bobsemple:bobsempleis0P@ds233208.mlab.com:33208/world-bank'

mongo = PyMongo(app)


@app.route('/countrylist', methods=['POST'])
def download_data():
    # Get world bank data
    countries = create_countries_list()

    # Get NASA data

    # Add to mongoDB database
    connect(
        host='mongodb://bobsemple:bobsempleis0P@ds233208.mlab.com:33208/world-bank'
    )
    for country in countries:
        country.save()
    return 'Hello World!'


@app.route('/countrylist', methods=['GET'])
def return_all_data():
    # Return all data in MongoDB database
    counties = mongo.db.collection_name
    output = []
    for q in counties.find():
        output.append({'name': q.Name})
    return jsonify(output)


@app.route('/countrylist', methods=['GET'])
def return_country_data():
    # Return data in MongoDB database for specific country

    return 'Hello World'


@app.route('/countrylist/<country>', methods=['GET'])
def return_one_country(country):
    countries = mongo.db.collection_name
    q = countries.find_one({'country': country})

    if q:
        output = {}
    else:
        output ='No results found'
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)