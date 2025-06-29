import serial
import threading
import time

class SerialReader:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.data = []
        self.running = False
        self.connected = False
        self.last_received_time = None

    def start(self):
        self.running = True
        threading.Thread(target=self.read_loop, daemon=True).start()

    def read_loop(self):
        try:
            with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
                self.connected = True
                while self.running:
                    line = ser.readline().decode("utf-8").strip()
                    if line:
                        try:
                            h, t = map(float, line.split(","))
                            self.data.append({"time": time.time(), "humidity": h, "temperature": t})
                            self.last_received_time = time.time()
                        except ValueError:
                            pass
        except serial.SerialException as e:
            print(f"Serial error: {e}")
            self.connected = False
