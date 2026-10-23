#!/usr/bin/env python3
"""RPLIDAR icin dogru baud'u bulmak icin taranan hizlarda a5 5a sync baytini arar."""
import serial
import time

PORT = "/dev/ttyUSB0"
BAUDS = [9600, 19200, 57600, 115200, 128000, 230400, 256000, 460800, 921600, 1000000]

for baud in BAUDS:
    try:
        ser = serial.Serial(PORT, baud, timeout=1.5)
        ser.reset_input_buffer()
        time.sleep(0.3)
        data = ser.read(500)
        ser.close()
        has_sync = b'\xa5\x5a' in data
        nonzero = len(data) - data.count(0)
        print(f"baud={baud:8d}  bayt_sayisi={len(data):4d}  a5-5a_sync={'EVET!' if has_sync else 'hayir':6s}  ornek={data[:16].hex()}")
    except Exception as e:
        print(f"baud={baud:8d}  HATA: {e}")
