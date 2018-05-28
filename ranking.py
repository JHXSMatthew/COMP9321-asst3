import db_objects
from mongoengine import connect




def get_ranking(year):
  connect(
      host='mongodb://mcgradyhaha:Mac2813809@ds231360.mlab.com:31360/comp9321_project'
  )

  ALL_INDICATORS = ["Population", "CO2", "CH4", "GNI", "GINI", "Agriculture_Percentage",
                    "Renewable_Percentage", "Fossil_Fuel_Percentage"]

  ranking = dict()
  for indicator in ALL_INDICATORS:
      temp =dict()
      for country in db_objects.Country.objects:
          value_list = country.get_values_list(indicator, year, year)['data']
          value = 0
          if len(value_list) == 1:
              value = value_list[0]
          if int(value) < 0:
              continue
          temp[country['Name']] = value

      sort = sorted(temp.items(), key=lambda x: x[1], reverse=True)
      rank = dict()
      for i in range(len(sort)):
          rank[sort[i][0]] = {indicator : i+1}
      deepSearch(ranking, rank)

  return ranking

def deepSearch(dict1, dict2):
   for key in dict2.keys():
       if key not in dict1.keys():
           dict1[key] = dict2[key]
       else:
           deepSearch(dict1[key], dict2[key])

