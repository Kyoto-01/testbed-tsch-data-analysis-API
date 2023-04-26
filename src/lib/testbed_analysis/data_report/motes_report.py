from abc import abstractmethod

from ..utils import TestbedData
from ..data_collector import TestbedClientsDataCollector
from ..data_collector import TestbedServersDataCollector
from ..data_analyzer import TestbedDataAnalyzer
from . import TestbedReport


class TestbedMotesReport(TestbedReport):

    def __init__(
        self,
        moteType: 'str',
        testbed: 'TestbedData'
    ):
        moteType = moteType.lower()
        assert moteType in ('client', 'server')

        super().__init__(testbed)

        self._moteType = moteType  # only for debug

        self._collector = None

        if moteType == 'client':
            self._collector = TestbedClientsDataCollector(testbed)
        else:
            self._collector = TestbedServersDataCollector(testbed)

    def _get_general_addr(
        self,
        moteAddr: 'str'
    ) -> 'str':
        if not self._report['general']['addr']:
            self._report['general']['addr'] = moteAddr

        return self._report['general']['addr']

    def _get_general_peer(
        self,
        moteAddr: 'str'
    ) -> 'list':
        if not self._report['general']['peer']:
            data = self._collector.get_peers(moteAddr)
            self._report['general']['peer'] = data

        return self._report['general']['peer']

    def _get_raw_throughput(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['throughput']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                data = self._collector.get_throughput(moteAddr, peer)
                self._report['raw']['throughput'][peer] = data

        return self._report['raw']['throughput']

    def _get_raw_packet(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['packet']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                data = self._collector.get_packets(moteAddr, peer)
                self._report['raw']['packet'][peer] = data

        return self._report['raw']['packet']

    def _get_raw_pktlen(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['pktlen']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                data = self._collector.get_packets_len(moteAddr, peer)
                self._report['raw']['pktlen'][peer] = data

        return self._report['raw']['pktlen']

    def _get_raw_channel(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['channel']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                data = self._collector.get_packets_channel(moteAddr, peer)
                self._report['raw']['channel'][peer] = data

        return self._report['raw']['channel']

    def _get_raw_txpower(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['txpower']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                data = self._collector.get_tx_powers(moteAddr, peer)
                self._report['raw']['txpower'][peer] = data

        return self._report['raw']['txpower']
    
    @abstractmethod
    def _get_raw_rssi(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    def _get_mean_rssi(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['rssi']:
            rssis = self._get_raw_rssi(moteAddr)

            for peer, rssi in rssis.items():
                data = TestbedDataAnalyzer.get_mean(rssi)
                self._report['mean']['rssi'][peer] = data

        return self._report['mean']['rssi']

    def _get_count_packet(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['count']['packet']:
            peers = self._get_general_peer(moteAddr)

            for peer in peers:
                data = self._collector.get_packets_count(moteAddr, peer)
                self._report['count']['packet'][peer] = data

        return self._report['count']['packet']

    def _get_report_general(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        super()._get_report_general(moteAddr, subtitle)

        if subtitle == 'peer':
            self._get_general_peer(moteAddr)
        elif not subtitle:
            self._get_general_peer(moteAddr)

        return self._report['general']

    def _get_report_mean(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        super()._get_report_mean(moteAddr, subtitle)

        if subtitle == 'rssi':
            self._get_mean_rssi(moteAddr)
        elif not subtitle:
            self._get_mean_rssi(moteAddr)

        return self._report['mean']

    def _get_report_raw(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        super()._get_report_raw(moteAddr, subtitle)

        if subtitle == 'rssi':
            self._get_raw_rssi(moteAddr)
        elif not subtitle:
            self._get_raw_rssi(moteAddr)

        return self._report['raw']
