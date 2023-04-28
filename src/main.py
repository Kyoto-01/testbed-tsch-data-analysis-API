#!/usr/bin/env python3

from pprint import pprint

from lib.testbed_analysis.database import InfluxDBConnection
from lib.testbed_analysis import TestbedData
from lib.testbed_analysis import TestbedClientsReport
from lib.testbed_analysis import TestbedServersReport
from lib.testbed_analysis import TestbedGeneralReport
from rpc import TestbedAnalysisRPC


DATABASE_CONFIG_FILE_PATH = '../config.ini'

TESTBED_NAME = 'testbed-71d1877d-356a-4757-9793-724c54c91bdf'


database = InfluxDBConnection(DATABASE_CONFIG_FILE_PATH)

testbed = TestbedData(
    name=TESTBED_NAME,
    database=database
)

analyzerRPC = TestbedAnalysisRPC(testbed)
clientReport = TestbedClientsReport(testbed)
serverReport = TestbedServersReport(testbed)
generalReport = TestbedGeneralReport(testbed)

general = generalReport.get_report(None)
client = clientReport.get_report('fe8000000000000002124b0014b5d33a')
server = serverReport.get_report('fe8000000000000002124b0018e0b9f2')

pprint(general)
pprint(client)
pprint(server)
