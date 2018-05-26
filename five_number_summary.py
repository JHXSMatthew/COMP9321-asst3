import db_objects
from mongoengine import connect
import np
import statistics

def get_index(year):
    index = db_objects.ENDING_YEAR - year
    return index

def get_five_num_sum(indicator, year):

    connect(
        host='mongodb://mcgradyhaha:Mac2813809@ds231360.mlab.com:31360/comp9321_project'
    )

    values = []

    for country in db_objects.Country.objects:
        value_list = country.get_values_list(indicator, db_objects.STARTING_YEAR, db_objects.ENDING_YEAR)['data']
        value = value_list[get_index(year)]
        if value is not -1:
            values.append(value)

    values_sum = sum(values)
    values.sort()
    min_value = values[0]
    max_value = values[len(values)-1]
    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)
    median_value = np.percentile(values, 50)
    num_sum = {'min': min_value, 'q1': q1, 'median': median_value, 'q3': q3, 'max': max_value}



    return num_sum


