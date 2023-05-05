from ..utils import TestbedData
from ..utils import constants


class TestbedDataPersist:

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        self._testbed = testbed

    def persist(
        self, 
        moteType: 'str',
        moteAddr: 'str', 
        peerAddr: 'str', 
        data: 'dict',
        time = None
    ):
        moteType = moteType.lower()
        
        assert moteType in constants.TESTBED_MEASUREMENTS, \
            'Invalid Mote Type.'

        tags = {}

        if moteAddr:
            tags['addr'] = moteAddr

        if peerAddr:
            tags['peer'] = peerAddr

        self._testbed.database.insert(
            bucket=self._testbed.name,
            measurement=moteType,
            tags=tags,
            fields=data,
            time=time
        )

        
