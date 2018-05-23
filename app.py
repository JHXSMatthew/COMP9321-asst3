from flask import Flask, jsonify, request
from mongoengine import connect
import db_objects
from collections import OrderedDict
import requests

from world_bank import create_countries_list

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'comp9321_project'
app.config['MONGO_URI'] = 'mongodb://mcgradyhaha:Mac2813809@ds231360.mlab.com:31360/comp9321_project'


############################################################### GET METHOD #############################################


@app.route('/api/<string:country>', methods=['GET'])
def get_indicator(country):
    connect(
        host='mongodb://mcgradyhaha:Mac2813809@ds231360.mlab.com:31360/comp9321_project'
    )

    c = db_objects.Country.objects(Name=country)[0]

    start_year = db_objects.STARTING_YEAR
    end_year = db_objects.ENDING_YEAR
    indicators = []

    if 'year' in request.args:
        start_year = int(request.args.get('year'))
        end_year = int(request.args.get('year'))
    elif 'start_year' in request.args and 'end_year' in request.args:
        start_year = int(request.args.get('start_year'))
        end_year = int(request.args.get('end_year'))

    if 'indicator' in request.args:
        indicators = request.args.getlist('indicator')

    return jsonify({
        'result': c.to_dict(indicators, start_year, end_year)})

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/all', methods=['GET'])
def get_all_data():
    # Return all countries data in MongoDB database
    connect(
        host='mongodb://mcgradyhaha:Mac2813809@ds231360.mlab.com:31360/comp9321_project'
    )

    output = []
    for country in db_objects.Country.objects:
        output.append({
            'Name': country['Name'],
            'Population': country['Population'],
            'CO2': country['CO2'],
            'CH4': country['CH4'],
            'GNI': country['GNI'],
            'GINI': country['GINI'],
            'Agriculture_Percentage': country['Agriculture_Percentage'],
            'Renewable_Percentage': country['Renewable_Percentage'],
            'Fossil_Fuel_Percentage': country['Fossil_Fuel_Percentage']
        })
    return jsonify({'result': output})


@app.route('/data/<country>', methods=['GET'])
def get_one_data(country):
    # Return a specific country data in MongoDB database
    countries = mongo.db.country

    country = countries.find_one({'Name': country})

    if country:
        output = {
            'id': country['_id'],
            'Country': country['Name'],
            'Population': country['Population'],
            'CO2': country['CO2'],
            'CH4': country['CH4'],
            'GNI': country['GNI'],
            'GINI': country['GINI'],
            'Agriculture_Percentage': country['Agriculture_Percentage'],
            'Renewable_Percentage': country['Renewable_Percentage'],
            'Fossil_Fuel_Percentage': country['Fossil_Fuel_Percentage']
        }
    else:
        output = 'No results found!'
    return jsonify(output)


@app.route('/data/countries', methods=['GET'])
def get_all_countries():
    # Return all countries in MongoDB database
    counties = mongo.db.country
    output = []
    for country in counties.find():
        output.append({
            'id': country['_id'],
            'Country': country['Name'],
        })
    return jsonify({'result': output})


############################################################### POST METHOD ############################################

@app.route('/data', methods=['POST'])
def download_data():
    # Get world bank data
    countries = create_countries_list()



    # Get NASA data

    # Add to mongoDB database
    connect(
        host='mongodb://mcgradyhaha:Mac2813809@ds231360.mlab.com:31360/comp9321_project'
    )
    for country in countries:
        country.save()
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
