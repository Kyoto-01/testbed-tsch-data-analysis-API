from ..utils import TestbedData
from . import TestbedMotesDataCollector
from ..utils.list_utils import get_first_occurrences


class TestbedClientsDataCollector(TestbedMotesDataCollector):

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        super().__init__('client', testbed)

        self._generalCollector = TestbedMotesDataCollector(
            moteType='client_general', 
            testbed=self._testbed
        )
    
    def get_ack_packets(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'list':
        ''' 
            return: acknowledged packets list.
        '''

        txpkts = self.get_packets(moteAddr, peerAddr)
        rxpkts = self._get_list('rx', moteAddr, peerAddr)
        ackpkts = []
    
        for ack in get_first_occurrences([p['value'] for p in rxpkts]):
            index = ack[0]
            time = rxpkts[index]['time']
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

        data = self._get_number('rx', moteAddr, peerAddr, unique=True)

        return data
    
    def get_PDRs(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'list':
        ''' 
            return: mote PDRs (Packet Delivery Ratios) over time.
        '''

        data = self._get_list('pdr', moteAddr, peerAddr)

        return data

    def get_PERs(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'list':
        ''' 
            return: mote PERs (Packet Error Ratios) over time.
        '''

        data = self._get_list('per', moteAddr, peerAddr)

        return data

    def get_delays(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'list':
        ''' 
            return: mote delays over time.
        '''

        data = self._get_list('delay', moteAddr, peerAddr)

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

    def get_mean_PDRs(
        self,
        moteAddr: 'str'
    ):
        ''' 
            return: mote mean PDRs over time.
        '''

        data = self._generalCollector._get_list('pdr', moteAddr)

        return data

    def get_mean_PERs(
        self,
        moteAddr: 'str'
    ):
        ''' 
            return: mote mean PERs over time.
        '''

        data = self._generalCollector._get_list('per', moteAddr)

        return data

    def get_mean_delays(
        self,
        moteAddr: 'str'
    ):
        ''' 
            return: mote mean delays over time.
        '''

        data = self._generalCollector._get_list('delay', moteAddr)

        return data
