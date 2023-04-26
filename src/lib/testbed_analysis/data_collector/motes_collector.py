from ..utils import TestbedData


class TestbedMotesDataCollector:

    '''
        Collect mote data from testbed database.

        ### Attributes

        * moteType: Group of motes from which data will be collected \
            ( client | server ).
        * testbed: testbed data structure.
    '''

    def __init__(
        self,
        moteType: 'str',
        testbed: 'TestbedData'
    ):
        moteType = moteType.lower()

        assert moteType in ('client', 'server'), 'Invalid Mote Type.'

        self._moteType = moteType
        self._testbed = testbed

    def _get_list(
        self, 
        field: 'str',
        moteAddr: 'str',
        peerAddr: 'str' = None,
        unique: 'bool' = False
    ) -> 'list':
        ''' 
            collects a list of values from testbed.
        '''

        tags = {
            'addr': moteAddr
        }

        if peerAddr:
            tags['peer'] = peerAddr

        data = self._testbed.database.select(
            bucket=self._testbed.name,
            measurement=self._moteType,
            field=field,
            tags=tags,
            unique=unique
        )

        return data
    
    def _get_number(
        self,
        field: 'str',
        moteAddr: 'str',
        peerAddr: 'str' = None,
        unique: 'bool' = False
    ):
        ''' 
            collects a numeric value from testbed.
        '''

        tags = {
            'addr': moteAddr
        }

        if peerAddr:
            tags['peer'] = peerAddr

        data = self._testbed.database.count(
            bucket=self._testbed.name,
            measurement=self._moteType,
            field=field,
            tags=tags,
            unique=unique
        )

        return data
    
    def get_motes(self) -> 'list':
        ''' 
            return: mote list.
        '''

        data = self._testbed.database.list_tag_values(
            tagkey='addr',
            bucket=self._testbed.name,
            measurement=self._moteType
        )

        return data

    def get_peers(
        self,
        moteAddr: 'str'
    ):
        ''' 
            return: mote peers list.
        '''
        
        data = self._testbed.database.list_tag_values(
            tagkey='peer',
            bucket=self._testbed.name,
            measurement=self._moteType,
            tags={'addr': moteAddr},
            fields=['tx']
        )

        return data

    def get_packets(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'list':
        ''' 
            return: packet list.
        '''

        data = self._get_list('tx', moteAddr, peerAddr)

        return data

    def get_packets_count(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'int':
        ''' 
            return: number of packets (Tx for clients and 
            Rx for servers).
        '''

        data = self._get_number('tx', moteAddr, peerAddr)

        return data
    
    def get_tx_powers(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'int':
        ''' 
            return: tx power list.
        '''

        data = self._get_list('txpwr', moteAddr, peerAddr)

        return data
    
    def get_packets_len(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'list':
        ''' 
            return: packet lens list.
        '''

        data = self._get_list('datalen', moteAddr, peerAddr)

        return data

    def get_packets_channel(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'list':
        ''' 
            return: channels used by packets list.
        '''

        data = self._get_list('ch', moteAddr, peerAddr)

        return data

    def get_throughput(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ):
        ''' 
            return: mote throughput per second list.
        '''

        data = self._get_list('throughput', moteAddr, peerAddr)

        return data