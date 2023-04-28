from ..utils import TestbedData
from ..data_collector import TestbedServersDataCollector
from ..data_analyzer import TestbedDataAnalyzer
from . import TestbedMotesReport


class TestbedClientsReport(TestbedMotesReport):

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        super().__init__('client', testbed)

        self._srvCollector = TestbedServersDataCollector(self._testbed)

    def _get_raw_pdr(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['pdr']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                data = self._collector.get_PDRs(moteAddr, peer)
                self._report['raw']['pdr'][peer] = data

        return self._report['raw']['pdr']

    def _get_raw_per(
        self,
        moteAddr: 'str',
    ) -> 'dict':
        if not self._report['raw']['per']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                data = self._collector.get_PERs(moteAddr, peer)
                self._report['raw']['per'][peer] = data

        return self._report['raw']['per']

    def _get_raw_delay(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['delay']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                data = self._collector.get_delays(moteAddr, peer)
                self._report['raw']['delay'][peer] = data

        return self._report['raw']['delay']

    def _get_raw_acked(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['acked']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                data = self._collector.get_ack_packets(moteAddr, peer)
                self._report['raw']['acked'][peer] = data

        return self._report['raw']['acked']

    def _get_raw_rssi(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['rssi']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                srv = peer.replace('fd00', 'fe80')
                cli = moteAddr.replace('fe80', 'fd00')
                data = self._srvCollector.get_packets_rssi(srv, cli)
                self._report['raw']['rssi'][peer] = data

        return self._report['raw']['rssi']

    def _get_mean_pdr(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['pdr']:
            pdrs = self._get_raw_pdr(moteAddr)

            for peer, pdr in pdrs.items():
                data = TestbedDataAnalyzer.get_mean(pdr)
                self._report['mean']['pdr'][peer] = data

        return self._report['mean']['pdr']

    def _get_mean_per(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['per']:
            pers = self._get_raw_per(moteAddr)

            for peer, per in pers.items():
                data = TestbedDataAnalyzer.get_mean(per)
                self._report['mean']['per'][peer] = data

        return self._report['mean']['per']

    def _get_mean_delay(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['delay']:
            delays = self._get_raw_delay(moteAddr)

            for peer, delay in delays.items():
                data = TestbedDataAnalyzer.get_mean(delay)
                self._report['mean']['delay'][peer] = data

        return self._report['mean']['delay']

    def _get_count_acked(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['count']['acked']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                data = self._collector.get_ack_packets_count(moteAddr, peer)
                self._report['count']['acked'][peer] = data

        return self._report['count']['acked']
