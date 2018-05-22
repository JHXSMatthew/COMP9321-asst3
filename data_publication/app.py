from flask import Flask, jsonify
from mongoengine import connect
from flask_pymongo import PyMongo
from collections import OrderedDict

from data_publication.world_bank import create_countries_list

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'comp9321_project'
app.config['MONGO_URI'] = 'mongodb://mcgradyhaha:Mac2813809@ds231360.mlab.com:31360/comp9321_project'

mongo = PyMongo(app)

############################################################### GET METHOD #############################################

@app.route('/data', methods=['GET'])
def get_all_data():
    # Return all countries data in MongoDB database

    counties = mongo.db.country
    output = []
    for country in counties.find():
        output.append({
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


@app.route('/data/population', methods=['GET'])
def get_all_population():
    # Return all population in MongoDB database
    counties = mongo.db.country
    output = []
    for country in counties.find():
        output.append({
            'id': country['_id'],
            'Country': country['Name'],
            'Population': country['Population']
        })
    return jsonify({'result': output})


@app.route('/data/co2', methods=['GET'])
def get_all_co2():
    # Return all CO2 in MongoDB database
    counties = mongo.db.country
    output = []
    for country in counties.find():
        output.append({
            'id': country['_id'],
            'Country': country['Name'],
            'CO2': country['CO2']
        })
    return jsonify({'result': output})


@app.route('/data/ch4', methods=['GET'])
def get_all_ch4():
    # Return all CH4 in MongoDB database
    counties = mongo.db.country
    output = []
    for country in counties.find():
        output.append({
            'id': country['_id'],
            'Country': country['Name'],
            'CH4': country['CH4']

        })
    return jsonify({'result': output})


@app.route('/data/gni', methods=['GET'])
def get_all_gni():
    # Return all population in MongoDB database
    counties = mongo.db.country
    output = []
    for country in counties.find():
        output.append({
            'id': country['_id'],
            'Country': country['Name'],
            'GNI': country['GNI']

        })
    return jsonify({'result': output})


@app.route('/data/gini', methods=['GET'])
def get_all_gini():
    # Return all population in MongoDB database
    counties = mongo.db.country
    output = []
    for country in counties.find():
        output.append({
            'id': country['_id'],
            'Country': country['Name'],
            'GINI': country['GINI']

        })
    return jsonify({'result': output})


@app.route('/data/a_p', methods=['GET'])
def get_all_ap():
    # Return all population in MongoDB database
    counties = mongo.db.country
    output = []
    for country in counties.find():
        output.append({
            'id': country['_id'],
            'Country': country['Name'],
            'Agriculture_Percentage': country['Agriculture_Percentage']
        })
    return jsonify({'result': output})


@app.route('/data/r_p', methods=['GET'])
def get_all_rp():
    # Return all population in MongoDB database
    counties = mongo.db.country
    output = []
    for country in counties.find():
        output.append({
            'id': country['_id'],
            'Country': country['Name'],
            'Renewable_Percentage': country['Renewable_Percentage']

        })
    return jsonify({'result': output})


@app.route('/data/f_f_p', methods=['GET'])
def get_all_ffp():
    # Return all population in MongoDB database
    counties = mongo.db.country
    output = []
    for country in counties.find():
        output.append({
            'id': country['_id'],
            'Country': country['Name'],
            'Fossil_Fuel_Percentage': country['Fossil_Fuel_Percentage']

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