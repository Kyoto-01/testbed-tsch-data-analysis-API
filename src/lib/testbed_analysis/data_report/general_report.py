from ..utils import TestbedData
from ..data_collector import TestbedClientsDataCollector
from ..data_collector import TestbedServersDataCollector
from ..data_analyzer import TestbedDataAnalyzer
from . import TestbedReport


class TestbedGeneralReport(TestbedReport):

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        super().__init__(testbed)

        self._cliCollector = TestbedClientsDataCollector(testbed)
        self._srvCollector = TestbedServersDataCollector(testbed)

    def _get_testbed_client(self):
        if not self._report['testbed']['client']:
            data = self._cliCollector.get_motes()
            self._report['testbed']['client'] = data

        return self._report['testbed']['client']

    def _get_testbed_server(self):
        if not self._report['testbed']['server']:
            data = self._srvCollector.get_motes()
            self._report['testbed']['server'] = data

        return self._report['testbed']['server']

    def _get_mean_pdr(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['pdr']:
            pdrs = self._get_raw_pdr(moteAddr)

            for peer, pdr in enumerate(pdrs):
                data = TestbedDataAnalyzer.get_mean(pdr)
                self._report['mean']['pdr'][peer] = data

        return self._report['mean']['pdr']

    def _get_mean_per(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['per']:
            pers = self._get_raw_per(moteAddr)

            for peer, per in enumerate(pers):
                data = TestbedDataAnalyzer.get_mean(per)
                self._report['mean']['per'][peer] = data

        return self._report['mean']['per']

    def _get_mean_delay(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['delay']:
            delays = self._get_raw_delay(moteAddr)

            for peer, delay in enumerate(delays):
                data = TestbedDataAnalyzer.get_mean(delay)
                self._report['mean']['delay'][peer] = data

        return self._report['mean']['delay']

    def _get_count_packet(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        ...

    def _get_count_acked(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        ...
    
    def _get_count_ackbit(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['count']['ackbit']:
            counts = self._get_count_acked(moteAddr)

            for peer, count in counts:
                data = self._get_mean_pktlen(moteAddr)[peer]
                data *= count
                self._report['count']['ackbit'][peer] = data

        return self._report['count']['ackbit']
    
    def _get_raw_throughput(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    def _get_raw_packet(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['packet']:
            clients = self._get_testbed_client()
            servers = self._get_testbed_server()

            if moteAddr:
                if moteAddr in clients:
                    data = self._cliCollector.get_packets(moteAddr)
                    self._report['raw']['packet'][moteAddr] = data
                elif moteAddr in servers:
                    data = self._srvCollector.get_packets(moteAddr)
                    self._report['raw']['packet'][moteAddr] = data
            else:
                for c in clients:
                    data = self._cliCollector.get_packets(c)
                    self._report['raw']['packet'][c] = data

                for s in servers:
                    data = self._srvCollector.get_packets(s)
                    self._report['raw']['packet'][s] = data

        return self._report['raw']['packet']

    def _get_raw_pktlen(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['pktlen']:
            clients = self._get_testbed_client()
            servers = self._get_testbed_server()

            if moteAddr:
                if moteAddr in clients:
                    data = self._cliCollector.get_packets_len(moteAddr)
                    self._report['raw']['pktlen'][moteAddr] = data
                elif moteAddr in servers:
                    data = self._srvCollector.get_packets_len(moteAddr)
                    self._report['raw']['pktlen'][moteAddr] = data
            for c in clients:
                data = self._cliCollector.get_packets_len(c)
                self._report['raw']['pktlen'][c] = data

            for s in servers:
                data = self._srvCollector.get_packets_len(s)
                self._report['raw']['pktlen'][s] = data

        return self._report['raw']['pktlen']

    def _get_raw_channel(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['channel']:
            clients = self._get_testbed_client()
            servers = self._get_testbed_server()

            if moteAddr:
                if moteAddr in clients:
                    data = self._cliCollector.get_packets_channel(moteAddr)
                    self._report['raw']['channel'][moteAddr] = data
                elif moteAddr in servers:
                    data = self._srvCollector.get_packets_channel(moteAddr)
                    self._report['raw']['channel'][moteAddr] = data
            else:
                for c in clients:
                    data = self._cliCollector.get_packets_channel(c)
                    self._report['raw']['channel'][c] = data

                for s in servers:
                    data = self._srvCollector.get_packets_channel(s)
                    self._report['raw']['channel'][s] = data

        return self._report['raw']['channel']

    def _get_raw_txpower(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['txpower']:
            clients = self._get_testbed_client()
            servers = self._get_testbed_server()

            if moteAddr:
                if moteAddr in clients:
                    data = self._cliCollector.get_tx_powers(moteAddr)
                    self._report['raw']['txpower'][moteAddr] = data
                elif moteAddr in servers:
                    data = self._srvCollector.get_tx_powers(moteAddr)
                    self._report['raw']['txpower'][moteAddr] = data
            else:
                for c in clients:
                    data = self._cliCollector.get_tx_powers(c)
                    self._report['raw']['txpower'][c] = data

                for s in servers:
                    data = self._srvCollector.get_tx_powers(s)
                    self._report['raw']['txpower'][s] = data

        return self._report['raw']['txpower']

    def _get_raw_pdr(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['packet']:
            clients = self._get_testbed_client()
            servers = self._get_testbed_server()

            if moteAddr:
                if moteAddr in clients:
                    data = self._cliCollector.get_packets(moteAddr)
                    self._report['raw']['packet'][moteAddr] = data
                elif moteAddr in servers:
                    data = self._srvCollector.get_packets(moteAddr)
                    self._report['raw']['packet'][moteAddr] = data
            else:
                for c in clients:
                    data = self._cliCollector.get_packets(c)
                    self._report['raw']['packet'][c] = data

                for s in servers:
                    data = self._srvCollector.get_packets(s)
                    self._report['raw']['packet'][s] = data

        return self._report['raw']['packet']

    def _get_raw_per(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    def _get_raw_delay(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass
