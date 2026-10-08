from __future__ import annotations

import random

from src.instruments.base import BaseInstrument


class DMM(BaseInstrument):
    def __init__(self, resource: str, simulated: bool = True):
        super().__init__("DMM", resource, simulated)

    def measure_voltage(self, channel: str = "VCC") -> float:
        self._require_connection()
        if self.simulated:
            base = 12.0 if channel == "VCC" else 5.0
            return round(base + random.uniform(-0.05, 0.05), 4)
        return 0.0

    def measure_resistance(self, channel: str = "GND") -> float:
        self._require_connection()
        if self.simulated:
            return round(100.0 + random.uniform(-10, 10), 2)
        return 0.0
