
class TestbedClientDataAnalyzer:

    def __init__(self):
        pass

    def get_mean_packet_len(
        self,
        pktlens: 'list'
    ) -> 'int':

        ''' 
            return: mean tx packet len
        '''

        mean = 0

        if pktlens:
            pktlens = [pl['value'] for pl in pktlens]
            mean = int(sum(pktlens) / len(pktlens))

        return mean

    def get_packet_throughput(
        self,
        txpkts: 'list'
    ) -> 'int':
        
        ''' 
            return: throughput in pps (packets per second) 
        '''

        throughput = 0

        if txpkts:
            pktnum = len(txpkts)

            time = (txpkts[pktnum - 1]['time'] - txpkts[0]['time'])
            time = time.total_seconds()

            # throughput in pps (packets per second)
            throughput = int(pktnum / time)

        return throughput

    def get_bit_throughput(
        self,
        txpkts: 'list',
        pktlen: 'int'
    ) -> 'int':
        
        ''' 
            return: throughput in bps (bits per second) 
        '''

        throughput = 0

        if txpkts:
            # throughput in pps (packets per second)
            throughput = self.get_packet_throughput(txpkts)

            # throughput in bps (bits per second)
            throughput *= pktlen

        return throughput

    def get_PDR(
        self,
        txpkts: 'list',
        rxpkts: 'list'
    ) -> 'float':
        
        ''' 
            return: packet delivery ratio 
        '''

        pdr = len(rxpkts) / len(txpkts)

        return

    def get_PER(
        self,
        txpkts: 'list',
        rxpkts: 'list'
    ) -> 'float':

        ''' 
            return: packet error ratio 
        '''

        per = 1 - self.get_PDR(txpkts, rxpkts)

        return per

    def get_delay(
        self, 
        txpkt: 'dict',
        rxpkt: 'dict'
    ):

        ''' 
            return: packet delay
        '''

        delay = rxpkt['time'] - txpkt['time']
        delay = delay.total_seconds()

        return delay
