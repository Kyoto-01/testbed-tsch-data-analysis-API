from data_collector.motes_collector import TestbedMotesDataCollector
from data_collector.motes_collector import TestbedData
from utils.list_utils import get_first_occurrences


class TestbedClientsDataCollector(TestbedMotesDataCollector):

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        super().__init__('client', testbed)

    def get_ack_packets(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'list':
        ''' 
            return: acknowledged packets list.
        '''

        tags = {
            'addr': moteAddr
        }

        if peerAddr:
            tags['peer'] = peerAddr

        txpkts = self.get_packets(moteAddr, peerAddr)

        rxpkts = self._testbed.database.select(
            bucket=self._testbed.name,
            measurement=self._moteType,
            field='rx',
            tags=tags
        )

        ackpkts = []

        for ack in get_first_occurrences(rxpkts):
            index, time = ack[0], ack[1]['time']
            ackpkts.append({
                'time:': time,
                'value': txpkts[index]['value']
            })

        return ackpkts

    def get_ack_packets_count(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'int':
        ''' 
            return: number of acknowledged packets.
        '''

        tags = {
            'addr': moteAddr
        }

        if peerAddr:
            tags['peer'] = peerAddr

        data = self._testbed.database.count(
            bucket=self._testbed.name,
            measurement=self._moteType,
            field='rx',
            tags=tags,
            unique=True
        )

        return data
