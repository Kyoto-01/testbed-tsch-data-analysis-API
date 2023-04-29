from ..utils import TestbedData


class TestbedGeneralDataCollector:

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        self._moteType = 'general'
        self._testbed = testbed

    def _get_list(
        self, 
        field: 'str',
        unique: 'bool' = False,
    ) -> 'list':
        ''' 
            collects a list of values from testbed.
        '''

        data = self._testbed.database.select(
            bucket=self._testbed.name,
            measurement=self._moteType,
            field=field,
            unique=unique
        )

        return data
    
    def _get_number(
        self,
        field: 'str',
        unique: 'bool' = False
    ) -> 'int':
        ''' 
            collects a numeric value from testbed.
        '''

        data = self._testbed.database.count(
            bucket=self._testbed.name,
            measurement=self._moteType,
            field=field,
            unique=unique
        )

        return data
    
    def get_testbeds(self) -> 'list':
        ''' 
            collects a list of executed (or in execution) testbeds.
        '''
                
        data = self._testbed.database.get_buckets(bucketType='user')

        return data
    
    def get_motes(self) -> 'list':
        ''' 
            return: testbed general mote list.
        '''

        data = self._testbed.database.list_tag_values(
            tagkey='addr',
            bucket=self._testbed.name
        )

        return data

    def get_throughputs(self):
        ''' 
            return: testbed mean throughput over time.
        '''

        data = self._get_list('throughput')

        return data
    
    def get_PDRs(self):
        ''' 
            return: testbed mean PDR over time.
        '''

        data = self._get_list('pdr')

        return data
    
    def get_PERs(self):
        ''' 
            return: testbed mean PER over time.
        '''

        data = self._get_list('per')

        return data
    
    def get_delays(self):
        ''' 
            return: testbed mean delay over time.
        '''

        data = self._get_list('delay')

        return data
