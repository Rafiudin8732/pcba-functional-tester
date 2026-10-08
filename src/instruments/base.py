from __future__ import annotations

import logging
from typing import Any


class BaseInstrument:
    def __init__(self, name: str, resource: str, simulated: bool = True):
        self.name = name
        self.resource = resource
        self.simulated = simulated
        self.connected = False
        self.logger = logging.getLogger("pcba_tester")

    def connect(self) -> bool:
        if self.simulated:
            self.connected = True
            self.logger.info("%s connected in simulated mode", self.name)
            return True
        self.logger.warning("%s real hardware connection is not configured in this starter project", self.name)
        return False

    def disconnect(self) -> None:
        self.connected = False
        self.logger.info("%s disconnected", self.name)

    def is_connected(self) -> bool:
        return self.connected

    def _require_connection(self) -> None:
        if not self.connected:
            raise RuntimeError(f"{self.name} is not connected")

    def measure(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
