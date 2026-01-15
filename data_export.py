import json
from datetime import datetime
import os


class DataExport:
    
    def __init__(self, export_folder="exports"):

        self.export_folder = export_folder

        if not os.path.exists(export_folder):
            os.makedirs(export_folder)
    
    def export_to_json(self, data, filename=None):

        try:
            # genereer bestandsnaam als niet opgegeven
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"smarthome_export_{timestamp}"

            if not filename.endswith(".json"):
                filename += ".json"
            
            # volledig pad
            filepath = os.path.join(self.export_folder, filename)
            
            # voeg metadata toe aan de export
            export_data = {
                "export_info": {
                    "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "application": "SmartHome Dashboard"
                },
                "data": data
            }
            # schrijf naar bestand

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False, default=str)
            
            print(f"Data geëxporteerd naar: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Fout bij exporteren naar JSON: {e}")
            return None


if __name__ == "__main__":
    print("=== Data Export Module Test ===\n")
    
    exporter = DataExport()
    
    test_data = {
        "weather": {"temperature": 18.5, "humidity": 65},
        "devices": {"Lamp": True, "Sensor": False}
    }
    
    filepath = exporter.export_to_json(test_data, "test_export")
    
    if filepath:
        print(f"Test bestand aangemaakt: {filepath}")
    
    print("\n=== Test voltooid ===")
