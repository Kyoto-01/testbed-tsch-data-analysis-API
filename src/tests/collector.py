from pprint import pprint
from database.db_connection import InfluxDBConnection
from utils.testbed_data import TestbedData
from utils.list_utils import sequential_values
from data_collector import (
    TestbedClientsDataCollector,
    TestbedServersDataCollector
)


class TestbedMoteCollectorTest:

    def __init__(
        self,
        testbed='testbed-c99cb42b-9ec6-49b0-8ef4-752c6dd05a47',
        clients=['fe8000000000000002124b0014b5d33a'],
        servers=['fe8000000000000002124b0018e0b9f2'],
        verbose=True
    ):
        self.verbose = verbose

        self.db = InfluxDBConnection('../config.ini')

        self.testbed = TestbedData(
            name=testbed,
            database=self.db
        )

        self.staticClients = clients
        self.staticServers = servers

        self.clientCollector = TestbedClientsDataCollector(self.testbed)
        self.serverCollector = TestbedServersDataCollector(self.testbed)

        self.clientList = {}
        self.serverList = {}

    def test_get_motes(self, id):
        print(f'\n* TEST {id}: get_motes()\n')

        print('\tclients.get_motes()')
        for mote in self.clientCollector.get_motes():
            self.clientList[mote] = {}

        print('\tservers.get_motes()')
        for mote in self.serverCollector.get_motes():
            self.serverList[mote] = {}

    def test_get_peers(self, id):
        print(f'\n* TEST {id}: get_peers(addr)\n')

        for mote in self.clientList:
            print(f'\tclients.get_peers({mote})')
            self.clientList[mote]['peers'] = self.clientCollector.get_peers(
                mote)

        for mote in self.serverList:
            print(f'\tservers.get_peers({mote})')
            self.serverList[mote]['peers'] = self.serverCollector.get_peers(
                mote)

    def test_get_packets(self, id):
        print(f'\n* TEST {id}: get_packets(addr, peer)\n')

        for mote in self.clientList:
            print(f'clients.get_packets({mote})')
            clientPkts = [
                p['value'] for p in self.clientCollector.get_packets(mote)
            ]
            self.clientList[mote]['packets'] = {'all': clientPkts}

            for peer in self.clientList[mote]['peers']:
                print(f'clients.get_packets({mote}, {peer})')
                clientPkts = [
                    p['value'] for p in self.clientCollector.get_packets(mote, peer)
                ]
                self.clientList[mote]['packets'][peer] = clientPkts

        for mote in self.serverList:
            print(f'servers.get_packets({mote})')
            serverPkts = [
                p['value'] for p in self.serverCollector.get_packets(mote)
            ]
            self.serverList[mote]['packets'] = {'all': serverPkts}

            for peer in self.serverList[mote]['peers']:
                print(f'servers.get_packets({mote}, {peer})')
                serverPkts = [
                    p['value'] for p in self.serverCollector.get_packets(mote, peer)
                ]
                self.serverList[mote]['packets'][peer] = serverPkts

    def test_get_packets_count(self, id):
        print(f'\n* TEST {id}: get_packets_count(addr, peer)\n')

        for mote in self.clientList:
            print(f'clients.get_packets_count({mote})')
            count = self.clientCollector.get_packets_count(mote)
            self.clientList[mote]['packets_count'] = {'all': count}

            for peer in self.clientList[mote]['peers']:
                print(f'clients.get_packets_count({mote}, {peer})')
                count = self.clientCollector.get_packets_count(mote, peer)
                self.clientList[mote]['packets_count'][peer] = count

        for mote in self.serverList:
            print(f'servers.get_packets_count({mote})')
            count = self.serverCollector.get_packets_count(mote)
            self.serverList[mote]['packets_count'] = {'all': count}

            for peer in self.serverList[mote]['peers']:
                print(f'servers.get_packets_count({mote}, {peer})')
                count = self.serverCollector.get_packets_count(mote, peer)
                self.serverList[mote]['packets_count'][peer] = count

    def test_get_packets_len(self, id):
        print(f'\n* TEST {id}: get_packets_len(addr, peer)\n')

        for mote in self.clientList:
            print(f'clients.get_packets_len({mote})')
            length = [
                p['value'] for p in self.clientCollector.get_packets_len(mote)
            ]
            self.clientList[mote]['packets_len'] = {'all': length}

            for peer in self.clientList[mote]['peers']:
                print(f'clients.get_packets_len({mote}, {peer})')
                length = [
                    p['value'] for p in self.clientCollector.get_packets_len(mote, peer)
                ]
                self.clientList[mote]['packets_len'][peer] = length

        for mote in self.serverList:
            print(f'servers.get_packets_len({mote})')
            length = [
                p['value'] for p in self.serverCollector.get_packets_len(mote)
            ]
            self.serverList[mote]['packets_len'] = {'all': length}

            for peer in self.serverList[mote]['peers']:
                print(f'servers.get_packets_len({mote}, {peer})')
                length = [
                    p['value'] for p in self.serverCollector.get_packets_len(mote, peer)
                ]
                self.serverList[mote]['packets_len'][peer] = length

    def test_get_packets_channel(self, id):
        print(f'\n* TEST {id}: get_packets_channel(addr, peer)\n')

        for mote in self.clientList:
            print(f'clients.get_packets_channel({mote})')
            ch = [
                p['value'] for p in self.clientCollector.get_packets_channel(mote)
            ]
            self.clientList[mote]['packets_channel'] = {'all': ch}

            for peer in self.clientList[mote]['peers']:
                print(f'clients.get_packets_channel({mote}, {peer})')
                ch = [
                    p['value'] for p in self.clientCollector.get_packets_channel(mote, peer)
                ]
                self.clientList[mote]['packets_channel'][peer] = ch

        for mote in self.serverList:
            print(f'servers.get_packets_channel({mote})')
            ch = [
                p['value'] for p in self.serverCollector.get_packets_channel(mote)
            ]
            self.serverList[mote]['packets_channel'] = {'all': ch}

            for peer in self.serverList[mote]['peers']:
                print(f'servers.get_packets_channel({mote}, {peer})')
                ch = [
                    p['value'] for p in self.serverCollector.get_packets_channel(mote, peer)
                ]
                self.serverList[mote]['packets_channel'][peer] = ch

    def test_get_ack_packets_count(self, id):
        print(f'\n* TEST {id}: get_ack_packets_count(addr, peer)\n')

        for mote in self.clientList:
            print(f'clients.get_ack_packets_count({mote})')
            count = self.clientCollector.get_ack_packets_count(mote)
            self.clientList[mote]['ack_packets_count'] = {'all': count}

        for mote in self.clientList:
            for peer in self.clientList[mote]['peers']:
                print(f'clients.get_ack_packets_count({mote}, {peer})')
                count = self.clientCollector.get_ack_packets_count(mote, peer)
                self.clientList[mote]['ack_packets_count'][peer] = count

    def test_ack_packets(self, id):
        print(f'\n* TEST {id}: get_ack_packets(addr, peer)\n')

        tests = []

        for mote in self.clientList:
            print(f'clients.get_ack_packets({mote})')
            clientAckpkts = [
                int(p['value']) for p in self.clientCollector.get_ack_packets(mote)
            ]
            self.clientList[mote]['ack_packets'] = {'all': clientAckpkts}

            tests.append(
                (not sequential_values(clientAckpkts) and
                self.clientCollector.get_ack_packets_count(mote) == len(clientAckpkts))
            )

            for peer in self.clientList[mote]['peers']:
                print(f'clients.get_ack_packets({mote}, {peer})')
                clientAckpkts = [
                    int(p['value']) for p in self.clientCollector.get_ack_packets(mote, peer)
                ]
                self.clientList[mote]['ack_packets'][peer] = clientAckpkts

                tests.append(
                    (not sequential_values(clientAckpkts) and 
                     self.clientCollector.get_ack_packets_count(mote, peer) == len(clientAckpkts))
                )

        print('[ OK ]' if all(tests) else '[ FAIL ]')

    def test_get_packets_rssi(self, id):
        print(f'\n* TEST {id}: get_packets_rssi(addr, peer)\n')

        for mote in self.serverList:
            print(f'servers.get_packets_rssi({mote})')
            rssis = [p['value']
                     for p in self.serverCollector.get_packets_rssi(mote)]
            self.serverList[mote]['packets_rssi'] = {'all': rssis}

        for mote in self.serverList:
            for peer in self.serverList[mote]['peers']:
                print(f'servers.get_packets_rssi({mote}, {peer})')
                rssis = [p['value']
                         for p in self.serverCollector.get_packets_rssi(mote, peer)]
                self.serverList[mote]['packets_rssi'][peer] = rssis

    def test(self):
        self.test_get_motes(1)
        self.test_get_peers(2)
        self.test_get_packets(3)
        self.test_get_packets_count(4)
        self.test_get_packets_len(5)
        self.test_get_packets_channel(6)
        self.test_get_ack_packets_count(7)
        self.test_ack_packets(8)
        self.test_get_packets_rssi(9)

        if self.verbose:
            print('\n\n\n========== LOGS ==========\n\n')
            print('========== CLIENT LOGS ==========\n\n')
            pprint(self.clientList, sort_dicts=False)
            print('\n\n========== SERVER LOGS ==========\n\n')
            pprint(self.serverList, sort_dicts=False)
            print('\n\n==========================\n\n\n')
