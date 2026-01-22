# BK9000 Modbus TCP Control

Python-Steuerung für Beckhoff BK9000 Bus Coupler mit KL-Terminals.

## Hardware

- **BK9000** Bus Coupler (IP: 10.0.0.7, Port: 502)
- **6x KL1114** (4-channel digital input, 24V DC) = 24 inputs
- **5x KL2134** (4-channel digital output, 24V DC) = 20 outputs
- **1x KL9010** (end terminal)

```
BK9000 → KL1114(x6) → KL2134(x5) → KL9010
```

Output-Adressierung läuft vom KL9010 rückwärts (Output 0-3 = KL2134 nächst am KL9010).

**KL2134 LED Layout (pro Modul):**
```
┌─────────┐
│  0   1  │
│  2   3  │
└─────────┘
```
Outputs pro Modul: #1=0-3, #2=4-7, #3=8-11, #4=12-15, #5=16-19

## Installation

```bash
pip install pymodbus
```

## Wichtig: Watchdog

Der BK9000 hat einen aggressiven Watchdog der Outputs nach Verbindungsverlust sperrt. **Muss bei jedem Boot deaktiviert werden:**

```python
client.write_register(0x1120, 0)   # Timeout = 0
client.write_register(0x1122, 2)   # Mode = Disabled
```

`daemon.py` macht das automatisch. Ohne Deaktivierung brauchen Outputs einen BK9000 Neustart nach jedem Disconnect.

## Verwendung

**Daemon starten (nach BK9000 Power-On):**
```bash
python daemon.py
```

**Befehle senden:**
```bash
python cmd.py on 0          # Output 0 an
python cmd.py off 0         # Output 0 aus
python cmd.py on 0,1,2,3    # Mehrere Outputs an
python cmd.py all on        # Alle 20 Outputs an
python cmd.py all off       # Alle Outputs aus
python cmd.py test          # Alle Outputs durchlaufen
python cmd.py status        # I/O Status anzeigen
```

**Watchdog einzeln deaktivieren:**
```bash
python init.py
```

**Diagnose/Health Check:**
```bash
python status.py
```

**Auto-Recovery (permanent laufen lassen):**
```bash
python watcher.py
```
Überwacht BK9000 alle 5 Sekunden. Deaktiviert Watchdog automatisch nach BK9000-Neustart.

## Dateien

| Datei | Zweck |
|-------|-------|
| `config.py` | IP-Adresse und I/O-Anzahl |
| `daemon.py` | Hauptcontroller - Watchdog deaktivieren, Befehle verarbeiten |
| `cmd.py` | Befehle an laufenden Daemon senden |
| `init.py` | Watchdog einzeln deaktivieren |
| `out.py` | Einfache Output-Steuerung (ohne Daemon) |
| `status.py` | Diagnose - Terminal-Anzahl und I/O-Status |
| `watcher.py` | Auto-Recovery nach BK9000-Neustart |
| `ads_test.py` | ADS-Protokoll Exploration |

## Modbus Register

| Register | Funktion |
|----------|----------|
| Coils 0-19 (FC01/05) | Digital Outputs (KL2134) |
| Discrete Inputs 0-23 (FC02) | Digital Inputs (KL1114) |
| 0x1000 | Coupler Info (ASCII: Model/Firmware) |
| 0x1012 | Digital Output Anzahl (20 = OK) |
| 0x1013 | Digital Input Anzahl (24 = OK) |
| 0x1120 | Watchdog Timeout (0 = aus) |
| 0x1122 | Watchdog Mode (1=enabled, 2=disabled) |

## Troubleshooting

**Outputs reagieren nicht:**
1. Läuft der Daemon?
2. BK9000 aus/ein, dann sofort `python daemon.py`

**Connection Timeout:**
1. IP in `config.py` prüfen
2. Netzwerk: `ping 10.0.0.7`
3. Port: `Test-NetConnection -ComputerName 10.0.0.7 -Port 502`

**LED-Verhalten:**
- KL1114: LEDs zeigen Input-Status (24V = AN)
- KL2134: LEDs zeigen Output-Status, brauchen 24V auf Power-Kontakten

## KL1114 Verdrahtung

```
┌─────────────┐
│  1   2   3   4   ← Eingänge (+24V Signal hier)
│  ●   ●   ●   ●
│
│  ●   ●   ●   ●
│  5   6   7   8   ← 0V / GND (intern verbunden)
└─────────────┘
```

## DIP-Schalter

| DIP | Funktion |
|-----|----------|
| 1-8 | Letztes Oktett der IP (binär) |
| 9 | BootP (ON = aktiv) |
| 10 | DHCP (ON = aktiv) |

**Modi:**
- DIP 9=OFF, 10=OFF → Statische IP (DIP 1-8 = letztes Oktett)
- DIP 9=ON, 10=OFF → BootP
- DIP 9=OFF, 10=ON → DHCP (aktuelle Einstellung)

## ADS Protokoll (Port 48898)

BK9000 unterstützt eingeschränktes ADS neben Modbus TCP.

- **Port 100**: Register-Zugriff (nur lesen)
- **Port 300**: Fieldbus-Daten (nur Inputs)

Für praktische Nutzung ist Modbus TCP besser. ADS-Implementierung (ca. 2000) sehr limitiert.

```bash
python ads_test.py
```

## Weitere Dokumentation

- `KL-MODULE.md` - Referenz aller KL-Terminaltypen
