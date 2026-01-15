# main.py
import tkinter as tk
from tkinter import messagebox
from pico_widget import PicoMonitorWidget
from database_module import DatabaseModule
from data_export import DataExport

class SmartHomeDashboard:
    def __init__(self):
        # Hoofdvenster
        self.root = tk.Tk()
        self.root.title("SmartHome Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Modules
        self.database_module = DatabaseModule()
        self.data_export = DataExport()
        self.current_weather_data = None

        # UI
        self.create_header()
        self.create_main_content()
        self.load_initial_data()

    def create_header(self):
        frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        frame.pack(fill=tk.X)
        frame.pack_propagate(False)
        tk.Label(
            frame,
            text="SmartHome Dashboard",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=20)

    def create_main_content(self):
        main = tk.Frame(self.root, bg="#f0f0f0")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        left = tk.Frame(main, bg="#f0f0f0")
        left.pack(side=tk.LEFT, fill=tk.Y)

        middle = tk.Frame(main, bg="#f0f0f0")
        middle.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15)

        right = tk.Frame(main, bg="#f0f0f0")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Pico Widget ---
        self.pico_widget = PicoMonitorWidget(left)
        self.pico_widget.pack(fill=tk.X)

        # --- Apparaten sectie ---
        self.create_devices_section(middle)
        # --- Acties sectie ---
        self.create_actions_section(right)

    def create_devices_section(self, parent):
        frame = tk.LabelFrame(
            parent,
            text="Smart Home Apparaten",
            font=("Arial", 14, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
        frame.pack(fill=tk.BOTH, expand=True)

        self.devices = {
            "Woonkamer Lamp": tk.BooleanVar(value=True),
            "Thermostaat": tk.BooleanVar(value=True),
            "Voordeur Sensor": tk.BooleanVar(value=False)
        }

        for name, var in self.devices.items():
            tk.Checkbutton(
                frame,
                text=name,
                variable=var,
                bg="white"
            ).pack(anchor=tk.W)

        tk.Button(
            frame,
            text="Opslaan naar Database",
            bg="#9b59b6",
            fg="white",
            command=self.save_devices_to_database
        ).pack(pady=10)

    def create_actions_section(self, parent):
        frame = tk.LabelFrame(
            parent,
            text="Acties",
            font=("Arial", 14, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Button(
            frame,
            text="Exporteer Data",
            width=25,
            bg="#e74c3c",
            fg="white",
            command=self.export_data
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Test Database",
            width=25,
            bg="#f39c12",
            fg="white",
            command=self.test_database_connection
        ).pack(pady=10)

        self.status_label = tk.Label(
            frame,
            text="Status: Gereed",
            bg="white",
            fg="#7f8c8d"
        )
        self.status_label.pack(pady=20)

    def save_devices_to_database(self):
        if self.database_module.save_device_status(
            {k: v.get() for k, v in self.devices.items()}
        ):
            messagebox.showinfo("Succes", "Opgeslagen in database")

    def export_data(self):
        self.data_export.export_to_json({
            "pico_moisture": self.pico_widget.moisture_value.cget("text"),
            "pico_prediction": self.pico_widget.tomorrow_value.cget("text"),
            "devices": {k: v.get() for k, v in self.devices.items()}
        })

    def test_database_connection(self):
        ok = self.database_module.test_connection()
        messagebox.showinfo("Database", "Verbinding OK" if ok else "Verbinding mislukt")

    def update_status(self, msg):
        self.status_label.config(text=f"Status: {msg}")
        self.root.update()

    def load_initial_data(self):
        self.update_status("Dashboard geladen")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    SmartHomeDashboard().run()
