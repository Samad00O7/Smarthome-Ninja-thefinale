# pico_widget.py
import tkinter as tk
from tkinter import font
import json
import serial
import serial.tools.list_ports
import numpy as np


class PicoMonitorWidget(tk.Frame):
    """
    Simpele widget voor Pico sensor: toont vochtigheid en voorspelling voor morgen.
    """

    def __init__(self, parent, serial_port=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg="#34495e")

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=10, weight="bold")
        self.value_font = font.Font(family="Helvetica", size=16, weight="bold")

        # Labels
        tk.Label(self, text="Moisture", font=self.title_font, fg="#3498db", bg="#34495e").grid(row=0, column=0,
                                                                                               sticky="w", padx=10,
                                                                                               pady=(10, 0))
        self.moisture_value = tk.Label(self, text="--", font=self.value_font, fg="white", bg="#34495e")
        self.moisture_value.grid(row=1, column=0, sticky="w", padx=10)
        tk.Label(self, text="%", font=("Helvetica", 9), fg="#95a5a6", bg="#34495e").grid(row=1, column=1, sticky="w")

        self.tomorrow_label = tk.Label(self, text="Vochtigheid morgen: --%", font=self.value_font, fg="white",
                                       bg="#34495e")
        self.tomorrow_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 10))

        # Serial
        self.ser = None
        self.serial_port = serial_port or self.find_pico_port()
        self.update_loop()  # start update loop

        # Houd historische vochtigheid bij (voorbeeld)
        self.moisture_history = []

    def find_pico_port(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if 'VID:PID=2E8A' in port.hwid:
                return port.device
        return None

    def update_loop(self):
        if self.serial_port:
            try:
                if self.ser is None or not self.ser.is_open:
                    self.ser = serial.Serial(self.serial_port, 115200, timeout=1)

                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line:
                        data = json.loads(line)
                        self.update_view(data)
            except:
                pass
        else:
            self.moisture_value.config(text="N/A")

        self.after(500, self.update_loop)

    def update_view(self, data):
        moisture = data.get('moisture_percent')
        if moisture is not None:
            self.moisture_value.config(text=f"{moisture:.1f}")
            self.moisture_history.append(moisture)
            if len(self.moisture_history) > 30:  # max 30 dagen/historie
                self.moisture_history.pop(0)

            predicted = self.predict_moisture_tomorrow(self.moisture_history)
            if predicted is not None:
                self.tomorrow_label.config(text=f"Vochtigheid morgen: {predicted}%")

    def predict_moisture_tomorrow(self, history):
        if len(history) < 2:
            return None
        x = np.arange(len(history))
        y = np.array(history)
        a, b = np.polyfit(x, y, 1)
        return round(a * (len(history)) + b, 1)

    def on_close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
