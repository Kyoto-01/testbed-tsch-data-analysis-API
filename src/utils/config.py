from argparse import ArgumentParser


def config_from_cmdline():
    config = {}

    parser = ArgumentParser()
    parser.add_argument('-a', '--addr', type=str, default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, default=5000)

    args = parser.parse_args()
    config['addr'] = args.addr
    config['port'] = args.port

    return config
