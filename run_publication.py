from flask import Flask, jsonify, request
from mongoengine import connect
import db_objects
from collections import OrderedDict
import requests

from world_bank import create_countries_list

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'comp9321_project'
app.config['MONGO_URI'] = 'mongodb://mcgradyhaha:Mac2813809@ds231360.mlab.com:31360/comp9321_project'

PUBLICATION_URL = "https://127.0.0.1"
PUBLICATION_PORT = 9998



############################################################ Indicator Info ############################################


co2 = {
    'Unit': 'kt',
    'Source': ' Carbon Dioxide Information Analysis Center, Environmental Sciences Division, '
              'Oak Ridge National Laboratory, Tennessee, United States.',
    'Definition': 'Carbon dioxide emissions are those stemming from the burning of fossil fuels '
                  'and the manufacture of cement. They include carbon dioxide produced during '
                  'consumption of solid, liquid, and gas fuels and gas flaring.'

}

gni = {
    'Unit': 'current US$',
    'Source': 'World Bank national accounts data, and OECD National Accounts data files.',
    'Definition': 'GNI per capita (formerly GNP per capita) is the gross national income, converted'
                  ' to U.S. dollars using the World Bank Atlas method, divided by the midyear population.'
                  ' GNI is the sum of value added by all resident producers plus any product taxes (less '
                  'subsidies) not included in the valuation of output plus net receipts of primary income '
                  '(compensation of employees and property income) from abroad. GNI, calculated in national'
                  ' currency, is usually converted to U.S. dollars at official exchange rates for comparisons'
                  ' across economies, although an alternative rate is used when the official exchange rate is'
                  ' judged to diverge by an exceptionally large margin from the rate actually applied in'
                  ' international transactions. To smooth fluctuations in prices and exchange rates, a special'
                  ' Atlas method of conversion is used by the World Bank. This applies a conversion factor that '
                  'averages the exchange rate for a given year and the two preceding years, adjusted for differences'
                  ' in rates of inflation between the country, and through 2000, the G-5 countries (France,'
                  ' Germany, Japan, the United Kingdom, and the United States). From 2001, these countries '
                  'include the Euro area, Japan, the United Kingdom, and the United States.',
}

gini = {
    'Unit': '%',
    'Source': 'World Bank, Development Research Group. Data are based on primary household survey data obtained '
              'from government statistical agencies and World Bank country departments.',
    'Definition': 'Gini index measures the extent to which the distribution of income (or, in some cases, '
                  'consumption expenditure) among individuals or households within an economy deviates from a'
                  ' perfectly equal distribution. A Lorenz curve plots the cumulative percentages of total income '
                  'received against the cumulative number of recipients, starting with the poorest individual '
                  'or household. The Gini index measures the area between the Lorenz curve and a hypothetical '
                  'line of absolute equality, expressed as a percentage of the maximum area under the line. Thus'
                  ' a Gini index of 0 represents perfect equality, while an index of 100 implies perfect inequality.'
}

ch4 = {
    'Unit': 'kt',
    'Source': 'European Commission, Joint Research Centre ( JRC )/Netherlands Environmental Assessment Agency '
              '( PBL ). Emission Database for Global Atmospheric Research ( EDGAR )',
    'Definition': 'Methane emissions are those stemming from human activities such as agriculture and from industrial '
                 'methane production.'
}

a_p = {
    'Unit': '% of land area',
    'Source': 'Food and Agriculture Organization, electronic files and web site',
    'Definition': 'Agricultural land refers to the share of land area that is arable, under permanent crops, '
                  'and under permanent pastures. Arable land includes land defined by the FAO as land under '
                  'temporary crops (double-cropped areas are counted once), temporary meadows for mowing or for '
                  'pasture, land under market or kitchen gardens, and land temporarily fallow. Land abandoned as'
                  ' a result of shifting cultivation is excluded. Land under permanent crops is land cultivated '
                  'with crops that occupy the land for long periods and need not be replanted after each harvest,'
                  ' such as cocoa, coffee, and rubber. This category includes land under flowering shrubs, '
                  'fruit trees, nut trees, and vines, but excludes land under trees grown for wood or timber. '
                  'Permanent pasture is land used for five or more years for forage, including natural and '
                  'cultivated crops.'
}

r_p = {
    'Unit': '% of total final energy consumption',
    'Souece': ' World Bank, Sustainable Energy for All ( SE4ALL ) database from the SE4ALL Global Tracking '
              'Framework led jointly by the World Bank, International Energy Agency, and the Energy Sector '
              'Management Assistance Program.',
    'Definition': 'Renewable energy consumption is the share of renewables energy in total final energy consumption.'
}

population ={
    'Unit': 'Total',
    'Source': '( 1 ) United Nations Population Division. World Population Prospects: 2017 Revision. '
              '( 2 ) Census reports and other statistical publications from national statistical offices, '
              '( 3 ) Eurostat: Demographic Statistics, '
              '( 4 ) United Nations Statistical Division. Population and Vital Statistics Reprot ( various years ), '
              '( 5 ) U.S. Census Bureau: International Database, and '
              '( 6 ) Secretariat of the Pacific Community: Statistics and Demography Programme.',
    'Definition': 'Total population is based on the de facto definition of population, which counts all '
                  'residents regardless of legal status or citizenship. The values shown are midyear estimates.'
}

f_f_p = {
    'Unit': '% of total',
    'Source': 'IEA Statistics ',
    'Definition': 'Fossil fuel comprises coal, oil, petroleum, and natural gas products.'
}





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


@app.route('/data/details/<indicator>', methods=['GET'])
def get_indicator_details(indicator):
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
    app.run(debug=True,port=PUBLICATION_PORT)
