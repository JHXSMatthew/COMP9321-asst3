from mongoengine import connect, Document, StringField, IntField, FloatField, ListField

connect(
    host='mongodb://bobsemple:bobsempleis0P@ds233208.mlab.com:33208/world-bank'
)

STARTING_YEAR = 1950
ENDING_YEAR = 2015


class Country(Document):
    """
    CH4 - methane
    GNI - gross national income
    GINI - gini index
    Agriculture_Percentage - percentage of land for agriculture
    """
    Name = StringField(required=True, max_length=50)
    Population = ListField(FloatField())
    CO2 = ListField(FloatField())
    CH4 = ListField(FloatField())
    GNI = ListField(FloatField())
    GINI = ListField(FloatField())
    Agriculture_Percentage = ListField(FloatField())
    Renewable_Percentage = ListField(FloatField())
    Fossil_Fuel_Percentage = ListField(FloatField())

    def __init__(self, name, population, co2, ch4, gni, gini, agri_p, renewable_p, fossil_p, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Name = name
        self.Population = population
        self.CO2 = co2
        self.CH4 = ch4
        self.GNI = gni
        self.GINI = gini
        self.Agriculture_Percentage = agri_p
        self.Renewable_Percentage = renewable_p
        self.Fossil_Fuel_Percentage = fossil_p

