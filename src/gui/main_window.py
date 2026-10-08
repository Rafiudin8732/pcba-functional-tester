from __future__ import annotations

import os
from typing import Any, Dict

import yaml
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.instruments.dmm import DMM
from src.instruments.psu import PSU
from src.instruments.oscilloscope import Oscilloscope
from src.tests.test_manager import FunctionalTestManager
from src.utils.data_export import export_results
from src.utils.logger import setup_logger


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PCBA Functional Tester")
        self.resize(1000, 700)

        self.logger = setup_logger()
        self.config = self._load_yaml("config/instrument_config.yaml")
        self.test_config = self._load_yaml("config/test_config.yaml")

        self.dmm = DMM(self.config["dmm"]["resource"], self.config["dmm"].get("simulated", True))
        self.psu = PSU(self.config["psu"]["resource"], self.config["psu"].get("simulated", True))
        self.scope = Oscilloscope(self.config["oscilloscope"]["resource"], self.config["oscilloscope"].get("simulated", True))
        self.test_manager = FunctionalTestManager(self.test_config)
        self.results = []

        self._build_ui()
        self._update_status("Ready")

    def _load_yaml(self, path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as yaml_file:
            return yaml.safe_load(yaml_file) or {}

    def _build_ui(self):
        central = QWidget()
        main_layout = QVBoxLayout()

        controls = QGroupBox("Instrument Controls")
        controls_layout = QHBoxLayout()

        self.connect_button = QPushButton("Connect Instruments")
        self.run_button = QPushButton("Run Functional Test")
        self.export_button = QPushButton("Export Results")
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("font-weight: bold; color: #2E7D32;")

        controls_layout.addWidget(self.connect_button)
        controls_layout.addWidget(self.run_button)
        controls_layout.addWidget(self.export_button)
        controls_layout.addWidget(self.status_label)
        controls.setLayout(controls_layout)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setPlaceholderText("Test log output will appear here...")

        self.connect_button.clicked.connect(self.connect_instruments)
        self.run_button.clicked.connect(self.run_functional_test)
        self.export_button.clicked.connect(self.export_results)

        info = QGroupBox("Board Information")
        info_layout = QFormLayout()
        self.board_name_input = QLineEdit(self.test_config.get("board", {}).get("name", "Controller Board"))
        self.voltage_input = QLineEdit(str(self.test_config.get("board", {}).get("supply_voltage", 12.0)))
        self.current_limit_input = QLineEdit(str(self.test_config.get("board", {}).get("max_current", 0.6)))

        info_layout.addRow("Board Name:", self.board_name_input)
        info_layout.addRow("Supply Voltage (V):", self.voltage_input)
        info_layout.addRow("Current Limit (A):", self.current_limit_input)
        info.setLayout(info_layout)

        main_layout.addWidget(controls)
        main_layout.addWidget(info)
        main_layout.addWidget(self.log_view)
        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def _update_status(self, message: str, is_error: bool = False):
        self.status_label.setText(message)
        color = "#D32F2F" if is_error else "#2E7D32"
        self.status_label.setStyleSheet(f"font-weight: bold; color: {color};")

    def append_log(self, message: str):
        self.log_view.append(message)
        self.logger.info(message)

    def connect_instruments(self):
        try:
            self.dmm.connect()
            self.psu.connect()
            self.scope.connect()
            self.append_log("Connected to DMM, PSU, and oscilloscope.")
            self._update_status("Connected")
        except Exception as exc:  # pragma: no cover
            self.append_log(f"Connection failed: {exc}")
            self._update_status("Connection failed", True)
            QMessageBox.critical(self, "Connection Error", str(exc))

    def run_functional_test(self):
        try:
            if not all([self.dmm.is_connected(), self.psu.is_connected(), self.scope.is_connected()]):
                self.append_log("Not all instruments are connected. Connecting automatically...")
                self.connect_instruments()

            self.append_log("Starting controller board functional test...")
            result = self.test_manager.run_controller_board_test(self.dmm, self.psu, self.scope)
            self.results.append(result)
            self.append_log(
                "Test result: "
                f"{result['status']} | Rail={result['rail_voltage_v']} V | "
                f"Current={result['current_a']} A | Frequency={result['signal_frequency_hz']} Hz"
            )
            self._update_status(result["status"])

        except Exception as exc:
            self.append_log(f"Test error: {exc}")
            self._update_status("Test failed", True)
            QMessageBox.critical(self, "Test Error", str(exc))

    def export_results(self):
        if not self.results:
            QMessageBox.information(self, "No Data", "There are no test results to export yet.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Test Results", "pcba_test_results", "CSV Files (*.csv);;JSON Files (*.json)")
        if not file_name:
            return

        export_path = file_name.rsplit(".", 1)[0] if "." in file_name else file_name
        paths = export_results(self.results, export_path)
        self.append_log(f"Results exported to: {paths['csv']} and {paths['json']}")
        QMessageBox.information(self, "Export Complete", f"Results saved to:\n{paths['csv']}\n{paths['json']}")
