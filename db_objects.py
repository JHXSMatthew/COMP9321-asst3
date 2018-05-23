from mongoengine import connect, Document, StringField, IntField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField


STARTING_YEAR = 1950
ENDING_YEAR = 2015

class Indicator:
    def __init__(self, name, url_name, unit, unit_detail):
        self.name = name
        self.url_name = name
        if url_name is not "":
            self.url_name = url_name
        self.unit = unit
        self.unit_detail = unit_detail

class Indicators:
    POP = Indicator("Population", "", "k", "thousands")
    CO2 = Indicator("CO2", "", "kt", "kilotons")
    CH4 = Indicator("CH4", "", "kt", "kilotons of CO2 equivalent")
    GNI = Indicator("GNI", "", "USD", "US dollars")
    GINI = Indicator("GINI", "", "NA", "NA")
    AGRI = Indicator("Agricultural Land", "Agriculture_Percentage", "% of land area", "NA")
    RENEWABLE = Indicator("Renewable Energy Consumption", "Renewable_Percentage", "% of total final energy consumption", "NA")
    FOSSIL_FUEL = Indicator("Fossil Fuel Energy Consumption", "Fossil_Fuel_Percentage", "% of total final energy consumption", "NA")


ALL_INDICATORS = ["Population", "CO2", "CH4", "GNI", "GINI", "Agriculture_Percentage",
                  "Renewable_Percentage", "Fossil_Fuel_Percentage"]


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
    #id = IntField(required=True, primary_key=True)
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

    def __init__(self, *args, **kwargs):
        super(Country, self).__init__(*args, **kwargs)

    def to_dict(self, indicators, start_year, end_year):
        r = {
            'Name': self.Name
        }

        if indicators is not []:
            for i in indicators:
                r[i] = [yr.to_dict() for yr in getattr(self, i) if start_year <= yr.Year <= end_year]
        else:
            for i in ALL_INDICATORS:
                r[i] = [yr.to_dict() for yr in getattr(self, i) if start_year <= yr.Year <= end_year]

        return r



