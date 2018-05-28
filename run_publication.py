from flask import Flask, jsonify, request
from mongoengine import connect
import db_objects
import numpy as np
import five_number_summary
import ranking
from collections import OrderedDict
import requests
from flask_cors import CORS

from world_bank import create_countries_list

CONNECTION_STRING = 'mongodb://mcgradyhaha:Mac2813809@ds231360.mlab.com:31360/comp9321_project'
#CONNECTION_STRING = 'mongodb://127.0.0.1:27017/test'

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'comp9321_project'
app.config['MONGO_URI'] = CONNECTION_STRING
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

PUBLICATION_URL = "https://127.0.0.1"
PUBLICATION_PORT = 9998


connect(
        host=CONNECTION_STRING
)

cache_analysis = None
############################################################### GET METHOD #############################################
@app.route('/analysis', methods=['GET'])
def get_analysis():
    global cache_analysis
    if 'year' in request.args:
        start_year = end_year = int(request.args.get('year'))
    elif 'start_year' in request.args and 'end_year' in request.args:
        start_year = int(request.args.get('start_year'))
        end_year = int(request.args.get('end_year'))
    else:
        start_year = db_objects.STARTING_YEAR
        end_year = db_objects.ENDING_YEAR
        
    if not cache_analysis:
        if 'indicator' in request.args:
            indicators = request.args.getlist('indicator')

            r = get_summary(start_year, end_year, indicators)
        else:
            r = get_summary(start_year, end_year, db_objects.ALL_INDICATORS)
        cache_analysis = jsonify({'result': r})
    return cache_analysis


def get_summary(start_year, end_year, indicators):
    result = []
    for indicator in indicators:
        year_values = [country.to_dict([indicator], start_year, end_year)#[indicator]
                       for country in db_objects.Country.objects]

        year_values = [[tuple([v['year'], v['value'], c['Name']]) for v in c[indicator]] for c in year_values if c[indicator] != []]
        print(year_values)

        results = {'indicator': indicator,
                   'summary': []}

        for years in list(zip(*year_values)):
            year = years[0][0]
            values = list(filter(lambda x: x != -1, [y[1] for y in years]))
            country_count = len(values)
            if len(values) == 0:
                values = [-1]
            #print(values, year)
            values_sum = sum(values)
            values.sort()

            min_value = values[0]
            max_value = values[-1]
            q1 = np.percentile(values, 25)
            q3 = np.percentile(values, 75)
            median_value = np.percentile(values, 50)
            average = 0
            try:
                average = values_sum/country_count
            except:
                pass
            results['summary'].append({'year': year, 'min': min_value, 'q1': q1, 'median': median_value, 'q3': q3,
                                       'max': max_value, 'sum': values_sum, 'average': average})

        result.append(results)
    return result

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
                'Country': country['Name']
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


cache_all_country = None
@app.route('/api/all', methods=['GET'])
def get_all_data():
    global cache_all_country
    # Return all countries data in MongoDB database
    # connect(
    #     host=CONNECTION_STRING
    # )

    if not cache_all_country:
        output = []
        for country in db_objects.Country.objects:
            output.append(country.to_dict([],db_objects.STARTING_YEAR,db_objects.ENDING_YEAR))
        cache_all_country = jsonify({'result': output})
    return cache_all_country



# @app.route('/analysis/<indicator>', methods=['GET'])
# def get_summary_for_indicator(indicator):
#     if 'year' in request.args:
#         year = int(request.args.get('year'))
#     else:
#         return jsonify({'Error' : 'Add year value as request argument'}), 400
#
#     output = five_number_summary.get_five_num_sum(indicator, year)
#
#     return jsonify(output), 200
#
#
# @app.route('/analysis/<country>/<indicator>', methods=['GET'])
# def get_country_analysis(country, indicator):
#     if 'year' in request.args:
#         year = int(request.args.get('year'))
#     else:
#         return jsonify({'Error' : 'Add year value as request argument'}), 400
#
#     indicator_summary = five_number_summary.get_five_num_sum(indicator, year)
#
#     connect(
#         host='mongodb://mcgradyhaha:Mac2813809@ds231360.mlab.com:31360/comp9321_project'
#     )
#
#     c = db_objects.Country.objects(Name=country)[0]
#     values_list = c.get_values_list(indicator, db_objects.STARTING_YEAR, db_objects.ENDING_YEAR)
#
#     year_index = five_number_summary.get_index(year)
#     value = values_list['data'][year_index]
#
#     percent_of_total = (value/indicator_summary['sum']) * 100
#
#     return jsonify({'Indicator': indicator, 'Year': year, 'percent_of_total':percent_of_total}), 200


@app.route('/analysis/ranking', methods=['GET'])
def get_ranking_by_year():
   if 'year' in request.args:
       year = int(request.args.get('year'))
   else:
       return jsonify({'Error' : 'Add year value as request argument'}), 400

   output = ranking.get_ranking(year)
   return jsonify(output), 200


@app.route('/api/indicator', methods=['GET'])
def get_indicator_list():
    return jsonify({'result': [getattr(db_objects.Indicators, indicator).to_dict() for indicator in db_objects.ALL_INDICATORS]})

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
