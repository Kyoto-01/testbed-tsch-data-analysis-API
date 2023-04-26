from ..database import InfluxDBConnection


class TestbedData:

    def __init__(
        self,
        name: 'str',
        database: 'InfluxDBConnection'
    ):
        self._name = name
        self._database = database

    @property
    def name(self):
        return self._name

    @property
    def database(self):
        return self._database
