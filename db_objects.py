from mongoengine import connect, Document, StringField, IntField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField


STARTING_YEAR = 1950
ENDING_YEAR = 2016

class Indicator:
    def __init__(self, name, url_name, unit, unit_detail, details):
        self.name = name
        self.url_name = name
        if url_name is not "":
            self.url_name = url_name
        self.unit = unit
        self.unit_detail = unit_detail
        self.details = details

    def to_dict(self):
         return {
            'Display_Name': self.name,
            'Name': self.url_name,
            'Unit': self.unit,
            'Unit_detail': self.unit_detail,
            'Details': self.details
        }

class Indicators:
    Population = Indicator("Population", "", "k", "thousands",
                    "Total population is based on the de facto definition of population, which counts all "
                    "residents regardless of legal status or citizenship. The values shown are midyear estimates."
                    )
    CO2 = Indicator("CO2", "", "kt", "kilotons",
                    "Carbon dioxide emissions are those stemming from the burning of fossil fuels "
                                      "and the manufacture of cement. They include carbon dioxide produced during "
                                      "consumption of solid, liquid, and gas fuels and gas flaring."
                    )
    CH4 = Indicator("CH4", "", "kt", "kilotons of CO2 equivalent",
                    "Methane emissions are those stemming from human activities such as agriculture and from industrial "
                                        "methane production."
                    )
    GNI = Indicator("GNI", "", "USD", "US dollars",
                    "GNI per capita (formerly GNP per capita) is the gross national income, converted "
                                        "to U.S. dollars using the World Bank Atlas method, divided by the midyear population. "
                                        "GNI is the sum of value added by all resident producers plus any product taxes (less "
                                       "subsidies) not included in the valuation of output plus net receipts of primary income "
                                       "(compensation of employees and property income) from abroad. GNI, calculated in national "
                                        "currency, is usually converted to U.S. dollars at official exchange rates for comparisons "
                                        "across economies, although an alternative rate is used when the official exchange rate is "
                                        "judged to diverge by an exceptionally large margin from the rate actually applied in "
                                        "international transactions. To smooth fluctuations in prices and exchange rates, a special "
                                        "Atlas method of conversion is used by the World Bank. This applies a conversion factor that "
                                       "averages the exchange rate for a given year and the two preceding years, adjusted for differences "
                                        "in rates of inflation between the country, and through 2000, the G-5 countries (France, "
                                        "Germany, Japan, the United Kingdom, and the United States). From 2001, these countries "
                                       "include the Euro area, Japan, the United Kingdom, and the United States."
                    )
    GINI = Indicator("GINI", "", "", "",
                     'Gini index measures the extent to which the distribution of income (or, in some cases, '
                     'consumption expenditure) among individuals or households within an economy deviates from a'
                     ' perfectly equal distribution. A Lorenz curve plots the cumulative percentages of total income '
                     'received against the cumulative number of recipients, starting with the poorest individual '
                     'or household. The Gini index measures the area between the Lorenz curve and a hypothetical '
                     'line of absolute equality, expressed as a percentage of the maximum area under the line. Thus'
                     ' a Gini index of 0 represents perfect equality, while an index of 100 implies perfect inequality.'
                     )
    Agriculture_Percentage = Indicator("Agricultural Land", "Agriculture_Percentage", "% of land area", "",
                                       "Agricultural land refers to the share of land area that is arable, under permanent crops, "
                                       "and under permanent pastures. Arable land includes land defined by the FAO as land under "
                                       "temporary crops (double-cropped areas are counted once), temporary meadows for mowing or for "
                                       "pasture, land under market or kitchen gardens, and land temporarily fallow. Land abandoned as "
                                       "a result of shifting cultivation is excluded. Land under permanent crops is land cultivated "
                                       "with crops that occupy the land for long periods and need not be replanted after each harvest, "
                                       "such as cocoa, coffee, and rubber. This category includes land under flowering shrubs, "
                                       "fruit trees, nut trees, and vines, but excludes land under trees grown for wood or timber. "
                                    "Permanent pasture is land used for five or more years for forage, including natural and "
                                    "cultivated crops."
                     )
    Renewable_Percentage = Indicator("Renewable Energy Consumption", "Renewable_Percentage", "% of total final energy consumption", "",
                          "Renewable energy consumption is the share of renewables "
                          "energy in total final energy consumption."
                          )
    Fossil_Fuel_Percentage = Indicator("Fossil Fuel Energy Consumption", "Fossil_Fuel_Percentage", "% of total final energy consumption", "",
                            "Fossil fuel comprises coal, oil, petroleum, and natural gas products."
                            )

    CO4_to_CO2_Ratio = Indicator("CO4 to CO2 Ratio", "CO4_to_CO2_Ratio", "%", "", "Ratio of CO4 to CO2, indicator of "
                                                                                    "agricultural emmisions to other activities")

    CO2_per_KCapita = Indicator("CO2 per Thousand Persons", "CO2_per_KCapita", "kt/Person(k)", "kiloton per thousand persons",
                               "CO2 equivalent emmitted by thousand persons")

    GNI_per_KCapita = Indicator("GNI per Thousand Persons", "GNI_per_KCapita", "USD/Person(k)", "USD per thousand perosns",
                                "Gross Nation Income per thousand persons")




ALL_INDICATORS = ["Population", "CO2", "CH4", "GNI", "GINI", "Agriculture_Percentage",
                  "Renewable_Percentage", "Fossil_Fuel_Percentage", "CO4_to_CO2_Ratio", "CO2_per_KCapita",
                  "GNI_per_KCapita"]


class Year(EmbeddedDocument):
    Year = IntField(required=True, primary_key=True)
    Value = FloatField()

    def __init__(self, *args, **kwargs):
        super(Year, self).__init__(*args, **kwargs)

    def to_dict(self):
        return {'year': self.Year,
                'value': self.Value}

class Country(Document):
    """
    CH4 - methane
    GNI - gross national income
    GINI - gini index
    Agriculture_Percentage - percentage of land for agriculture
    """
    id = IntField(required=True, primary_key=True)
    Name = StringField(required=True, max_length=50)
    Population = ListField(EmbeddedDocumentField(Year))
    CO2 = ListField(EmbeddedDocumentField(Year))
    CH4 = ListField(EmbeddedDocumentField(Year))
    CH4_CO2 = ListField(EmbeddedDocumentField(Year))
    GNI = ListField(EmbeddedDocumentField(Year))
    GINI = ListField(EmbeddedDocumentField(Year))
    Agriculture_Percentage = ListField(EmbeddedDocumentField(Year))
    Renewable_Percentage = ListField(EmbeddedDocumentField(Year))
    Fossil_Fuel_Percentage = ListField(EmbeddedDocumentField(Year))
    CO4_to_CO2_Ratio = ListField(EmbeddedDocumentField(Year))
    CO2_per_KCapita = ListField(EmbeddedDocumentField(Year))
    GNI_per_KCapita = ListField(EmbeddedDocumentField(Year))

    def __init__(self, *args, **kwargs):
        super(Country, self).__init__(*args, **kwargs)

    def to_dict(self, indicators, start_year, end_year):
        global ALL_INDICATORS
        r = {
            'Name': self.Name
        }

        if indicators and len(indicators) > 0:
            for i in indicators:
                ##########if i == CO4 to co2 ratio etc:

                r[i] = [yr.to_dict() for yr in getattr(self, i) if start_year <= yr.Year <= end_year]
        else:
            for i in ALL_INDICATORS:
                r[i] = [yr.to_dict() for yr in getattr(self, i) if start_year <= yr.Year <= end_year]

        return r
    
    def get_values_list(self, indicator, start_year, end_year):
        '''
        year = end_year - index
        list is in reverse order (from end year to start year)
        :param indicator:
        :param start_year:
        :param end_year:
        :return:
        '''
        data = []
        if getattr(self, indicator) == []:
            data = [-1] * (end_year-start_year)
        else:
            [data.append(yr.Value) for yr in getattr(self, indicator) if start_year <= yr.Year <= end_year]
        output = {'start_year': start_year, 'end_year': end_year, 'data': data}

        return output



