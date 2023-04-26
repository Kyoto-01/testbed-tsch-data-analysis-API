```json
{
    "mote": {
        "client": [
            mote-1, 
            ..., 
            mote-n
        ],
        "server": [
            mote-1, 
            ..., 
            mote-n
        ]
    },
    "general": {
        "addr": addr,
        "uptime": uptime,
        "peer": [
            peer-1, 
            ..., 
            peer-n
        ]
    },
    "count": {
        "packet": {
            "all": packet_count-all,
            "peer-1": packet_count-1, 
            ..., 
            "peer-n": packet_count-n
        },
        "acked": {
            "all": acked_count-all,
            "peer-1": acked_count-1, 
            ..., 
            "peer-n": acked_count-n
        },
        "txbit": {
            "all": txbit_count-all,
            "peer-1": txbit_count-1, 
            ..., 
            "peer-n": txbit_count-n
        },
        "rxbit": {
            "all": rxbit_count-all,
            "peer-1": rxbit_count-1, 
            ..., 
            "peer-n": rxbit_count-n
        },
    },
    "mean": {
        "throughput": {
            "all": mean_throughput-all,
            "peer-1": mean_throughput-1, 
            ..., 
            "peer-n": mean_throughput-n
        },
        "pdr": {
            "all": mean_pdr-all,
            "peer-1": mean_pdr-1, 
            ..., 
            "peer-n": mean_pdr-n
        },
        "per": {
            "all": mean_per-all,
            "peer-1": mean_per-1, 
            ..., 
            "peer-n": mean_per-n
        },
        "delay": {
            "all": mean_delay-all,
            "peer-1": mean_delay-1, 
            ..., 
            "peer-n": mean_delay-n
        },
        "pktlen": {
            "all": mean_pktlen-all,
            "peer-1": mean_pktlen-1,
            ...,
            "peer-n": mean_pktlen-n
        },
        "rssi": {
            "all": mean_rssi-all,
            "peer-1": mean_rssi-1, 
            ..., 
            "peer-n": mean_rssi-n
        }
    },
    "throughput": {
        "all": [throughput-1, ..., throughput-n],
        "peer-1": [throughput-1, ..., throughput-n], 
        ..., 
        "peer-n": [throughput-1, ..., throughput-n]
    },
    "pdr": {
        "all": [pdr-1, ..., pdr-n],
        "peer-1": [pdr-1, ..., pdr-n],
        ...,
        "peer-n": [pdr-1, ..., pdr-n]
    },
    "per": {
        "all": [per-1, ..., per-n],
        "peer-1": [per-1, ..., per-n],
        ...,
        "peer-n": [per-1, ..., per-n]
    },
    "delay": {
        "all": [delay-1, ..., delay-n],
        "peer-1": [delay-1, ..., delay-n],
        ...,
        "peer-n": [delay-1, ..., delay-n]
    },
    "packet": {
        "all": [packet-1, ..., packet-n],
        "peer-1": [packet-1, ..., packet-n],
        ...,
        "peer-n": [packet-1, ..., packet-n]
    },
    "acked": {
        "all": [acked-1, ..., acked-n],
        "peer-1": [acked-1, ..., acked-n],
        ...,
        "peer-n": [acked-1, ..., acked-n]
    },
    "pktlen": { 
        "all": [pktlen-1, ..., pktlen-n],
        "peer-1": [pktlen-1, ..., pktlen-n],
        ...,
        "peer-n": [pktlen-1, ..., pktlen-n]
    },
    "channel": {
        "all": [channel-1, ..., channel-n],
        "peer-1": [channel-1, ..., channel-n],
        ...,
        "peer-n": [channel-1, ..., channel-n]
    },
    "txpower": {
        "all": [txpower-1, ..., txpower-n],
        "peer-1": [txpower-1, ..., txpower-n],
        ...,
        "peer-n": [txpower-1, ..., txpower-n]
    },
    "rssi": {
        "all": [rssi-1, ..., rssi-n],
        "peer-1": [rssi-1, ..., rssi-n],
        ...,
        "peer-n": [rssi-1, ..., rssi-n]
    }
}
```