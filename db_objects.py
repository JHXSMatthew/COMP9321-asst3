from mongoengine import connect, Document, StringField, IntField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField


STARTING_YEAR = 1950
ENDING_YEAR = 2015

class Year(EmbeddedDocument):
    Year = IntField(required=True, primary_key=True)
    Value = FloatField()

    def __init__(self, year, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Year = year
        self.Value = value

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

    def __init__(self, *args, **kwargs):
        super(Country, self).__init__(*args, **kwargs)

        # self.Name = name
        # self.Population = population
        # self.CO2 = co2
        # self.CH4 = ch4
        # self.GNI = gni
        # self.GINI = gini
        # self.Agriculture_Percentage = agri_p
        # self.Renewable_Percentage = renewable_p
        # self.Fossil_Fuel_Percentage = fossil_p


