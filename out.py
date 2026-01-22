"""
Simple output control - runs in background with watchdog

Usage:
  python out.py <channel> on     - Turn output on
  python out.py <channel> off    - Turn output off
  python out.py all on           - All outputs on
  python out.py all off          - All outputs off
  python out.py status           - Show I/O status
  python out.py test             - Test all outputs
"""
import sys
import time
import threading
from pymodbus.client import ModbusTcpClient
from config import BK9000_IP, BK9000_PORT, NUM_INPUTS, NUM_OUTPUTS

outputs = [False] * NUM_OUTPUTS
running = True

def watchdog(client):
    while running:
        try:
            for i, state in enumerate(outputs):
                client.write_coil(i, state)
        except:
            pass
        time.sleep(0.05)

def main():
    global running, outputs

    if len(sys.argv) < 2:
        print(__doc__)
        return

    client = ModbusTcpClient(BK9000_IP, port=BK9000_PORT, timeout=2)
    if not client.connect():
        print("Connection failed!")
        return

    # Start watchdog
    t = threading.Thread(target=watchdog, args=(client,), daemon=True)
    t.start()

    cmd = sys.argv[1].lower()

    if cmd == "status":
        result = client.read_discrete_inputs(0, NUM_INPUTS)
        inputs = result.bits[:NUM_INPUTS] if not result.isError() else [False]*NUM_INPUTS

        print("\nINPUTS:")
        for k in range(6):
            s = k * 4
            print(f"  KL1114 #{k+1}: " + " ".join(["ON " if inputs[s+i] else "---" for i in range(4)]))

        print("\nOUTPUTS: (all off - use 'on' command to set)")

    elif cmd == "test":
        print("Testing all 20 outputs (0.5s each)...")
        for i in range(NUM_OUTPUTS):
            klemme = (i // 4) + 1
            kanal = i % 4
            print(f"  Output {i:2d} (KL2134 #{klemme}, Ch {kanal})")
            outputs[i] = True
            time.sleep(0.5)
            outputs[i] = False
        print("Done!")

    elif cmd == "all":
        if len(sys.argv) > 2 and sys.argv[2].lower() == "on":
            outputs[:] = [True] * NUM_OUTPUTS
            print("All outputs ON - holding for 10 seconds...")
            time.sleep(10)
        else:
            print("All outputs OFF")

    elif cmd.isdigit():
        ch = int(cmd)
        if len(sys.argv) > 2:
            if sys.argv[2].lower() == "on":
                outputs[ch] = True
                print(f"Output {ch} ON - holding for 10 seconds...")
                time.sleep(10)
            else:
                print(f"Output {ch} OFF")

    running = False
    time.sleep(0.1)
    client.close()

if __name__ == "__main__":
    main()
