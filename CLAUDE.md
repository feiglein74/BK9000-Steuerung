# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Modbus TCP control for Beckhoff BK9000 Bus Coupler with KL-series I/O terminals.

**Hardware Configuration:**
- BK9000 Bus Coupler (IP: 10.0.0.7, Port: 502)
- 6x KL1114 (4-channel digital input, 24V DC) = 24 inputs
- 5x KL2134 (4-channel digital output, 24V DC) = 20 outputs
- 1x KL9010 (end terminal)

**Physical Layout:**
```
BK9000 → KL1114(x6) → KL2134(x5) → KL9010
```
Note: Output addressing runs from KL9010 backwards (Output 0-3 = KL2134 nearest to KL9010).

**KL2134 LED Layout (per module):**
```
┌─────────┐
│  0   1  │
│  2   3  │
└─────────┘
```
Outputs per module: #1=0-3, #2=4-7, #3=8-11, #4=12-15, #5=16-19

## Critical: Watchdog Behavior

The BK9000 has an aggressive watchdog that locks outputs after any connection loss. **Must be disabled on every boot:**

```python
client.write_register(0x1120, 0)   # Timeout = 0
client.write_register(0x1122, 2)   # Mode = Disabled
```

The `daemon.py` does this automatically. Without disabling, outputs require BK9000 power cycle after any disconnect.

## Commands

**Start daemon (required after BK9000 power-on):**
```bash
python daemon.py
```

**Send commands to daemon:**
```bash
python cmd.py on 0          # Output 0 on
python cmd.py off 0         # Output 0 off
python cmd.py on 0,1,2,3    # Multiple outputs on
python cmd.py all on        # All 20 outputs on
python cmd.py all off       # All outputs off
python cmd.py test          # Cycle through all outputs
python cmd.py status        # Show I/O status
```

**Standalone watchdog disable:**
```bash
python init.py
```

**Health check / Monitoring:**
```bash
python status.py
```
Returns OK if all terminals present, MISMATCH if terminal count changed (hardware failure).

**Auto-recovery watcher (run permanently):**
```bash
python watcher.py
```
Monitors BK9000 every 5 seconds. Automatically disables watchdog after BK9000 reboot. Run as startup script or Windows service for 24/7 operation.

## Key Files

| File | Purpose |
|------|---------|
| `config.py` | IP address and I/O counts |
| `daemon.py` | Main controller - disables watchdog, handles commands |
| `cmd.py` | Send commands to running daemon |
| `init.py` | Standalone watchdog disable |
| `out.py` | Simple output control (no daemon needed, but needs BK9000 reboot after disconnect) |
| `status.py` | Health check - verifies terminal count for monitoring |
| `watcher.py` | Auto-recovery - monitors BK9000 and disables watchdog after reboot |

## Modbus Register Map

| Register | Function |
|----------|----------|
| Coils 0-19 (FC01/05) | Digital outputs (KL2134) |
| Discrete Inputs 0-23 (FC02) | Digital inputs (KL1114) |
| 0x1000 | Coupler info (ASCII: model/firmware) |
| 0x1012 | Digital output count (20 = OK) |
| 0x1013 | Digital input count (24 = OK) |
| 0x1120 | Watchdog timeout (write 0 to disable) |
| 0x1122 | Watchdog mode (1=enabled, 2=disabled) |

## Dependencies

```bash
pip install pymodbus
```

## Troubleshooting

**Outputs don't respond:**
1. Check if daemon is running
2. Power cycle BK9000, then immediately start `python daemon.py`

**Connection timeout:**
1. Verify IP address in `config.py`
2. Check network connection: `ping 10.0.0.7`
3. Verify port 502 is open: `Test-NetConnection -ComputerName 10.0.0.7 -Port 502`

**LED behavior:**
- KL1114: LEDs show input state (24V = ON)
- KL2134: LEDs show output state, require 24V on power contacts

## KL1114 Wiring (Digital Inputs)

```
┌─────────────┐
│  1   2   3   4   ← Inputs (connect +24V signal here)
│  ●   ●   ●   ●
│
│  ●   ●   ●   ●
│  5   6   7   8   ← 0V / GND (directly connected)
└─────────────┘
```
- Accent 1-4: Input channels (active when +24V applied)
- Contacts 5-8: Common 0V/GND (internally connected)

## DIP Switch Configuration

| DIP | Function |
|-----|----------|
| 1-8 | Last octet of IP address (binary) |
| 9 | BootP mode (ON = enabled) |
| 10 | DHCP mode (ON = enabled) |

**Modes:**
- DIP 9=OFF, 10=OFF → Static IP (DIP 1-8 = last octet, base IP set via KS2000)
- DIP 9=ON, 10=OFF → BootP Server
- DIP 9=OFF, 10=ON → DHCP (current setting)

Note: DIP switches only set the last octet. Base IP (default 172.16.17.x) requires KS2000 software to change.

## ADS Protocol (Port 48898)

The BK9000 supports a limited ADS implementation alongside Modbus TCP.

**Connection:**
- Port: 48898 (TCP)
- AMS Net ID: 10.0.0.7.1.1 (IP.1.1 format)

**Available Ports:**
| ADS Port | Function | Status |
|----------|----------|--------|
| 100 | Register Communication | Works (read only) |
| 300 | Fieldbus Data (I/O) | Partial (inputs only) |

**Port 100 - Register Access:**
- Uses Index Group = 0, Index Offset = register address
- Example: Read 0x1000 → `ads_read(port=100, IG=0, IO=0x1000, length=16)`

**Port 300 - I/O Data:**
- Inputs: Index Group = 0xF020, Offset = 0
- Outputs: Not accessible (Error 0x702)

**Conclusion:** For practical use, Modbus TCP is preferable. The BK9000 ADS implementation (ca. 2000) is very limited and doesn't offer significant advantages over Modbus.

**Test Script:**
```bash
python ads_test.py
```
