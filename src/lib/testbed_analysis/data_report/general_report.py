from ..utils import TestbedData
from ..data_collector import TestbedClientsDataCollector
from ..data_collector import TestbedServersDataCollector
from ..data_collector import TestbedGeneralDataCollector
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
        self._collector = TestbedGeneralDataCollector(testbed)

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

    def _get_raw_throughput(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['throughput']:
            if moteAddr:
                clients = self._get_testbed_client()
                servers = self._get_testbed_server()

                if moteAddr in clients:
                    data = self._cliCollector.get_throughput(moteAddr)
                    self._report['raw']['throughput'][moteAddr] = data
                elif moteAddr in servers:
                    data = self._srvCollector.get_throughput(moteAddr)
                    self._report['raw']['throughput'][moteAddr] = data
            else:
                data = self._collector.get_throughputs()
                self._report['raw']['throughput']['general'] = data

        return self._report['raw']['throughput']
    
    def _get_raw_pdr(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['pdr']:
            if moteAddr:
                clients = self._get_testbed_client()
                if moteAddr in clients:
                    data = self._cliCollector.get_PDRs(moteAddr)
                    self._report['raw']['pdr'][moteAddr] = data
            else:
                data = self._collector.get_PDRs()
                self._report['raw']['pdr']['general'] = data

        return self._report['raw']['pdr']

    def _get_raw_per(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['per']:
            if moteAddr:
                clients = self._get_testbed_client()
                if moteAddr in clients:
                    data = self._cliCollector.get_PERs(moteAddr)
                    self._report['raw']['per'][moteAddr] = data
            else:
                data = self._collector.get_PERs()
                self._report['raw']['per']['general'] = data

        return self._report['raw']['per']

    def _get_raw_delay(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['raw']['delay']:
            if moteAddr:
                clients = self._get_testbed_client()
                if moteAddr in clients:
                    data = self._cliCollector.get_delays(moteAddr)
                    self._report['raw']['delay'][moteAddr] = data
            else:
                data = self._collector.get_delays()
                self._report['raw']['delay']['general'] = data

        return self._report['raw']['delay']

    def _get_report_testbed(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        super()._get_report_testbed(moteAddr, subtitle)
        
        if subtitle == 'client':
            self._get_testbed_client()
        elif subtitle == 'server':
            self._get_testbed_server()
        elif not subtitle:
            self._get_testbed_client()
            self._get_testbed_server()

        return self._report['testbed']
