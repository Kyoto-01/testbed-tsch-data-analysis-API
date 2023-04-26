from abc import ABC, abstractmethod
from datetime import datetime
from copy import deepcopy

from ..utils import TestbedData
from ..data_analyzer import TestbedDataAnalyzer


REPORT_FORMAT = {
    'count': {
        'packet': {},
        'acked': {},
        'pktbit': {},
        'ackbit': {},
    },
    'mean': {
        'throughput': {},
        'pdr': {},
        'per': {},
        'delay': {},
        'pktlen': {},
        'rssi': {}
    },
    'raw': {
        'throughput': {},
        'pdr': {},
        'per': {},
        'delay': {},
        'packet': {},
        'acked': {},
        'pktlen': {},
        'channel': {},
        'txpower': {},
        'rssi': {}
    },
    'general': {
        'addr': '',
        'start': 0,
        'uptime': 0,
        'peer': []
    },
    'testbed': {
        'name': '',
        'client': [],
        'server': []
    },
    'date': 0
}


class TestbedReport(ABC):

    def __init__(
        self,
        testbed: 'TestbedData'
    ):
        self._testbed = testbed
        self._report: 'dict' = deepcopy(REPORT_FORMAT)

    def _get_date(self):
        if not self._report['date']:
            self._report['date'] = datetime.now()

        return self._report['date']

    def _get_testbed_name(self):
        if not self._report['testbed']['name']:
            self._report['testbed']['name'] = self._testbed.name

        return self._report['testbed']['name']

    def _get_general_start(
        self,
        moteAddr: 'str'
    ) -> 'float':
        if not self._report['general']['uptime']:
            packets = self._get_raw_packet(moteAddr)['all']
            data = packets[0][1]
            self._report['general']['uptime'] = data

        return self._report['general']['uptime']
    
    def _get_general_uptime(
        self,
        moteAddr: 'str'
    ) -> 'float':
        if not self._report['general']['uptime']:
            packets = self._get_raw_packet(moteAddr)['all']
            data = TestbedDataAnalyzer.get_uptime(packets)
            self._report['general']['uptime'] = data

        return self._report['general']['uptime']

    def _get_mean_pktlen(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['pktlen']:
            pktlens = self._get_raw_pktlen(moteAddr)

            for v, k in enumerate(pktlens):
                data = TestbedDataAnalyzer.get_mean(v)
                self._report['mean']['pktlen'][k] = data

        return self._report['mean']['pktlen']
    
    def _get_mean_throughput(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['throughput']:
            throughputs = self._get_raw_throughput(moteAddr)

            for v, k in enumerate(throughputs):
                data = TestbedDataAnalyzer.get_mean(v)
                self._report['mean']['throughput'][k] = data

        return self._report['mean']['throughput']

    @abstractmethod
    def _get_count_packet(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    def _get_count_pktbit(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['count']['pktbit']:
            counts = self._get_count_packet(moteAddr)

            for v, k in enumerate(counts):
                data = self._get_mean_pktlen(moteAddr)[k]
                data *= v
                self._report['count']['pktbit'][k] = data

        return self._report['count']['pktbit']
    
    @abstractmethod
    def _get_raw_throughput(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    @abstractmethod
    def _get_raw_packet(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    @abstractmethod
    def _get_raw_pktlen(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    @abstractmethod
    def _get_raw_channel(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    @abstractmethod
    def _get_raw_txpower(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass
    
    def _get_report_testbed(
        self,
        subtitle: 'str'
    ) -> 'dict':
        if subtitle == 'name':
            self._get_testbed_name()
        elif not subtitle:
            self._get_testbed_name()

        return self._report['testbed']

    def _get_report_general(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        if subtitle == 'start':
            self._get_general_start(moteAddr)
        elif subtitle == 'uptime':
            self._get_general_uptime(moteAddr)
        elif not subtitle:
            self._get_general_start(moteAddr)
            self._get_general_uptime(moteAddr)

        return self._report['general']

    def _get_report_mean(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        if subtitle == 'throughput':
            self._get_mean_throughput(moteAddr)
        elif subtitle == 'pktlen':
            self._get_mean_pktlen(moteAddr)
        elif not subtitle:
            self._get_mean_throughput(moteAddr)
            self._get_mean_pktlen(moteAddr)

        return self._report['mean']

    def _get_report_count(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        if subtitle == 'packet':
            self._get_count_packet(moteAddr)
        elif subtitle == 'pktbit':
            self._get_count_pktbit(moteAddr)
        elif not subtitle:
            self._get_count_packet(moteAddr)
            self._get_count_pktbit(moteAddr)

        return self._report['count']

    def _get_report_raw(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        if subtitle == 'throughput':
            self._get_raw_throughput(moteAddr)
        elif subtitle == 'packet':
            self._get_raw_packet(moteAddr)
        elif subtitle == 'pktlen':
            self._get_raw_pktlen(moteAddr)
        elif subtitle == 'channel':
            self._get_raw_channel(moteAddr)
        elif subtitle == 'txpower':
            self._get_raw_txpower(moteAddr)
        elif not subtitle:
            self._get_raw_throughput(moteAddr)
            self._get_raw_packet(moteAddr)
            self._get_raw_pktlen(moteAddr)
            self._get_raw_channel(moteAddr)
            self._get_raw_txpower(moteAddr)

        return self._report['raw']
    
    def _set_report_topic(   
        self,     
        moteAddr: 'str',
        title: 'str',
        subtitle: 'str' = None
    ):
        if title == 'general':
            self._get_report_general(moteAddr, subtitle)
        elif title == 'raw':
            self._get_report_raw(moteAddr, subtitle)
        elif title == 'mean':
            self._get_report_mean(moteAddr, subtitle)
        elif title == 'count':
            self._get_report_count(moteAddr, subtitle)
        elif title == 'testbed':
            self._get_report_testbed(subtitle)

    def get_report(
        self,
        moteAddr: 'str',
        topics: 'list[str]'
    ):
        '''
        topics: a list of topics of the report in the format
        "title/subtitle" or "title/".
        '''

        for topic in topics:
            title, subtitle = topic.split('/')
            self._set_report_topic(moteAddr, title, subtitle)

        self._get_date()

        return self._report

    def reset(self):
        self._report = deepcopy(REPORT_FORMAT)