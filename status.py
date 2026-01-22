"""
BK9000 Status - Full diagnostics and health check
"""
from pymodbus.client import ModbusTcpClient
from config import BK9000_IP, BK9000_PORT, NUM_INPUTS, NUM_OUTPUTS

EXPECTED_OUTPUTS = NUM_OUTPUTS  # 5x KL2134
EXPECTED_INPUTS = NUM_INPUTS    # 6x KL1114


def get_full_status():
    client = ModbusTcpClient(BK9000_IP, port=BK9000_PORT, timeout=3)
    if not client.connect():
        return {"error": "Connection failed"}

    status = {}

    # Coupler info (0x1000) - contains model/firmware as ASCII
    r = client.read_holding_registers(0x1000, count=8)
    if not r.isError():
        try:
            ascii_str = ''.join([chr(reg >> 8) + chr(reg & 0xFF) for reg in r.registers])
            status["coupler_info"] = ascii_str.replace('\x00', ' ').strip()
        except:
            status["coupler_info"] = "unknown"

    # I/O count (0x1010)
    r = client.read_holding_registers(0x1010, count=8)
    if not r.isError():
        status["digital_outputs"] = r.registers[2]
        status["digital_inputs"] = r.registers[3]
        status["outputs_ok"] = r.registers[2] == EXPECTED_OUTPUTS
        status["inputs_ok"] = r.registers[3] == EXPECTED_INPUTS

    # Watchdog registers
    r = client.read_holding_registers(0x1120, count=1)
    if not r.isError():
        status["watchdog_timeout"] = r.registers[0]

    r = client.read_holding_registers(0x1122, count=1)
    if not r.isError():
        mode = r.registers[0]
        status["watchdog_mode_raw"] = mode
        status["watchdog_mode"] = "DISABLED" if mode == 2 else "ENABLED"
        status["watchdog_safe"] = mode == 2

    r = client.read_holding_registers(0x1124, count=1)
    if not r.isError():
        status["watchdog_fallback"] = r.registers[0]

    # Read current I/O states
    r = client.read_discrete_inputs(address=0, count=NUM_INPUTS)
    if not r.isError():
        status["inputs"] = r.bits[:NUM_INPUTS]

    r = client.read_coils(address=0, count=NUM_OUTPUTS)
    if not r.isError():
        status["outputs"] = r.bits[:NUM_OUTPUTS]

    client.close()
    return status


def format_io_grid(bits, cols=4, label="CH"):
    """Format I/O bits as visual grid"""
    lines = []
    for i in range(0, len(bits), cols):
        row_bits = bits[i:i+cols]
        row_str = " ".join(["[X]" if b else "[ ]" for b in row_bits])
        row_labels = " ".join([f"{i+j:2d}" for j in range(len(row_bits))])
        lines.append(f"  {row_str}  ({label} {i}-{i+len(row_bits)-1})")
    return "\n".join(lines)


def main():
    print()
    print("=" * 55)
    print("  BK9000 FULL DIAGNOSTICS")
    print("=" * 55)

    status = get_full_status()

    if "error" in status:
        print(f"\n  ERROR: {status['error']}")
        print()
        return 1

    # Connection info
    print(f"\n  Connection: {BK9000_IP}:{BK9000_PORT} - OK")

    # Coupler info
    print(f"\n  COUPLER IDENTIFICATION")
    print(f"  " + "-" * 40)
    print(f"  Model/Firmware: {status.get('coupler_info', 'unknown')}")

    # Terminal count
    print(f"\n  TERMINAL COUNT")
    print(f"  " + "-" * 40)
    outputs = status.get('digital_outputs', 0)
    inputs = status.get('digital_inputs', 0)
    out_status = "OK" if status.get('outputs_ok') else "MISMATCH!"
    in_status = "OK" if status.get('inputs_ok') else "MISMATCH!"
    print(f"  Digital Outputs: {outputs:2d} (expected {EXPECTED_OUTPUTS}) [{out_status}]")
    print(f"  Digital Inputs:  {inputs:2d} (expected {EXPECTED_INPUTS}) [{in_status}]")

    # Watchdog
    print(f"\n  WATCHDOG STATUS")
    print(f"  " + "-" * 40)
    wd_mode = status.get('watchdog_mode', 'unknown')
    wd_safe = status.get('watchdog_safe', False)
    wd_timeout = status.get('watchdog_timeout', 0)
    wd_fallback = status.get('watchdog_fallback', 0)

    if wd_safe:
        print(f"  Mode: {wd_mode} - Outputs persist after disconnect")
    else:
        print(f"  Mode: {wd_mode} - WARNING: Outputs will lock on disconnect!")
        print(f"  Timeout: {wd_timeout}ms")
        print(f"  Fallback: {wd_fallback}")

    # Current I/O states
    if "inputs" in status:
        print(f"\n  DIGITAL INPUTS (KL1114 x6)")
        print(f"  " + "-" * 40)
        inputs_active = sum(status["inputs"])
        print(f"  Active: {inputs_active} of {NUM_INPUTS}")
        print(format_io_grid(status["inputs"], cols=4, label="IN"))

    if "outputs" in status:
        print(f"\n  DIGITAL OUTPUTS (KL2134 x5)")
        print(f"  " + "-" * 40)
        outputs_active = sum(status["outputs"])
        print(f"  Active: {outputs_active} of {NUM_OUTPUTS}")
        print(format_io_grid(status["outputs"], cols=4, label="OUT"))

    # Summary
    print()
    print("=" * 55)
    all_ok = status.get('outputs_ok') and status.get('inputs_ok') and status.get('watchdog_safe')
    if all_ok:
        print("  STATUS: ALL OK")
    else:
        issues = []
        if not status.get('outputs_ok'):
            issues.append("Output count mismatch")
        if not status.get('inputs_ok'):
            issues.append("Input count mismatch")
        if not status.get('watchdog_safe'):
            issues.append("Watchdog enabled (run init.py)")
        print(f"  STATUS: ISSUES DETECTED")
        for issue in issues:
            print(f"    - {issue}")
    print("=" * 55)
    print()

    return 0 if all_ok else 1


if __name__ == "__main__":
    exit(main())
