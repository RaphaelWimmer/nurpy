#!/usr/bin/env python3

# simple script to read a single tag and report ID and RSSI

import serial
import sys
import time
import binascii


# Windows: "COM1"
DEV = "/dev/ttyACM0"
TIMEOUT = 500  # ms

CMD_SCAN = b"\xa5\x05\x00\x00\x00\x5F\x30\xF4\x01\x1d\xc6"  # Simple Scan, see NUR protocol 8.1
# we build this command below from its individual parts

CMD_HEADER = b"\xa5\x05\x00\x00\x00\x5F"  # see NUR protocol 3.1
CMD_SCAN_SINGLE_TAG = b"\x30"  # see NUR protocol 8.1


def crc16_init():
    CRC16_POLYNOMIAL = 0x1021
    crc16table = []
    for i in range(256):
        c = i << 8
        for j in range(8):
            if c & 0x8000:
                c = CRC16_POLYNOMIAL ^ (c << 1)
            else:
                c = c << 1
        crc16table.append(c)
    return crc16table


def crc16(bytestring, table):
    CRC16_START = 0xFFFF
    crc = CRC16_START
    for i in bytestring:
        # print(hex(i), hex((crc >> 8) ^ i))
        crc = (crc << 8) ^ table[(crc >> 8) ^ i]
        crc = crc & 0xffff  # truncate to 16 bit
    return crc


def print_data(d):
    if len(d) == 10:  # error (FIXME)
        print("_", end="")
    else:
        print("")
        rssi = d[9]
        rssi_s = d[10]
        epc = d[11:-2]
        print(f"RSSI: {rssi - 256} dBm ({rssi_s}%)")
        print("Code: " + str(binascii.hexlify(epc)))
        print("")


# assemble command
# in the following: suffix _b for bytes
timeout_b = bytes([TIMEOUT % 256, TIMEOUT >> 8])  # little-endian
crctable = crc16_init()
payload_b = CMD_SCAN_SINGLE_TAG + timeout_b
checksum = crc16(payload_b, crctable)
checksum_b = bytes([checksum % 256, checksum >> 8])  # little-endian
command_b = CMD_HEADER + payload_b + checksum_b

# for a timeout of 500 ms, our assembled command should be the same as the predefined one here
# if you change the timeout, also comment out the following line
assert command_b == CMD_SCAN

if len(sys.argv) > 1:
    DEV = sys.argv[1]

s = serial.Serial(DEV, 115200)

while True:
    s.write(CMD_SCAN)
    print(".", end="")
    time.sleep(0.5)
    r = s.read_all()
    if len(r) > 0:
        print_data(r)
