import db_objects
from mongoengine import connect

def get_index(year):
   index = db_objects.ENDING_YEAR - year
   return index


def get_ranking(indicator, year):
   connect(
       host='mongodb://mcgradyhaha:Mac2813809@ds231360.mlab.com:31360/comp9321_project'
   )

   ranking = {}
   for country in db_objects.Country.objects:
       value_list = country.get_values_list(indicator, db_objects.STARTING_YEAR, db_objects.ENDING_YEAR)['data']
       value = value_list[get_index(year)]
       ranking[country['Name']] = value

   sort = sorted(ranking.items(), key = lambda x : x[1], reverse=True)
   print(sort)
   output = dict()
   for i in range(len(sort)):
       output[sort[i][0]] = {(i+1) : sort[i][1]}
   return output