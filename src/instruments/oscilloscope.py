from __future__ import annotations

import random

from src.instruments.base import BaseInstrument


class Oscilloscope(BaseInstrument):
    def __init__(self, resource: str, simulated: bool = True):
        super().__init__("Oscilloscope", resource, simulated)

    def capture_waveform(self) -> dict:
        self._require_connection()
        if self.simulated:
            freq = 1000000 + random.uniform(-50000, 50000)
            return {
                "frequency_hz": round(freq, 2),
                "amplitude_v": round(3.3 + random.uniform(-0.2, 0.2), 4),
                "waveform": [0.0, 1.0, 2.0, 3.0, 2.0, 1.0, 0.0],
            }
        return {"frequency_hz": 0.0, "amplitude_v": 0.0, "waveform": []}
