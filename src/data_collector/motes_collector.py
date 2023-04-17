from utils.testbed_data import TestbedData


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
            tags={'addr': moteAddr}
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

        tags = {
            'addr': moteAddr
        }

        if peerAddr:
            tags['peer'] = peerAddr

        data = self._testbed.database.select(
            bucket=self._testbed.name,
            measurement=self._moteType,
            field='tx',
            tags=tags
        )

        return data

    def get_packets_count(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'int':
        ''' 
            return: number of packets \
                (Tx for clients and Rx for servers).
        '''

        tags = {
            'addr': moteAddr
        }

        if peerAddr:
            tags['peer'] = peerAddr

        data = self._testbed.database.count(
            bucket=self._testbed.name,
            measurement=self._moteType,
            field='tx',
            tags=tags
        )

        return data

    def get_packets_len(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'list':
        ''' 
            return: packet lens list.
        '''

        tags = {
            'addr': moteAddr
        }

        if peerAddr:
            tags['peer'] = peerAddr

        data = self._testbed.database.select(
            bucket=self._testbed.name,
            measurement=self._moteType,
            field='datalen',
            tags=tags
        )

        return data

    def get_packets_channel(
        self,
        moteAddr: 'str',
        peerAddr: 'str' = None
    ) -> 'list':
        ''' 
            return: channels used by packets list.
        '''

        tags = {
            'addr': moteAddr
        }

        if peerAddr:
            tags['peer'] = peerAddr

        data = self._testbed.database.select(
            bucket=self._testbed.name,
            measurement=self._moteType,
            field='ch',
            tags=tags
        )

        return data
