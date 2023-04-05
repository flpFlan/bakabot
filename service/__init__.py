import logging
from service.base import Service

all_services: set[Service] = set()

log = logging.getLogger("Service")
