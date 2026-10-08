from __future__ import annotations

import random
from datetime import datetime
from typing import Dict, Any

from src.instruments.dmm import DMM
from src.instruments.psu import PSU
from src.instruments.oscilloscope import Oscilloscope


class FunctionalTestManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def run_controller_board_test(self, dmm: DMM, psu: PSU, osc: Oscilloscope) -> Dict[str, Any]:
        voltage_config = self.config["board"]["supply_voltage"]
        tolerance = self.config["board"]["voltage_tolerance"]
        expected_frequency = self.config["board"]["expected_clock_frequency"]
        freq_tolerance = self.config["board"]["frequency_tolerance"]

        psu.set_voltage(voltage_config)
        rail_voltage = dmm.measure_voltage("VCC")
        current = psu.measure_current()
        waveform = osc.capture_waveform()
        frequency = waveform["frequency_hz"]

        voltage_ok = abs(rail_voltage - voltage_config) <= tolerance
        current_ok = current <= self.config["board"]["max_current"]
        frequency_ok = abs(frequency - expected_frequency) <= expected_frequency * freq_tolerance

        result = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "board": self.config["board"]["name"],
            "rail_voltage_v": rail_voltage,
            "supply_voltage_v": voltage_config,
            "current_a": current,
            "signal_frequency_hz": frequency,
            "expected_frequency_hz": expected_frequency,
            "status": "PASS" if all([voltage_ok, current_ok, frequency_ok]) else "FAIL",
            "details": {
                "rail_voltage_ok": voltage_ok,
                "current_ok": current_ok,
                "frequency_ok": frequency_ok,
            },
        }

        return result
