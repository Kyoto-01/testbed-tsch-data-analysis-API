from data_collector.motes_collector import TestbedMotesDataCollector
from data_collector.motes_collector import TestbedData


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

        tags = {
            'addr': moteAddr
        }

        if peerAddr:
            tags['peer'] = peerAddr

        data = self._testbed.database.select(
            bucket=self._testbed.name,
            measurement=self._moteType,
            field='rssi',
            tags=tags
        )

        return data
