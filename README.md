# Testbed TSCH Data Analysis API

API para fornecimento de relatórios do testbed e chamada remota de procedimentos de análise dos dados do mesmo.

## 1. Execução da API

Em ```testbed-tsch-data-analysis-API/src``` execute:

```
./main.py [-a | --addr <addr>] [-p | --port <port>]
```

* **-a | --addr**: Endereço no qual a API vai receber requisições.
* **-p | --port**: Porta na qual a API vai receber requisições.

## 2. Consumo da API

Os recursos da API são consumidos ao acessar uma URI fornecida pela mesma. O corpo da solicitação deve ser um JSON contendo parâmetros específicos para cada tipo de recurso. A resposta retornada pelos recursos do tipo RPC também são no formato JSON e contém o retorno de cada função executada.

### 2.1. URIs

Abaixo, uma lista das URIs fornecidas pela API.

#### 2.1.1. URIs de relatórios

* **/api/report/client**: Relatório de um cliente do testbed.
* **/api/report/server**: Relatório de um servidor do testbed.
* **/api/report/general**: Relatório geral dos motes do testbed.

#### 2.1.2. URIs de RPCs

* **/rpc/analysis/update/all**: Calcula e grava no banco de dados métricas de taxa de transferência, PDR, PER e latência dos motes do testbed.

### 2.2. Corpo das requisições

O corpo das requisições é um JSON contendo parâmetros específicos. Abaixo são listados os parâmetros que devem estar contidos no corpo das requisições de cada tipo de recurso.

#### 2.2.1. Relatórios

Os parâmetros a seguir servem para todos os recursos do tipo relatório:

* **testbed_name**: Nome do testbed para o qual se deseja gerar um relatório.

* **mote_addr**: Endereço do mote (pertencente ao testbed) para o qual se deseja gerar um relatório (Este parâmetro é opcional para o recurso ```/api/report/general```, pois não tem nenhum efeito).

* **topics**: Lista de tópicos que devem estar presentes no relatório. Todos os tópicos e subtópicos que podem ser passados para essa lista são informados [aqui](src/lib/testbed_analysis/docs/data_report/report_topics.md).

Exemplo: 

```json
{
    "testbed_name": "testbed-71d1877d-356a-4757-9793-724c54c91bdf",
    "mote_addr": "fe8000000000000002124b0014b5d33a",
    "topics": ["count/packet/", "mean", "allmean", "raw/pdr/", "general/uptime/", "testbed"]
}
```

#### 2.2.2. RPCs

Os parâmetros a seguir são utilizados pelo recurso ```/rpc/analysis/update/all```:

* **testbed_name**: Nome do testbed no qual se deseja executar uma função.

* **tx_offset**: Índice a partir do qual se deseja utilizar os dados transmitidos para realização dos cálculos de análise de dados. Esse parâmetro é um dicionário que contém outros dicionários, cada um relacionado a um cliente do testbed e contendo os índices (tx_offsets) de pacotes transmitidos para cada par (servidor). O valor desse parâmetro pode ser um dicionário vazio, dessa forma todos os pacotes transmitidos serão utilizados para os cálculos de análise de dados.

Exemplo 1: 

```json
    "testbed_name": "testbed-71d1877d-356a-4757-9793-724c54c91bdf",
    "tx_offset": {
        "fe8000000000000002124b0014b5d33a": {
            "fd0000000000000002124b0018e0b9f2": 3828
        }
    }
```

Exemplo 2:

```json
    "testbed_name": "testbed-71d1877d-356a-4757-9793-724c54c91bdf",
    "tx_offset": {}
```

### 2.3. Retorno dos RPCs

A resposta retornada pelos recursos do tipo RPC são no formato JSON e contém o retorno de cada função executada.

#### 2.3.1. /rpc/analysis/update/all

Executa e retorna os retornos de todas as funções de análise de dados disponibilizadas pela API.

Exemplo:

```json
{
    "analyze_clients_delay": {
        "fe8000000000000002124b0014b5d33a": {
            "fd0000000000000002124b0018e0b9f2": 3828
        }
    },
    "analyze_clients_pdr": true,
    "analyze_clients_per": true,
    "analyze_clients_throughput": true,
    "analyze_servers_throughput": true
}
```

**OBS**.: O valor do campo *analyze_clients_delay* pode ser utilizado pelo parâmetro *tx_offset* da requisição do RPC `/rpc/analysis/update/all`.