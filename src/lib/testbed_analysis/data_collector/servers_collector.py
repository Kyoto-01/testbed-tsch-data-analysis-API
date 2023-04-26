from . import TestbedMotesDataCollector
from ..utils import TestbedData


class TestbedServersDataCollector(TestbedMotesDataCollector):

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        super().__init__('server', testbed)

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
