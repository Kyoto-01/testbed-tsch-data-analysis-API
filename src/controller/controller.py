from lib.testbed_analysis.database import InfluxDBConnection
from lib.testbed_analysis import TestbedData
from lib.testbed_analysis import TestbedGeneralReport
from utils.constants import DATABASE_CONFIG_FILE_PATH


ERR_400_MSG = ('Bad request.', 400)
ERR_404_MSG = ('Resource not found.', 404)


class Controller:

    def __init__(
        self,
        request: 'dict'
    ):
        self._request: 'dict' = request
        self._testbed: 'TestbedData' = None
        self._generalReport: 'TestbedGeneralReport' = None
        self._testbedList: 'list' = None
        self._response: 'dict' = None
        self._setup = self._setup_controller()

    def _setup_controller(self):
        ret = True

        try:
            database = InfluxDBConnection(DATABASE_CONFIG_FILE_PATH)

            self._testbed = TestbedData(
                name=self._request['testbed_name'],
                database=database
            )

            self._generalReport = TestbedGeneralReport(self._testbed)
            self._testbedList = self._generalReport._get_testbed_testbed()
        except KeyError as ke:
            ret = False

        return ret

    def _check_req_parameters_key(self) -> 'bool':
        res = True

        try:
            __ = self._request['testbed_name']

        except KeyError as ke:
            res = False

        return res

    def _check_req_parameters_value_type(self) -> 'bool':
        res = isinstance(self._request['testbed_name'], str)

        return res
    
    def _check_req_parameters_value(self) -> 'bool':
        res = self._testbed.name in self._testbedList

        return res

    def _check_req_parameters_errors(self) -> 'tuple':
        res = None

        if (
            not self._setup or
            not self._check_req_parameters_key() or
            not self._check_req_parameters_value_type()
        ):
            res = ERR_400_MSG
        elif not self._check_req_parameters_value():
            res = ERR_404_MSG

        return res
    
    def _check_response(self) -> 'bool':
        res = bool(self._response)

        return res
