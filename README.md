# Nordic ID's Universal RFID (NUR) tools in Python

Accessing Nordic ID's RFID readers via USB CDC (serial connection).
The tools in this repository do not require the [NUR SDK](https://github.com/NordicID/nur_sdk) but directly implement the NUR API.

Currently, only a single tool is available:

- `scan_tag.py` looks for a single tag within the reader's range and prints EPC (electronic product code) and RSSI (signal strength)

Tested with [Nordic ID Stix](https://www.nordicid.com/device/nordic-id-stix/).

See also:

- [driver-rain-py-nurapi](https://github.com/kliskatek/driver-rain-py-nurapi) - Python module that wraps precompiled NUR API libraries for Windows and Linux
