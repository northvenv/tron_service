from tronpy import AsyncTron


def get_tron_client():
    return AsyncTron(network="nile")