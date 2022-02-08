""" p1exporter CLI"""
from p1exporter import P1Reader, P1Collector, CRCException

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

import logging

logging.basicConfig(
    format="ts=%(asctime)s level=%(levelname)s caller=%(name)s msg=%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# TODO
# - parametrize port and USB device

if __name__ == "__main__":
    collector = P1Collector()
    REGISTRY.register(collector)
    start_http_server(8080)
    with P1Reader() as p1_reader:
        while True:
            try:
                telegram = p1_reader.read()
            except CRCException as error:
                logger.warning(error)

            logger.info(f"Got telegram with {len(telegram)} keys")
            collector.update(telegram)
