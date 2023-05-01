from ..controller import Controller
from lib.data_analysis_entity import TestbedAnalysisEntity


class RPCAnalysisController(Controller):

    def __init__(
        self,
        request: 'dict'
    ):
        self._analysisEntity: 'TestbedAnalysisEntity' = None

        super().__init__(request)

    def _setup_controller(self):
        ret = super()._setup_controller()

        if ret:
            self._analysisEntity = TestbedAnalysisEntity(self._testbed)

        return ret

    def _check_req_parameters_key(self) -> 'bool':
        res = super()._check_req_parameters_key()

        if res:
            try:
                __ = self._request['tx_offset']
            except KeyError as ke:
                res = False

        return res

    def _check_req_parameters_value_type(self) -> 'bool':
        res = super()._check_req_parameters_value_type()

        res = res and self._check_txoffset_value_type()

        return res

    def _check_txoffset_value_type(self):
        res = isinstance(self._request['tx_offset'], dict)

        if res:
            for i in self._request['tx_offset'].values():
                res = res and isinstance(i, dict)
                if res:
                    for j in i.values():
                        res = res and isinstance(j, int)
                        if not res:
                            break
                else:
                    break

        return res

    def update_analysis_all(self):
        self._response = self._check_req_parameters_errors()

        if not self._response:
            self._response = {
                'analyze_clients_throughput': \
                    self._analysisEntity.analyze_clients_throughput(),
                'analyze_servers_throughput': \
                    self._analysisEntity.analyze_servers_throughput(),
                'analyze_clients_pdr': \
                    self._analysisEntity.analyze_clients_pdr(),
                'analyze_clients_per': \
                    self._analysisEntity.analyze_clients_per(),
                'analyze_clients_delay': \
                    self._analysisEntity.analyze_clients_delay(
                        txpktOffsets=self._request['tx_offset']
                    )
            }

        return self._response
