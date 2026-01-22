"""
BK9000 Daemon - runs permanently, never loses connection

Reads commands from commands.txt:
  on 0        - Output 0 on
  off 0       - Output 0 off
  on 0,1,2,3  - Multiple outputs on
  all on      - All on
  all off     - All off

Start: python daemon.py
Send commands: echo "on 0" > commands.txt
"""
import os
import threading
import time
from pymodbus.client import ModbusTcpClient
from config import BK9000_IP, BK9000_PORT, NUM_INPUTS, NUM_OUTPUTS

COMMAND_FILE = "commands.txt"

outputs = [False] * NUM_OUTPUTS
inputs = [False] * NUM_INPUTS
client = None
connected = False


def watchdog_loop():
    """Continuously write outputs to keep them alive"""
    global connected
    while True:
        try:
            if connected and client:
                for i, state in enumerate(outputs):
                    client.write_coil(i, state)
        except Exception as e:
            print(f"Watchdog error: {e}")
            connected = False
        time.sleep(0.05)


def read_inputs_loop():
    """Periodically read inputs"""
    global inputs
    while True:
        try:
            if connected and client:
                result = client.read_discrete_inputs(0, NUM_INPUTS)
                if not result.isError():
                    inputs = result.bits[:NUM_INPUTS]
        except:
            pass
        time.sleep(0.2)


def process_command(cmd):
    """Process a single command"""
    global outputs
    cmd = cmd.strip().lower()
    if not cmd:
        return

    print(f"Command: {cmd}")

    if cmd == "all on":
        outputs[:] = [True] * NUM_OUTPUTS
        print("  -> All outputs ON")

    elif cmd == "all off":
        outputs[:] = [False] * NUM_OUTPUTS
        print("  -> All outputs OFF")

    elif cmd == "status":
        print(f"  Inputs:  {['ON' if i else '---' for i in inputs]}")
        print(f"  Outputs: {['ON' if o else '---' for o in outputs]}")

    elif cmd.startswith("on "):
        try:
            channels = [int(x.strip()) for x in cmd[3:].split(",")]
            for ch in channels:
                if 0 <= ch < NUM_OUTPUTS:
                    outputs[ch] = True
            print(f"  -> Outputs {channels} ON")
        except:
            print("  -> Error parsing command")

    elif cmd.startswith("off "):
        try:
            channels = [int(x.strip()) for x in cmd[4:].split(",")]
            for ch in channels:
                if 0 <= ch < NUM_OUTPUTS:
                    outputs[ch] = False
            print(f"  -> Outputs {channels} OFF")
        except:
            print("  -> Error parsing command")

    elif cmd == "test":
        print("  -> Testing all outputs...")
        for i in range(NUM_OUTPUTS):
            outputs[i] = True
            time.sleep(0.3)
            outputs[i] = False


def command_loop():
    """Watch for commands in file"""
    # Create empty command file
    open(COMMAND_FILE, 'w').close()

    last_mtime = 0
    while True:
        try:
            if os.path.exists(COMMAND_FILE):
                mtime = os.path.getmtime(COMMAND_FILE)
                if mtime > last_mtime:
                    last_mtime = mtime
                    with open(COMMAND_FILE, 'r') as f:
                        for line in f:
                            process_command(line)
                    # Clear the file
                    open(COMMAND_FILE, 'w').close()
        except:
            pass
        time.sleep(0.1)


def main():
    global client, connected

    print("BK9000 Daemon")
    print("=" * 40)
    print(f"Connecting to {BK9000_IP}...")

    client = ModbusTcpClient(BK9000_IP, port=BK9000_PORT, timeout=5)
    connected = client.connect()

    if not connected:
        print("Connection failed!")
        return

    print("Connected!")

    # Disable watchdog automatically
    print("Disabling watchdog...")
    client.write_register(0x1120, 0)
    client.write_register(0x1122, 2)
    r = client.read_holding_registers(0x1122, count=1)
    if not r.isError() and r.registers[0] == 2:
        print("Watchdog DISABLED - outputs will persist after disconnect!")
    else:
        print("Warning: Could not disable watchdog")
    print()
    print(f"Send commands via: echo \"on 0\" > {COMMAND_FILE}")
    print("Commands: on <n>, off <n>, all on, all off, status, test")
    print()
    print("Press Ctrl+C to stop")
    print()

    # Start background threads
    threading.Thread(target=watchdog_loop, daemon=True).start()
    threading.Thread(target=read_inputs_loop, daemon=True).start()
    threading.Thread(target=command_loop, daemon=True).start()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
            if not connected:
                print("Connection lost! Reconnecting...")
                connected = client.connect()
                if connected:
                    print("Reconnected!")
    except KeyboardInterrupt:
        print("\nShutting down...")
        outputs[:] = [False] * NUM_OUTPUTS
        time.sleep(0.2)
        client.close()
        print("Bye!")


if __name__ == "__main__":
    main()
