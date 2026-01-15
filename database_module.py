try:
    import psycopg2

    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    print("WAARSCHUWING: psycopg2 niet geïnstalleerd!")
    print("Installeer met: pip install psycopg2-binary")


class DatabaseModule:
    """
    class voor het beheren van de PostgreSQL database verbinding.
    """

    def __init__(self):

        self.db_config = {
            "host": "smarthome-db-server.postgres.database.azure.com",
            "database": "smarthome_db",
            "user": "smarthome_admin",
            "password": "zH_j4:7V?x.fuW*",
            "port": "5432",
            "sslmode": "require"
        }

        self.connection = None

    def connect(self):
        if not PSYCOPG2_AVAILABLE:
            print("psycopg2 is niet beschikbaar!")
            return False

        try:
            self.connection = psycopg2.connect(
                host=self.db_config["host"],
                database=self.db_config["database"],
                user=self.db_config["user"],
                password=self.db_config["password"],
                port=self.db_config["port"],
                sslmode=self.db_config["sslmode"]
            )
            print("Verbinding met database succesvol!")
            return True

        except Exception as e:
            print(f"Fout bij verbinden met database: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def test_connection(self):
        if not PSYCOPG2_AVAILABLE:
            return False

        try:
            if self.connect():
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
                self.disconnect()
                return True
            return False

        except Exception as e:
            print(f"Database test mislukt: {e}")
            return False

    def create_tables(self):
        if not self.connect():
            return False

        try:
            cursor = self.connection.cursor()

            # tabel voor apparaatstatus
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS device_status (
                    id SERIAL PRIMARY KEY,
                    device_name VARCHAR(100) UNIQUE NOT NULL,
                    is_active BOOLEAN DEFAULT FALSE,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.connection.commit()
            cursor.close()
            print("Tabellen succesvol aangemaakt!")
            return True

        except Exception as e:
            print(f"Fout bij aanmaken tabellen: {e}")
            return False

        finally:
            self.disconnect()

    def save_device_status(self, devices):

        if not PSYCOPG2_AVAILABLE:
            print("Database niet beschikbaar - data wordt niet opgeslagen")
            return False

        if not self.connect():
            return False

        try:
            cursor = self.connection.cursor()

            for device_name, is_active in devices.items():
                # check of apparaat al bestaat
                cursor.execute(
                    "SELECT id FROM device_status WHERE device_name = %s",
                    (device_name,)
                )
                result = cursor.fetchone()

                if result:
                    # update bestaand apparaat
                    cursor.execute(
                        """
                        UPDATE device_status 
                        SET is_active = %s, last_updated = CURRENT_TIMESTAMP
                        WHERE device_name = %s
                        """,
                        (is_active, device_name)
                    )
                else:
                    # voeg nieuw apparaat toe
                    cursor.execute(
                        """
                        INSERT INTO device_status (device_name, is_active)
                        VALUES (%s, %s)
                        """,
                        (device_name, is_active)
                    )

            self.connection.commit()
            cursor.close()
            return True

        except Exception as e:
            print(f"Fout bij opslaan apparaatstatus: {e}")
            return False

        finally:
            self.disconnect()

    def get_all_device_status(self):
        if not PSYCOPG2_AVAILABLE:
            return []

        if not self.connect():
            return []

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT device_name, is_active, last_updated 
                FROM device_status 
                ORDER BY device_name
                """
            )
            results = cursor.fetchall()
            cursor.close()

            # format de resultaten
            devices = []
            for row in results:
                status = "AAN" if row[1] else "UIT"
                devices.append(f"{row[0]}: {status}")

            return devices

        except Exception as e:
            print(f"Fout bij ophalen apparaatstatus: {e}")
            return []

        finally:
            self.disconnect()


if __name__ == "__main__":
    print("=== Database Module Test ===\n")

    db = DatabaseModule()

    print("Database verbinding testen...")
    if db.test_connection():
        print("Verbinding succesvol!")
    else:
        print("Verbinding mislukt - controleer de credentials")

    print("\n=== Test voltooid ===")