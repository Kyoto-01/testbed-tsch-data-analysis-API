from abc import ABC, abstractmethod
from datetime import datetime
from copy import deepcopy

from ..utils import TestbedData
from ..utils.list_utils import dict_list_values_to_list
from ..utils.list_utils import order_by_sublist_key
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
    'allmean': {
        'throughput': .0,
        'pdr': .0,
        'per': .0,
        'delay': .0,
        'pktlen': .0,
        'rssi': .0
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
        'start': .0,
        'uptime': .0,
        'peer': []
    },
    'testbed': {
        'name': '',
        'client': [],
        'server': []
    },
    'date': .0
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
            self._report['date'] = datetime.now().timestamp()

        return self._report['date']

    def _get_testbed_name(self):
        if not self._report['testbed']['name']:
            self._report['testbed']['name'] = self._testbed.name

        return self._report['testbed']['name']

    def _get_general_start(
        self,
        moteAddr: 'str'
    ) -> 'float':
        if not self._report['general']['start']:
            packets = self._get_raw_packet(moteAddr)
            packets = dict_list_values_to_list(packets)
            packets = order_by_sublist_key(packets, 'time')

            data = packets[0]['time']
            data = data.timestamp()
            self._report['general']['start'] = data

        return self._report['general']['start']
    
    def _get_general_uptime(
        self,
        moteAddr: 'str'
    ) -> 'float':
        if not self._report['general']['uptime']:
            packets = self._get_raw_packet(moteAddr)
            packets = dict_list_values_to_list(packets)
            packets = order_by_sublist_key(packets, 'time')

            data = TestbedDataAnalyzer.get_uptime(packets)
            self._report['general']['uptime'] = data

        return self._report['general']['uptime']
    
    @abstractmethod
    def _get_raw_packet(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    @abstractmethod
    def _get_raw_throughput(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    @abstractmethod
    def _get_raw_pdr(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    @abstractmethod
    def _get_raw_per(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass

    @abstractmethod
    def _get_raw_delay(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        pass
    
    def _get_mean_throughput(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['throughput']:
            throughputs = self._get_raw_throughput(moteAddr)

            for k, v in throughputs.items():
                data = TestbedDataAnalyzer.get_mean(v)
                self._report['mean']['throughput'][k] = data

        return self._report['mean']['throughput']

    def _get_mean_pdr(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['pdr']:
            pdrs = self._get_raw_pdr(moteAddr)

            for k, v in pdrs.items():
                data = TestbedDataAnalyzer.get_mean(v)
                self._report['mean']['pdr'][k] = data

        return self._report['mean']['pdr']

    def _get_mean_per(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['per']:
            pers = self._get_raw_per(moteAddr)

            for k, v in pers.items():
                data = TestbedDataAnalyzer.get_mean(v)
                self._report['mean']['per'][k] = data

        return self._report['mean']['per']

    def _get_mean_delay(
        self,
        moteAddr: 'str'
    ) -> 'dict':
        if not self._report['mean']['delay']:
            delays = self._get_raw_delay(moteAddr)

            for k, v in delays.items():
                data = TestbedDataAnalyzer.get_mean(v)
                self._report['mean']['delay'][k] = data

        return self._report['mean']['delay']
    
    def _get_allmean_throughput(
        self,
        moteAddr: 'str'
    ) -> 'float':
        if not self._report['allmean']['throughput']:
            mthroughputs = self._get_mean_throughput(moteAddr)
            mthroughputs = list(mthroughputs.values())

            data = sum(mthroughputs) / len(mthroughputs)
            self._report['allmean']['throughput'] = data

        return self._report['allmean']['throughput']

    def _get_allmean_pdr(
        self,
        moteAddr: 'str'
    ) -> 'float':
        if not self._report['allmean']['pdr']:
            mpdrs = self._get_mean_pdr(moteAddr)
            mpdrs = list(mpdrs.values())

            data = sum(mpdrs) / len(mpdrs)
            self._report['allmean']['pdr'] = data

        return self._report['allmean']['pdr']
    
    def _get_allmean_per(
        self,
        moteAddr: 'str'
    ) -> 'float':
        if not self._report['allmean']['per']:
            mpers = self._get_mean_per(moteAddr)
            mpers = list(mpers.values())

            data = sum(mpers) / len(mpers)
            self._report['allmean']['per'] = data

        return self._report['allmean']['per']
    
    def _get_allmean_delay(
        self,
        moteAddr: 'str'
    ) -> 'float':
        if not self._report['allmean']['delay']:
            mdelays = self._get_mean_delay(moteAddr)
            mdelays = list(mdelays.values())

            data = sum(mdelays) / len(mdelays)
            self._report['allmean']['delay'] = data

        return self._report['allmean']['delay']

    def _get_report_testbed(
        self,
        moteAddr: 'str',
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

    def _get_report_raw(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        if subtitle == 'packet':
            self._get_raw_packet(moteAddr)
        elif subtitle == 'throughput':
            self._get_raw_throughput(moteAddr)
        elif subtitle == 'pdr':
            self._get_raw_pdr(moteAddr)
        elif subtitle == 'per':
            self._get_raw_per(moteAddr)
        elif subtitle == 'delay':
            self._get_raw_delay(moteAddr)
        elif not subtitle:
            self._get_raw_throughput(moteAddr)
            self._get_raw_packet(moteAddr)
            self._get_raw_pdr(moteAddr)
            self._get_raw_per(moteAddr)
            self._get_raw_delay(moteAddr)

        return self._report['raw']

    def _get_report_mean(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        if subtitle == 'throughput':
            self._get_mean_throughput(moteAddr)
        elif subtitle == 'pdr':
            self._get_mean_pdr(moteAddr)
        elif subtitle == 'per':
            self._get_mean_per(moteAddr)
        elif subtitle == 'delay':
            self._get_mean_delay(moteAddr)
        elif not subtitle:
            self._get_mean_throughput(moteAddr)
            self._get_mean_pdr(moteAddr)
            self._get_mean_per(moteAddr)
            self._get_mean_delay(moteAddr)

        return self._report['mean']

    def _get_report_allmean(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        if subtitle == 'throughput':
            self._get_allmean_throughput(moteAddr)
        elif subtitle == 'pdr':
            self._get_allmean_pdr(moteAddr)
        elif subtitle == 'per':
            self._get_allmean_per(moteAddr)
        elif subtitle == 'delay':
            self._get_allmean_delay(moteAddr)
        elif not subtitle:
            self._get_allmean_throughput(moteAddr)
            self._get_allmean_pdr(moteAddr)
            self._get_allmean_per(moteAddr)
            self._get_allmean_delay(moteAddr)

        return self._report['allmean']

    def _get_report_count(
        self,
        moteAddr: 'str',
        subtitle: 'str'
    ) -> 'dict':
        return self._report['count']

    def _set_report_by_topic(   
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
        elif title == 'allmean':
            self._get_report_allmean(moteAddr, subtitle)
        elif title == 'count':
            self._get_report_count(moteAddr, subtitle)
        elif title == 'testbed':
            self._get_report_testbed(moteAddr, subtitle)

    def _is_topic_valid(self, topic: 'str') -> 'bool':
        title, subtitle = topic.split('/')[:2]

        return (
            title != 'date' and
            title in self._report and 
            (subtitle in self._report[title] or not subtitle)
        )

    def _format_report_by_topics(
        self,
        topics: 'list[str]'
    ):
        report = {}

        report['date'] = self._report['date']

        for topic in topics:
            if not topic.endswith('/'):
                topic += '/'
        
            title, subtitle = topic.split('/')[:2]

            if self._is_topic_valid(topic):
                report[title] = {}

                if subtitle:
                    report[title][subtitle] = self._report[title][subtitle]
                else:
                    report[title] = self._report[title]
        
        return report
    
    def get_report_by_topics(
        self,
        moteAddr: 'str',
        topics: 'list[str]'
    ):
        '''
            topics: a list of topics of the report in the format
            "title/subtitle" or "title/".
        '''

        for topic in topics:
            if not topic.endswith('/'):
                topic += '/'

            title, subtitle = topic.split('/')[:2]

            if self._is_topic_valid(topic):
                self._set_report_by_topic(moteAddr, title, subtitle)

        self._get_date()

        report = self._format_report_by_topics(topics)

        return report
    
    def get_full_report(
        self,
        moteAddr: 'str'
    ):
        self._get_report_general(moteAddr, None)
        self._get_report_raw(moteAddr, None)
        self._get_report_mean(moteAddr, None)
        self._get_report_allmean(moteAddr, None)
        self._get_report_count(moteAddr, None)
        self._get_report_testbed(moteAddr, None)
        self._get_date()

        return self._report

    def reset(self):
        self._report = deepcopy(REPORT_FORMAT)
