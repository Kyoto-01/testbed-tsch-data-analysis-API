from ..utils import TestbedData
from . import TestbedMotesReport


class TestbedServersReport(TestbedMotesReport):

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        super().__init__('server', testbed)

    def _get_testbed_server(self):
        if not self._report['testbed']['server']:
            data = self._collector.get_motes()
            self._report['testbed']['server'] = data

        return self._report['testbed']['server']

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

    def _get_report_testbed(
        self, 
        subtitle: 'str'
    ) -> 'dict':
        super()._get_report_testbed(subtitle)

        if subtitle == 'server':
            self._get_testbed_server()
        elif not subtitle:
            self._get_testbed_server()

        return self._report['testbed'] 
