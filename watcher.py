"""
BK9000 Watcher - Monitors connection and auto-disables watchdog after reboot

Run this permanently (e.g., as Windows service or startup script).
It will detect when BK9000 comes online and disable the watchdog automatically.
"""
import time
from pymodbus.client import ModbusTcpClient
from config import BK9000_IP, BK9000_PORT

CHECK_INTERVAL = 5  # seconds between checks

def check_and_fix():
    """Check BK9000 and disable watchdog if needed. Returns status string."""
    try:
        client = ModbusTcpClient(BK9000_IP, port=BK9000_PORT, timeout=2)
        if not client.connect():
            return "offline"

        # Check watchdog status
        r = client.read_holding_registers(0x1122, count=1)
        if r.isError():
            client.close()
            return "error"

        watchdog_mode = r.registers[0]

        if watchdog_mode != 2:
            # Watchdog is enabled - disable it!
            client.write_register(0x1120, 0)
            client.write_register(0x1122, 2)
            client.close()
            return "fixed"
        else:
            client.close()
            return "ok"

    except Exception as e:
        return f"error: {e}"


def main():
    print("BK9000 Watcher")
    print("=" * 40)
    print(f"Monitoring {BK9000_IP} every {CHECK_INTERVAL}s")
    print("Press Ctrl+C to stop")
    print()

    last_status = None

    try:
        while True:
            status = check_and_fix()

            # Only print on status change
            if status != last_status:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                if status == "offline":
                    print(f"[{timestamp}] BK9000 OFFLINE - waiting...")
                elif status == "fixed":
                    print(f"[{timestamp}] BK9000 ONLINE - Watchdog DISABLED!")
                elif status == "ok":
                    print(f"[{timestamp}] BK9000 OK - Watchdog already disabled")
                else:
                    print(f"[{timestamp}] {status}")

                last_status = status

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
