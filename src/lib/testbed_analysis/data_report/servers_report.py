from ..utils import TestbedData
from ..data_collector import TestbedClientsDataCollector
from . import TestbedMotesReport


class TestbedServersReport(TestbedMotesReport):

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        super().__init__('server', testbed)

        self._cliCollector = TestbedClientsDataCollector(self._testbed)

    def _get_raw_pdr(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['pdr']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                cli = peer.replace('fd00', 'fe80')
                srv = moteAddr.replace('fe80', 'fd00')
                data = self._cliCollector.get_PDRs(cli, srv)
                self._report['raw']['pdr'][peer] = data

        return self._report['raw']['pdr']

    def _get_raw_per(
        self,
        moteAddr: 'str',
    ) -> 'dict':
        if not self._report['raw']['per']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                cli = peer.replace('fd00', 'fe80')
                srv = moteAddr.replace('fe80', 'fd00')
                data = self._cliCollector.get_PERs(cli, srv)
                self._report['raw']['per'][peer] = data

        return self._report['raw']['per']

    def _get_raw_delay(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['delay']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                cli = peer.replace('fd00', 'fe80')
                srv = moteAddr.replace('fe80', 'fd00')
                data = self._cliCollector.get_delays(cli, srv)
                self._report['raw']['delay'][peer] = data

        return self._report['raw']['delay']

    def _get_raw_rssi(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['rssi']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                data = self._collector.get_packets_rssi(moteAddr, peer)
                self._report['raw']['rssi'][peer] = data

        return self._report['raw']['rssi']

    def _get_raw_acked(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['acked']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                cli = peer.replace('fd00', 'fe80')
                srv = moteAddr.replace('fe80', 'fd00')
                data = self._cliCollector.get_ack_packets(cli, srv)
                self._report['raw']['acked'][peer] = data

        return self._report['raw']['acked']
    
    def _get_count_acked(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['count']['acked']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                cli = peer.replace('fd00', 'fe80')
                srv = moteAddr.replace('fe80', 'fd00')
                data = self._cliCollector.get_ack_packets_count(cli, srv)
                self._report['count']['acked'][peer] = data

        return self._report['count']['acked']
