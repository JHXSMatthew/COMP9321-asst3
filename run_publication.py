from flask import Flask, jsonify, request
from mongoengine import connect
import db_objects
import numpy as np
from collections import OrderedDict
import requests
from flask_cors import CORS

from world_bank import create_countries_list

CONNECTION_STRING = 'mongodb://mcgradyhaha:Mac2813809@ds231360.mlab.com:31360/comp9321_project'
# CONNECTION_STRING = 'mongodb://127.0.0.1:27017/test'

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'comp9321_project'
app.config['MONGO_URI'] = CONNECTION_STRING
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

PUBLICATION_URL = "https://127.0.0.1"
PUBLICATION_PORT = 9998


############################################################ Indicator Info ############################################
a_p = {
    'Unit': '% of land area',
    'Source': 'Food and Agriculture Organization, electronic files and web site',
    'Definition':
}

r_p = {
    'Unit': '% of total final energy consumption',
    'Souece': ' World Bank, Sustainable Energy for All ( SE4ALL ) database from the SE4ALL Global Tracking '
              'Framework led jointly by the World Bank, International Energy Agency, and the Energy Sector '
              'Management Assistance Program.',
    'Definition':
}

population ={
    'Unit': 'Total',
    'Source': '( 1 ) United Nations Population Division. World Population Prospects: 2017 Revision. '
              '( 2 ) Census reports and other statistical publications from national statistical offices, '
              '( 3 ) Eurostat: Demographic Statistics, '
              '( 4 ) United Nations Statistical Division. Population and Vital Statistics Reprot ( various years ), '
              '( 5 ) U.S. Census Bureau: International Database, and '
              '( 6 ) Secretariat of the Pacific Community: Statistics and Demography Programme.',
    'Definition':
}

f_f_p = {
    'Unit': '% of total',
    'Source': 'IEA Statistics ',
    'Definition':
}



connect(
        host=CONNECTION_STRING
)

############################################################### GET METHOD #############################################
@app.route('/analysis', methods=['GET'])
def get_analysis():
    #c = db_objects.Country.objects(Name=country)[0]

    if 'year' in request.args:
        start_year = end_year = int(request.args.get('year'))
    elif 'start_year' in request.args and 'end_year' in request.args:
        start_year = int(request.args.get('start_year'))
        end_year = int(request.args.get('end_year'))
    if 'indicator' in request.args:
        indicators = request.args.getlist('indicator')

        get_sum(indicators)

    # return jsonify({
    #     'result': c.to_dict(indicators, start_year, end_year)})


def get_sum(indicators):
    #print(db_objects.Country.objects(Name="Taiwan, China")[0].Population == [])

    year_values = [[(v.Year, v.Value, country.Name) for v in country.Population] for country in db_objects.Country.objects if country.Population != []]
    results = []

    for years in list(zip(*year_values)):
        year = years[0][0]
        values = [y[1] for y in years]
        print(values)
        values_sum = sum(values)
        values.sort()
        min_value = values[0]
        max_value = values[len(values) - 1]
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        median_value = np.percentile(values, 50)
        results.append({'year': year, 'min': min_value, 'q1': q1, 'median': median_value, 'q3': q3, 'max': max_value})

    print (results)

cache_country_list = None
@app.route('/api/countries', methods=['GET'])	
def get_all_countries():
    # Return all countries in MongoDB database
    global cache_country_list
    
    if not cache_country_list:
        output = []	
        for country in db_objects.Country.objects:	
            output.append({	
                'id': country['id'],	
                'Country': country['Name'],	
            })	
        cache_country_list = jsonify({'result': output})
    return cache_country_list
	


@app.route('/api/<string:country>', methods=['GET'])
def get_indicator(country):
    # connect(
    #     host=CONNECTION_STRING
    # )

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


@app.route('/api/all', methods=['GET'])
def get_all_data():
    # Return all countries data in MongoDB database
    # connect(
    #     host=CONNECTION_STRING
    # )

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

@app.route('/api/details', methods=['GET'])
def get_indicator_details():
    output = []

    output.append({
        'unit': eval(indicator)['Unit'],
        'source': eval(indicator)['Source'],
        'definition': eval(indicator)['Definition']

    })
    return jsonify({'result': output})



############################################################### POST METHOD ############################################

@app.route('/data', methods=['POST'])
def download_data():
    # Get world bank data
    print('on post - create country data')
    countries = create_countries_list()



    # Get NASA data

    # Add to mongoDB database
    # connect(
    #     host=CONNECTION_STRING
    # )
    for country in countries:
        country.save()
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True,port=PUBLICATION_PORT)
