from __future__ import annotations

import random

from src.instruments.base import BaseInstrument


class PSU(BaseInstrument):
    def __init__(self, resource: str, simulated: bool = True):
        super().__init__("PSU", resource, simulated)

    def set_voltage(self, voltage: float) -> float:
        self._require_connection()
        if self.simulated:
            self.last_voltage = voltage
            return float(voltage)
        return float(voltage)

    def measure_output(self) -> float:
        self._require_connection()
        if self.simulated:
            return round(12.0 + random.uniform(-0.08, 0.08), 4)
        return 0.0

    def measure_current(self) -> float:
        self._require_connection()
        if self.simulated:
            return round(0.28 + random.uniform(-0.05, 0.05), 4)
        return 0.0
