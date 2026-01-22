# CLAUDE.md

Anweisungen für Claude Code in diesem Repository.

## Projekt

BK9000 Modbus TCP Steuerung. Siehe README.md für Details.

## Wichtige Regeln

### Watchdog immer beachten
Bei jedem Modbus-Code der Outputs schreibt: Watchdog muss deaktiviert sein!
```python
client.write_register(0x1120, 0)   # Timeout = 0
client.write_register(0x1122, 2)   # Mode = Disabled
```

### pymodbus API
- `read_coils(address=0, count=20)` - nicht positional!
- `read_discrete_inputs(address=0, count=24)`
- `write_coil(address, value)`
- `read_holding_registers(0x1000, count=8)` - positional OK

### Hardware-Konfiguration
```python
BK9000_IP = "10.0.0.7"
BK9000_PORT = 502
NUM_INPUTS = 24   # 6x KL1114
NUM_OUTPUTS = 20  # 5x KL2134
```

### Output-Adressierung
Output 0-3 = KL2134 nächst am KL9010 (von hinten nach vorne nummeriert).

## Code-Stil

- Deutsch für User-Output, Englisch für Code/Kommentare
- Einfach halten - keine Über-Abstraktion
- config.py für Konfiguration nutzen

## Testen

```bash
python status.py      # Verbindung + I/O Status
python init.py        # Watchdog deaktivieren
python daemon.py      # Hauptcontroller starten
```
