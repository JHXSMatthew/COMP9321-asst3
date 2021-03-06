import db_objects
from mongoengine import connect


ALL_INDICATORS = ["Population", "CO2", "CH4", "GNI", "GINI", "Agriculture_Percentage",
                   "Renewable_Percentage", "Fossil_Fuel_Percentage"]

cache_rank = {}
def get_ranking(year):
  global cache_rank
  if year not in cache_rank:
    cty = db_objects.Country.objects
    for i in cty:
      pass
    ranking = dict()
    for indicator in ALL_INDICATORS:
        temp =dict()
        for country in cty:
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
    cache_rank[year] = ranking
  return cache_rank[year]


cache_overall_rank = {}
def get_overall_ranking(year):
   global cache_overall_rank
   if year not in cache_overall_rank:
    cty = db_objects.Country.objects
    for i in cty:
        pass
    ranking = dict()
    for indicator in ALL_INDICATORS:
        temp = dict()
        for country in cty:
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
            rank[sort[i][0]] = [i+1]
        for key in rank:
            if key not in ranking:
                ranking[key] = rank[key]
            else:
                ranking[key] += rank[key]

    for country in ranking.keys():
        i = sum(ranking[country]) / len(ranking[country])
        ranking[country] = i
    sort = sorted(ranking.items(), key=lambda x: x[1])
    all_ranking=dict()
    for i in range(len(sort)):
        all_ranking[sort[i][0]] = i + 1
    cache_overall_rank[year] = all_ranking

   return cache_overall_rank[year]


def deepSearch(dict1, dict2):
  for key in dict2.keys():
      if key not in dict1.keys():
          dict1[key] = dict2[key]
      else:
          deepSearch(dict1[key], dict2[key])
