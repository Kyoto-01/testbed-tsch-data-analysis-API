from lib.testbed_analysis import TestbedData
from lib.testbed_analysis import TestbedClientsReport
from lib.testbed_analysis import TestbedServersReport
from lib.testbed_analysis import TestbedGeneralReport
from lib.testbed_analysis import TestbedDataAnalyzer
from lib.testbed_analysis import TestbedDataPersist
from lib.testbed_analysis.utils import list_utils
from lib.testbed_analysis import REPORT_FORMAT


class TestbedAnalysisRPC:

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        self._testbed = testbed
        self._dataPersist = TestbedDataPersist(testbed)

    def analyze_clients_throughput(self):
        allReport = TestbedGeneralReport(self._testbed)
        clients = allReport._get_testbed_client()

        throughputsGeneral = []

        for c in clients:
            report = TestbedClientsReport(self._testbed)
            packets = report._get_raw_packet(c)

            throughputsMote = []

            # throughput per link
            for k, v in packets.items():
                data = TestbedDataAnalyzer.get_packet_throughput(v)
                throughputsMote.append({'value': data})
                data = {'throughput': data}
                self._dataPersist.persist('client', c, k, data)

            # throughput per mote
            data = TestbedDataAnalyzer.get_mean(throughputsMote)
            throughputsGeneral.append({'value': data})
            data = {'throughput': data}
            self._dataPersist.persist('client_general', c, None, data)

        # throughput general
        data = TestbedDataAnalyzer.get_mean(throughputsGeneral)
        data = {'throughput': data}
        self._dataPersist.persist('general', None, None, data)

    def analyze_servers_throughput(self):
        allReport = TestbedGeneralReport(self._testbed)
        servers = allReport._get_testbed_server()

        for s in servers:
            report = TestbedServersReport(self._testbed)
            packets = report._get_raw_packet(s)

            throughputsMote = []

            # throughput per link
            for k, v in packets.items():
                data = TestbedDataAnalyzer.get_packet_throughput(v)
                throughputsMote.append({'value': data})
                data = {'throughput': data}
                self._dataPersist.persist('server', s, k, data)

            # throughput per mote
            data = TestbedDataAnalyzer.get_mean(throughputsMote)
            data = {'throughput': data}
            self._dataPersist.persist('server_general', s, None, data)

    def analyze_clients_pdr(self):
        allReport = TestbedGeneralReport(self._testbed)
        clients = allReport._get_testbed_client()
        pdrsGeneral = []

        for c in clients:
            report = TestbedClientsReport(self._testbed)
            pktcount = report._get_count_packet(c)
            ackcount = report._get_count_acked(c)

            pdrsMote = []

            # PDR per link
            for k in pktcount:
                data = TestbedDataAnalyzer.get_PDR(pktcount[k], ackcount[k])
                pdrsMote.append({'value': data})
                data = {'pdr': data}
                self._dataPersist.persist('client', c, k, data)

            # PDR per mote
            data = TestbedDataAnalyzer.get_mean(pdrsMote)
            pdrsGeneral.append({'value': data})
            data = {'pdr': data}
            self._dataPersist.persist('client_general', c, None, data)

        # PDR general
        data = TestbedDataAnalyzer.get_mean(pdrsGeneral)
        data = {'pdr': data}
        self._dataPersist.persist('general', None, None, data)

    def analyze_clients_per(self):
        allReport = TestbedGeneralReport(self._testbed)
        clients = allReport._get_testbed_client()
        persGeneral = []

        for c in clients:
            report = TestbedClientsReport(self._testbed)
            pktcount = report._get_count_packet(c)
            ackcount = report._get_count_acked(c)

            persMote = []

            # PER per link
            for k in pktcount:
                data = TestbedDataAnalyzer.get_PER(pktcount[k], ackcount[k])
                persMote.append({'value': data})
                data = {'per': data}
                self._dataPersist.persist('client', c, k, data)

            # PER per mote
            data = TestbedDataAnalyzer.get_mean(persMote)
            persGeneral.append({'value': data})
            data = {'per': data}
            self._dataPersist.persist('client_general', c, None, data)

        # PER general
        data = TestbedDataAnalyzer.get_mean(persGeneral)
        data = {'per': data}
        self._dataPersist.persist('general', None, None, data)

    def analyze_clients_delay(self):
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

            # delays per link
            for p in peers:
                srvReport.reset()

                linkPrevDelays = prevDelays[p]
                linkTxpkts = txpkts[p]
                linkRxpkts = srvReport._get_raw_packet(p.replace('fd00', 'fe80'))
                linkRxpkts = linkRxpkts[c.replace('fe80', 'fd00')]

                data = TestbedDataAnalyzer.get_delays(
                    linkTxpkts[len(linkPrevDelays):], linkRxpkts
                )

                for d in data:
                    delaysMote.append({'value': d})
                    d = {'delay2': d}
                    self._dataPersist.persist('client', c, p, d)

                delaysMote = delaysMote + linkPrevDelays

            # delays per mote
            data = TestbedDataAnalyzer.get_mean(delaysMote)
            delaysGeneral.append({'value': data})
            data = {'delay2': data}
            self._dataPersist.persist('client_general', c, None, data)

        # delays general
        data = TestbedDataAnalyzer.get_mean(delaysGeneral)
        data = {'delay2': data}
        self._dataPersist.persist('general', None, None, data)
