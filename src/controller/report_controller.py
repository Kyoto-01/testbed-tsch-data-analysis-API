from lib.testbed_analysis.database import InfluxDBConnection
from lib.testbed_analysis import TestbedData
from lib.testbed_analysis import TestbedClientsReport
from lib.testbed_analysis import TestbedServersReport
from lib.testbed_analysis import TestbedGeneralReport
from lib.testbed_analysis.data_report import TestbedMotesReport
from utils.constants import DATABASE_CONFIG_FILE_PATH


ERR_400_MSG = ('Bad request.', 400)
ERR_404_MSG = ('Resource not found.', 404)


class ReportController:

    def __init__(
        self,
        request: 'dict'
    ):
        self._request: 'dict' = request
        self._testbed: 'TestbedData' = None
        self._generalReport: 'TestbedGeneralReport' = None
        self._testbedList: 'list' = None
        self._report: 'TestbedMotesReport' = None
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
            __ = self._request['topics']
            __ = self._request['mote_addr']

        except KeyError as ke:
            res = False

        return res

    def _check_req_parameters_value_type(self) -> 'bool':
        res = isinstance(self._request['testbed_name'], str)
        res = res and isinstance(self._request['topics'], list)
        res = res and isinstance(self._request['mote_addr'], str)

        return res

    def _check_req_parameters_value(self) -> 'bool':
        res = self._testbed.name in self._testbedList

        return res

    def _check_response(self) -> 'bool':
        res = bool(self._response)

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

    def get_report(self) -> 'dict':
        self._response = self._check_req_parameters_errors()

        if not self._response:
            self._response = self._report.get_report_by_topics(
                self._request['mote_addr'],
                self._request['topics']
            )

            if not self._check_response():
                self._response = ERR_404_MSG

        return self._response


class ReportGeneralController(ReportController):

    def __init__(
        self,
        request: 'dict'
    ):
        super().__init__(request)

    def _setup_controller(self):
        self._request['mote_addr'] = ''

        ret = super()._setup_controller()

        if ret:
            self._report = self._generalReport

        return ret


class ReportMoteController(ReportController):

    def __init__(
        self,
        request: 'dict'
    ):
        self._moteList = None

        super().__init__(request)

    def _check_req_parameters_value(self) -> 'bool':
        res = super()._check_req_parameters_value()
        res = res and self._request['mote_addr'] in self._moteList

        return res


class ReportClientController(ReportMoteController):

    def __init__(
        self,
        request: 'dict'
    ):
        super().__init__(request)

    def _setup_controller(self):
        ret = super()._setup_controller()

        if ret:
            self._report = TestbedClientsReport(self._testbed)
            if self._testbed.name in self._testbedList:
                self._moteList = self._generalReport._get_testbed_client()
            else:
                self._moteList = []

        return ret


class ReportServerController(ReportMoteController):

    def __init__(
        self,
        request: 'dict'
    ):
        super().__init__(request)

    def _setup_controller(self):
        ret = super()._setup_controller()

        if ret:
            self._report = TestbedServersReport(self._testbed)
            if self._testbed.name in self._testbedList:
                self._moteList = self._generalReport._get_testbed_server()
            else:
                self._moteList = []

        return ret
