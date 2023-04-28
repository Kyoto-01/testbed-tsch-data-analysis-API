from . import TestbedMotesDataCollector
from ..utils import TestbedData


class TestbedServersDataCollector(TestbedMotesDataCollector):

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        super().__init__('server', testbed)

        self._generalCollector = TestbedMotesDataCollector(
            moteType='server_general', 
            testbed=self._testbed
        )

    def get_packets_rssi(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'list':
        ''' 
            return: packets rssi list.
        '''

        data = self._get_list('rssi', moteAddr, peerAddr)

        return data

    def get_mean_throughputs(
        self,
        moteAddr: 'str'
    ):
        ''' 
            return: mote mean throughputs over time.
        '''

        data = self._generalCollector._get_list('throughput', moteAddr)

        return data
