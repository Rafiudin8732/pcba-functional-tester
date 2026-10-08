# PCBA Functional Tester

A Python GUI-based functional tester starter for controller boards using a DMM, DC PSU, and oscilloscope.

This project is designed for manufacturing-style board validation and includes:

- GUI application with instrument controls
- Swing/logic checks for controller board tests
- File-based logging for each run
- CSV/JSON result export
- Simulated instrument mode for safe startup and UI validation
- Hardware abstraction for real DMM, PSU, and oscilloscope control

## Features

- Connect to instruments from a config file
- Run a controller board functional test sequence
- Check supply voltage and rail integrity
- Capture oscilloscope waveform and estimate signal frequency
- Log all operations to disk
- Save results as CSV and JSON
- Run in simulation mode without hardware connected

## Hardware Supported

- Digital Multimeter (DMM)
- DC Power Supply Unit (PSU)
- Oscilloscope

## Requirements

- Python 3.10+
- PyQt5
- PyYAML
- PyVISA
- pandas

## Installation

```bash
git clone https://github.com/Rafiudin8732/pcba-functional-tester.git
cd pcba-functional-tester
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the GUI

```bash
python main.py
```

## Typical Workflow

1. Update `config/instrument_config.yaml` with your instrument addresses.
2. Update `config/test_config.yaml` with your board test limits.
3. Launch the app.
4. Click `Connect Instruments`.
5. Click `Run Functional Test`.
6. View pass/fail status and exported logs.

## Log Files

Logs are saved in the `logs/` folder, for example:

```text
logs/pcba_tester_YYYY-MM-DD.log
```

## Example Config

```yaml
dmm:
  resource: "USB0::0x0957::0x1A07::MY12345678::INSTR"
  simulated: true

psu:
  resource: "USB0::0x1AB1::0x0588::P123456::INSTR"
  simulated: true

oscilloscope:
  resource: "TCPIP0::192.168.0.10::inst0::INSTR"
  simulated: true
```

## License

MIT
