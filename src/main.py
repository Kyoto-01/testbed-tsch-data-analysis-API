#!/usr/bin/env python3

from lib.testbed_analysis.database import InfluxDBConnection
from lib.testbed_analysis import TestbedData
from rpc import TestbedAnalysisRPC

from lib.testbed_analysis import TestbedClientsReport
from lib.testbed_analysis import TestbedServersReport
from lib.testbed_analysis import TestbedGeneralReport


DATABASE_CONFIG_FILE_PATH = '../config.ini'

TESTBED_NAME = 'testbed-c99cb42b-9ec6-49b0-8ef4-752c6dd05a47'


database = InfluxDBConnection(DATABASE_CONFIG_FILE_PATH)

testbed = TestbedData(
    name=TESTBED_NAME,
    database=database
)

analyzer = TestbedAnalysisRPC(testbed)

analyzer.analyze_clients_delay()

# allReport = TestbedGeneralReport(testbed)
# srvReport = TestbedServersReport(testbed)
# cliReport = TestbedClientsReport(testbed)

# servers = allReport._get_testbed_server()
# peers = srvReport._get_general_peer(servers[0])

# print(servers, '\n', peers)

# cliReport = TestbedClientsReport(testbed)
# srvReport = TestbedServersReport(testbed)
# allReport = TestbedGeneralReport(testbed)

# clients = allReport._get_testbed_client()
# servers = allReport._get_testbed_server()

# print('CLIENTS:', clients)
# print('PEERS:', cliReport._get_general_peer(clients[0]))
# print('PKTS:', cliReport._get_raw_packet(clients[0]))

# print('SERVERS:', servers)
# print('PEERS:', srvReport._get_general_peer(servers[0]))
