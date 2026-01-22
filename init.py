"""
BK9000 Initialization - Disables watchdog after power-on

Run this once after BK9000 boots, before using outputs.
Or use the web interface at http://10.0.0.7 to save permanently.
"""
from pymodbus.client import ModbusTcpClient
from config import BK9000_IP, BK9000_PORT

def disable_watchdog():
    client = ModbusTcpClient(BK9000_IP, port=BK9000_PORT, timeout=3)
    if not client.connect():
        print("Connection failed!")
        return False

    print(f"Connected to BK9000 at {BK9000_IP}")

    # Read current values
    r1 = client.read_holding_registers(0x1120, count=1)
    r2 = client.read_holding_registers(0x1122, count=1)

    timeout_val = r1.registers[0] if not r1.isError() else "error"
    mode_val = r2.registers[0] if not r2.isError() else "error"

    print(f"Current: Timeout=0x1120={timeout_val}, Mode=0x1122={mode_val}")

    if mode_val == 2:
        print("Watchdog already disabled!")
        client.close()
        return True

    # Disable watchdog
    print("Disabling watchdog...")
    client.write_register(0x1120, 0)      # Timeout = 0
    client.write_register(0x1122, 2)      # Mode = Disabled

    # Verify
    r2 = client.read_holding_registers(0x1122, count=1)
    if not r2.isError() and r2.registers[0] == 2:
        print("Watchdog DISABLED!")
        print()
        print("NOTE: This setting is lost after power cycle.")
        print("      Use web interface http://10.0.0.7 to save permanently.")
        client.close()
        return True
    else:
        print("Failed to disable watchdog!")
        client.close()
        return False

if __name__ == "__main__":
    disable_watchdog()
