from datetime import datetime

from lib.testbed_analysis import TestbedData
from lib.testbed_analysis import TestbedClientsReport
from lib.testbed_analysis import TestbedServersReport
from lib.testbed_analysis import TestbedGeneralReport
from lib.testbed_analysis import TestbedDataAnalyzer
from lib.testbed_analysis import TestbedDataPersist


class TestbedAnalysisEntity:

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        self._testbed = testbed
        self._dataPersist = TestbedDataPersist(testbed)

    def analyze_clients_throughput(self) -> 'bool':
        time = datetime.utcnow()

        allReport = TestbedGeneralReport(self._testbed)
        report = TestbedClientsReport(self._testbed)
        clients = allReport._get_testbed_client()

        throughputsGeneral = []

        for c in clients:
            report.reset()

            packets = report._get_raw_packet(c)
            throughputsMote = []

            # throughput per link
            for k, v in packets.items():
                data = TestbedDataAnalyzer.get_packet_throughput(v)
                throughputsMote.append({'value': data})
                data = {'throughput': data}
                self._dataPersist.persist('client', c, k, data, time)

            # throughput per mote
            data = TestbedDataAnalyzer.get_mean(throughputsMote)
            throughputsGeneral.append({'value': data})
            data = {'throughput': data}
            self._dataPersist.persist('client_general', c, None, data, time)

        # throughput general
        data = TestbedDataAnalyzer.get_mean(throughputsGeneral)
        data = {'throughput': data}
        self._dataPersist.persist('general', None, None, data, time)

        return True

    def analyze_servers_throughput(self) -> 'bool':
        time = datetime.utcnow()
        
        allReport = TestbedGeneralReport(self._testbed)
        report = TestbedServersReport(self._testbed)
        servers = allReport._get_testbed_server()

        for s in servers:
            report.reset()

            packets = report._get_raw_packet(s)
            throughputsMote = []

            # throughput per link
            for k, v in packets.items():
                data = TestbedDataAnalyzer.get_packet_throughput(v)
                throughputsMote.append({'value': data})
                data = {'throughput': data}
                self._dataPersist.persist('server', s, k, data, time)

            # throughput per mote
            data = TestbedDataAnalyzer.get_mean(throughputsMote)
            data = {'throughput': data}
            self._dataPersist.persist('server_general', s, None, data, time)

        return True

    def analyze_clients_pdr(self) -> 'bool':
        time = datetime.utcnow()
        
        allReport = TestbedGeneralReport(self._testbed)
        report = TestbedClientsReport(self._testbed)
        clients = allReport._get_testbed_client()
        pdrsGeneral = []

        for c in clients:
            report.reset()

            pktcount = report._get_count_packet(c)
            ackcount = report._get_count_acked(c)

            pdrsMote = []

            # PDR per link
            for k in pktcount:
                data = TestbedDataAnalyzer.get_PDR(pktcount[k], ackcount[k])
                pdrsMote.append({'value': data})
                data = {'pdr': data}
                self._dataPersist.persist('client', c, k, data, time)

            # PDR per mote
            data = TestbedDataAnalyzer.get_mean(pdrsMote)
            pdrsGeneral.append({'value': data})
            data = {'pdr': data}
            self._dataPersist.persist('client_general', c, None, data, time)

        # PDR general
        data = TestbedDataAnalyzer.get_mean(pdrsGeneral)
        data = {'pdr': data}
        self._dataPersist.persist('general', None, None, data, time)

        return True

    def analyze_clients_per(self) -> 'bool':
        time = datetime.utcnow()
        
        allReport = TestbedGeneralReport(self._testbed)
        report = TestbedClientsReport(self._testbed)
        clients = allReport._get_testbed_client()
        persGeneral = []

        for c in clients:
            report.reset()

            pktcount = report._get_count_packet(c)
            ackcount = report._get_count_acked(c)

            persMote = []

            # PER per link
            for k in pktcount:
                data = TestbedDataAnalyzer.get_PER(pktcount[k], ackcount[k])
                persMote.append({'value': data})
                data = {'per': data}
                self._dataPersist.persist('client', c, k, data, time)

            # PER per mote
            data = TestbedDataAnalyzer.get_mean(persMote)
            persGeneral.append({'value': data})
            data = {'per': data}
            self._dataPersist.persist('client_general', c, None, data, time)

        # PER general
        data = TestbedDataAnalyzer.get_mean(persGeneral)
        data = {'per': data}
        self._dataPersist.persist('general', None, None, data, time)

        return True

    def analyze_clients_delay(self, txpktOffsets: 'dict') -> 'dict':
        time = datetime.utcnow()
        
        allReport = TestbedGeneralReport(self._testbed)
        cliReport = TestbedClientsReport(self._testbed)
        srvReport = TestbedServersReport(self._testbed)

        clients = allReport._get_testbed_client()
        delaysGeneral = []

        for c in clients:
            cliReport.reset()

            peers = cliReport._get_general_peer(c)
            prevDelays = cliReport._get_raw_delay(c)
            txpkts = cliReport._get_raw_packet(c)

            delaysMote = []

            if not c in txpktOffsets:
                txpktOffsets[c] = {}

            # delays per link
            for p in peers:
                srvReport.reset()

                linkPrevDelays = prevDelays[p]
                linkTxpkts = txpkts[p]
                linkRxpkts = srvReport._get_raw_packet(p.replace('fd00', 'fe80'))
                linkRxpkts = linkRxpkts[c.replace('fe80', 'fd00')]

                if p not in txpktOffsets[c]:
                    txpktOffsets[c][p] = 0

                data = TestbedDataAnalyzer.get_delays(
                    linkTxpkts[txpktOffsets[c][p]:], linkRxpkts
                )
                
                txpktOffsets[c][p] = len(linkTxpkts)

                for d in data:
                    delaysMote.append({'value': d})
                    d = {'delay': d}
                    self._dataPersist.persist('client', c, p, d, time)

                delaysMote = delaysMote + linkPrevDelays

            # delays per mote
            data = TestbedDataAnalyzer.get_mean(delaysMote)
            delaysGeneral.append({'value': data})
            data = {'delay': data}
            self._dataPersist.persist('client_general', c, None, data, time)

        # delays general
        data = TestbedDataAnalyzer.get_mean(delaysGeneral)
        data = {'delay': data}
        self._dataPersist.persist('general', None, None, data, time)

        return txpktOffsets
