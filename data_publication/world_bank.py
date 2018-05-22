import requests
from data_publication.db_objects import Country, Year


def create_country_objects():
    '''
    Populates the countries list with country objects including their name
    :return:
    '''

    countries = []
    general_info_url = 'http://api.worldbank.org/v2/countries?format=json&per_page=500'

    response = requests.get(general_info_url, params=None)
    response_list = response.json()[1]

    country_id = 1

    for country in response_list:
        if country['region']['id'] != 'NA':
            # region = country['region']['value']
            # capital_city = country['capitalCity']
            country = Country(Name=country['name'], id=country_id)
            country_id += 1
            countries.append(country)

    return countries


# Generic parsing for values
def get_indicator_values(indicator, object_value, countries):
    '''
    Connect to Worldbank REST API and parsing response for values
    :param indicator: World Bank API Indicator value
    :param object_value: MongoDB Object value to be added
    :return:
    '''

    api_url = 'http://api.worldbank.org/v2/countries/all/indicators/'
    url = api_url+indicator+'?format=json&date=1950:2016&per_page=20000'

    response = requests.get(url, params=None)
    response_list = response.json()[1]

    for country in response_list:
        if country['countryiso3code'] is not "":

            name = country['country']['value']
            year = int(country['date'])
            value = country['value']

            if value is None:
                value = -1
            # Check if country object exists

            for country_object in countries:

                if country_object.Name == name:
                    year_object = Year(year, value)
                    country_object[object_value].append(year_object)
                    break
    return countries


def create_countries_list():
    '''

    :return:
    '''
    indicator_values = [['NY.GNP.PCAP.CD', 'GNI'], ['SI.POV.GINI', 'GINI'], ['EN.ATM.METH.KT.CE', 'CH4'],
                        ['EN.ATM.CO2E.KT', 'CO2'], ['AG.LND.AGRI.ZS', 'Agriculture_Percentage'],
                        ['EG.FEC.RNEW.ZS', 'Renewable_Percentage'], ['SP.POP.TOTL', 'Population'],
                        ['EG.USE.COMM.FO.ZS', 'Fossil_Fuel_Percentage']]

    countries = create_country_objects()

    for indicator in indicator_values:
        countries = get_indicator_values(indicator[0], indicator[1], countries)

    return countries
