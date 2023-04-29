from abc import ABC, abstractmethod

from lib.testbed_analysis.database import InfluxDBConnection
from lib.testbed_analysis import TestbedData
from lib.testbed_analysis import TestbedClientsReport
from lib.testbed_analysis import TestbedServersReport
from lib.testbed_analysis import TestbedGeneralReport
from lib.testbed_analysis.data_report import TestbedMotesReport
from utils.constants import DATABASE_CONFIG_FILE_PATH


class ReportController(ABC):

    def __init__(
        self,
        request: 'dict'
    ):
        self._request: 'dict' = request

        database = InfluxDBConnection(DATABASE_CONFIG_FILE_PATH)
        self._testbed: 'TestbedData' = TestbedData(
            name=self._request['testbed_name'],
            database=database
        )

        self._generalReport: 'TestbedMotesReport' = \
            TestbedGeneralReport(self._testbed)

        self._testbedList: 'list' = \
            self._generalReport._get_testbed_testbed()

        self._report: 'TestbedMotesReport' = None

        self._response: 'dict' = None

    def _check_req_parameters_key(self) -> 'bool':
        res = True

        try:
            __ = self._request['testbed_name']
            __ = self._request['topics']

        except KeyError as ke:
            res = False

        return res

    def _check_req_parameters_value_type(self) -> 'bool':
        res = isinstance(self._request['testbed_name'], str)
        res = res and isinstance(self._request['topics'], list)

        return res

    def _check_req_parameters_value(self) -> 'bool':
        res = self._testbed.name in self._testbedList

        return res

    def _check_response(self) -> 'bool':
        res = bool(self._response)

        return res

    def _check_req_parameters_errors(self) -> 'tuple':
        res = None

        if not self._check_req_parameters_key():
            res = (f'Bad request.', 400)
        elif not self._check_req_parameters_value_type():
            res = (f'Bad request.', 400)
        elif not self._check_req_parameters_value():
            res = (f'Resource not found.', 404)

        return res

    @abstractmethod
    def get_report(self) -> 'dict':
        pass


class ReportGeneralController(ReportController):

    def __init__(
        self,
        request: 'dict'
    ):
        super().__init__(request)

        self._report = self._generalReport

    def get_report(self) -> 'dict':
        self._response = self._check_req_parameters_errors()

        if not self._response:
            self._response = self._report.get_report_by_topics(
                None,
                self._request['topics']
            )

            if not self._check_response():
                self._response = (f'Resource not found.', 404)

        return self._response


class ReportMoteController(ReportController):

    def __init__(
        self,
        request: 'dict'
    ):
        super().__init__(request)

        self._moteList = None

    def _check_req_parameters_key(self) -> 'bool':
        res = super()._check_req_parameters_key()

        try:
            __ = self._request['mote_addr']

        except KeyError as ke:
            res = False

        return res

    def _check_req_parameters_value_type(self) -> 'bool':
        res = super()._check_req_parameters_value_type()
        res = res and isinstance(self._request['mote_addr'], str)

        return res

    def _check_req_parameters_value(self) -> 'bool':
        res = super()._check_req_parameters_value()
        res = res and self._request['mote_addr'] in self._moteList

        return res

    def get_report(self) -> 'dict':
        self._response = self._check_req_parameters_errors()

        if not self._response:
            self._response = self._report.get_report_by_topics(
                self._request['mote_addr'],
                self._request['topics']
            )

            if not self._check_response():
                self._response = (f'Resource not found.', 404)

        return self._response


class ReportClientController(ReportMoteController):

    def __init__(
        self,
        request: 'dict'
    ):
        super().__init__(request)

        self._report = TestbedClientsReport(self._testbed)
        self._moteList = self._generalReport._get_testbed_client()


class ReportServerController(ReportMoteController):

    def __init__(
        self,
        request: 'dict'
    ):
        super().__init__(request)

        self._report = TestbedServersReport(self._testbed)
        self._moteList = self._generalReport._get_testbed_server()
