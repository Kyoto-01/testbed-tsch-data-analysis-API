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

    @abstractmethod
    def _get_raw_rssi(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    @abstractmethod
    def _get_raw_pdr(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    @abstractmethod
    def _get_raw_per(
        self,
        moteAddr: 'str',
    ) -> 'dict':
        pass

    @abstractmethod
    def _get_raw_delay(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    @abstractmethod
    def _get_raw_acked(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

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
    
    def _get_mean_pktlen(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['pktlen']:
            pktlens = self._get_raw_pktlen(moteAddr)

            for k, v in pktlens.items():
                data = TestbedDataAnalyzer.get_mean(v)
                self._report['mean']['pktlen'][k] = data

        return self._report['mean']['pktlen']
    
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

    def _get_allmean_pktlen(
        self,
        moteAddr: 'str'
    ) -> 'float':
        if not self._report['allmean']['pktlen']:
            mpktlens = self._get_mean_pktlen(moteAddr)
            mpktlens = list(mpktlens.values())

            data = sum(mpktlens) / len(mpktlens)
            self._report['allmean']['pktlen'] = data

        return self._report['allmean']['pktlen']
    
    def _get_allmean_rssi(
        self,
        moteAddr: 'str'
    ) -> 'float':
        if not self._report['allmean']['rssi']:
            mrssis = self._get_mean_rssi(moteAddr)
            mrssis = list(mrssis.values())

            data = sum(mrssis) / len(mrssis)
            self._report['allmean']['rssi'] = data

        return self._report['allmean']['rssi']
    
    def _get_allmean_throughput(
        self,
        moteAddr: 'str'
    ) -> 'float':
        if not self._report['allmean']['throughput']:
            mthroughputs = self._get_mean_throughput(moteAddr)
            mthroughputs = list(mthroughputs.values())

            data = sum(mthroughputs) / len(mthroughputs)
            self._report['allmean']['throughput'] = data

        return self._report['allmean']['throughput']

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
    
    def _get_count_pktbit(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['count']['pktbit']:
            counts = self._get_count_packet(moteAddr)

            for k, v in counts.items():
                data = self._get_mean_pktlen(moteAddr)[k]
                data *= v
                self._report['count']['pktbit'][k] = round(data)

        return self._report['count']['pktbit']
    
    @abstractmethod
    def _get_count_acked(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    def _get_count_ackbit(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['count']['ackbit']:
            counts = self._get_count_acked(moteAddr)

            for peer, count in counts.items():
                data = self._get_mean_pktlen(moteAddr)[peer]
                data *= count
                self._report['count']['ackbit'][peer] = round(data)

        return self._report['count']['ackbit']

    def _get_report_general(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        super()._get_report_general(moteAddr, subtitle)

        if subtitle == 'addr':
            self._get_general_addr(moteAddr)
        if subtitle == 'peer':
            self._get_general_peer(moteAddr)
        elif not subtitle:
            self._get_general_addr(moteAddr)
            self._get_general_peer(moteAddr)

        return self._report['general']
    
    def _get_report_count(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        super()._get_report_count(moteAddr, subtitle)

        if subtitle == 'packet':
            self._get_count_packet(moteAddr)
        elif subtitle == 'pktbit':
            self._get_count_pktbit(moteAddr)
        elif subtitle == 'acked':
            self._get_count_acked(moteAddr)
        elif subtitle == 'ackbit':
            self._get_count_ackbit(moteAddr)
        elif not subtitle:
            self._get_count_packet(moteAddr)
            self._get_count_pktbit(moteAddr)
            self._get_count_acked(moteAddr)
            self._get_count_ackbit(moteAddr)

        return self._report['count']

    def _get_report_mean(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        super()._get_report_mean(moteAddr, subtitle)

        if subtitle == 'rssi':
            self._get_mean_rssi(moteAddr)
        elif subtitle == 'pktlen':
            self._get_mean_pktlen(moteAddr)
        elif not subtitle:
            self._get_mean_rssi(moteAddr)
            self._get_mean_pktlen(moteAddr)

        return self._report['mean']

    def _get_report_allmean(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        super()._get_report_allmean(moteAddr, subtitle)

        if subtitle == 'rssi':
            self._get_allmean_rssi(moteAddr)
        elif subtitle == 'pktlen':
            self._get_allmean_pktlen(moteAddr)
        elif not subtitle:
            self._get_allmean_rssi(moteAddr)
            self._get_allmean_pktlen(moteAddr)

        return self._report['allmean']

    def _get_report_raw(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        super()._get_report_raw(moteAddr, subtitle)

        if subtitle == 'rssi':
            self._get_raw_rssi(moteAddr)
        elif subtitle == 'acked':
            self._get_raw_acked(moteAddr)
        elif subtitle == 'pktlen':
            self._get_raw_pktlen(moteAddr)
        elif subtitle == 'channel':
            self._get_raw_channel(moteAddr)
        elif subtitle == 'txpower':
            self._get_raw_txpower(moteAddr)
        elif not subtitle:
            self._get_raw_rssi(moteAddr)
            self._get_raw_acked(moteAddr)
            self._get_raw_pktlen(moteAddr)
            self._get_raw_channel(moteAddr)
            self._get_raw_txpower(moteAddr)

        return self._report['raw']
