# KL-Module Referenz

Übersicht der Beckhoff KL-Bus-Terminals für BK9000/BK9050/BKxxxx Koppler.

## Aktuell verbaut

| Modul | Typ | Kanäle | Beschreibung |
|-------|-----|--------|--------------|
| **KL1114** | Digital IN | 4 | 24V DC, 3ms Filter |
| **KL2134** | Digital OUT | 4 | 24V DC, 0.5A pro Kanal |
| **KL9010** | End-Terminal | - | K-Bus Abschluss (Pflicht!) |

---

## Digital Eingänge (KL1xxx)

| Modul | Kanäle | Spannung | Besonderheit |
|-------|--------|----------|--------------|
| KL1002 | 2 | 24V DC | Standard |
| KL1004 | 4 | 24V DC | Standard |
| KL1104 | 4 | 24V DC | Accent-Klemmen |
| **KL1114** | 4 | 24V DC | Accent, 3ms Filter |
| KL1124 | 4 | 5V DC | TTL-Pegel |
| KL1154 | 4 | 24V DC | Verpolschutz |
| KL1194 | 4 | 24V DC | 3-Leiter, Sensorversorgung |
| KL1232 | 2 | 24V AC/DC | Wechselspannung |
| KL1304 | 4 | 24V DC | Potentialgetrennt |
| KL1408 | 8 | 24V DC | 8-Kanal (HD) |
| KL1418 | 8 | 24V DC | 8-Kanal, schnell (0.2ms) |
| KL1488 | 8 | 24V DC | 8-Kanal, potentialfrei |
| KL1501 | 1 | - | **Zähler** bis 100kHz |
| KL1512 | 2 | - | **Zähler** 24V DC |

## Digital Ausgänge (KL2xxx)

| Modul | Kanäle | Strom | Besonderheit |
|-------|--------|-------|--------------|
| KL2012 | 2 | 0.5A | Standard |
| KL2022 | 2 | 2A | Hoher Strom |
| KL2032 | 2 | 24V DC | Potentialfrei |
| KL2114 | 4 | 0.5A | Standard |
| **KL2134** | 4 | 0.5A | Accent-Klemmen |
| KL2184 | 4 | 0.5A | Potentialfrei |
| KL2408 | 8 | 0.5A | 8-Kanal (HD) |
| KL2442 | 2 | 2x3A | **Relais** |
| KL2602 | 2 | 30V/5A | **Relais**, potentialfrei |
| KL2612 | 2 | 125V/0.5A | **Relais**, AC tauglich |
| KL2631 | 1 | - | **PWM** 24V DC |
| KL2641 | 1 | - | **PWM** 24V, 5A |

## Analog Eingänge (KL3xxx) - für Spannungsmessung!

| Modul | Kanäle | Bereich | Auflösung | Besonderheit |
|-------|--------|---------|-----------|--------------|
| KL3001 | 1 | ±10V | 12-Bit | Standard |
| KL3002 | 2 | ±10V | 12-Bit | Standard |
| KL3012 | 2 | 0-10V | 12-Bit | Unipolar |
| **KL3054** | 4 | 4-20mA | 12-Bit | **Stromschleife** |
| **KL3064** | 4 | 0-10V | 12-Bit | **Spannungsmessung** |
| KL3102 | 2 | ±10V | 16-Bit | Hohe Auflösung |
| KL3112 | 2 | 0-10V | 16-Bit | Hohe Auflösung |
| KL3152 | 2 | 4-20mA | 16-Bit | Stromschleife, präzise |
| KL3162 | 2 | 0-10V | 16-Bit | Differenziell |
| KL3202 | 2 | PT100 | - | **Temperatur** RTD |
| KL3204 | 4 | PT100 | - | **Temperatur** 4-Kanal |
| KL3222 | 2 | PT100 | - | **Temperatur** 3-Leiter |
| KL3312 | 2 | Thermoelem. | - | **Temperatur** TC |
| KL3314 | 4 | Thermoelem. | - | **Temperatur** 4-Kanal |
| KL3403 | 3 | 500V AC | - | **Netzüberwachung** |
| KL3404 | 4 | ±10V | 12-Bit | Single-ended |
| KL3408 | 8 | ±10V | 12-Bit | 8-Kanal (HD) |
| KL3454 | 4 | 4-20mA | 12-Bit | Stromschleife |
| KL3464 | 4 | 0-10V | 12-Bit | Spannungsmessung |
| KL3468 | 8 | 0-10V | 12-Bit | 8-Kanal |

## Analog Ausgänge (KL4xxx)

| Modul | Kanäle | Bereich | Auflösung |
|-------|--------|---------|-----------|
| KL4001 | 1 | 0-10V | 12-Bit |
| KL4002 | 2 | 0-10V | 12-Bit |
| KL4004 | 4 | 0-10V | 12-Bit |
| KL4012 | 2 | ±10V | 12-Bit |
| KL4022 | 2 | 4-20mA | 12-Bit |
| KL4112 | 2 | 0-10V | 16-Bit |
| KL4132 | 2 | ±10V | 16-Bit |
| KL4404 | 4 | 0-10V | 12-Bit |
| KL4408 | 8 | 0-10V | 12-Bit |
| KL4414 | 4 | 0-20mA | 12-Bit |

## Spezial-Module (KL5xxx, KL6xxx)

| Modul | Funktion | Beschreibung |
|-------|----------|--------------|
| KL5001 | SSI | Absolutwertgeber |
| KL5101 | Inkremental | Encoder bis 500kHz |
| KL5111 | Inkremental | Encoder mit Latch |
| KL5151 | Inkremental | Encoder, 2-Kanal |
| KL6001 | Seriell | RS232 |
| KL6011 | Seriell | RS232, 115200 Baud |
| KL6021 | Seriell | RS422/RS485 |
| KL6031 | Seriell | RS485, Vollduplex |
| KL6041 | Seriell | RS485, 2-Kanal |
| KL6201 | AS-i | AS-Interface Master |
| KL6301 | Profibus | Profibus-DP Slave |
| KL6401 | LON | LON-Bus |
| KL6581 | DALI | Lichtsteuerung |
| KL6771 | DMX | Bühnenbeleuchtung |
| KL6811 | MP-Bus | Belimo Antriebe |

## System/Diagnose (KL9xxx)

| Modul | Funktion | Beschreibung |
|-------|----------|--------------|
| KL9100 | Potential | 24V Einspeiseklemme |
| KL9110 | Potential | 24V mit Sicherung |
| KL9150 | Potential | Potentialtrennung |
| KL9160 | Potential | 0V Verteilerklemme |
| KL9186 | Potential | 8x 24V Verteilung |
| KL9188 | Potential | 8x 0V Verteilung |
| KL9200 | Diagnose | K-Bus Diagnose |
| KL9210 | Schutz | Überstromschutz 2A |
| KL9260 | Diagnose | Diagnose-Interface |
| KL9290 | Diagnose | K-Bus Status |
| KL9400 | Diagnose | Modul-Interface |
| **KL9505** | Power | **K-Bus Spannungsüberwachung** |
| KL9510 | Power | K-Bus Refresh (bei >64 Klemmen) |
| KL9520 | Power | Netzteil 24V → K-Bus |
| KL9528 | Power | US-Spannungsversorgung |
| KL9540 | Power | Puffermodul |
| KL9560 | System | Systemklemme |
| **KL9010** | End | **Bus-Endklemme** (Pflicht!) |

---

## Empfehlungen für Überwachung

### 24V Spannungsüberwachung
```
Option 1: KL3064 (4x 0-10V Analog-Eingang)
          + Spannungsteiler 24V → 10V (2:1)

Option 2: KL3054 (4x 4-20mA)
          + Stromwandler/Shunt

Option 3: Freier KL1114-Eingang
          + Relais das bei 24V anzieht
          → Einfache OK/Fehler-Erkennung
```

### Temperaturüberwachung
```
KL3204 - 4x PT100 (Schaltschrank-Temperatur)
KL3314 - 4x Thermoelement (höhere Temperaturen)
```

### K-Bus Status
```
KL9505 - Zeigt K-Bus Spannung an
KL9200 - Erweiterte K-Bus Diagnose
```

---

## Modbus-Adressierung

Bei BK9000 werden Module automatisch adressiert:
- Digitale I/Os: Bitweise ab Adresse 0
- Analoge Werte: Wortweise (16-Bit) ab Adresse 0

```
Beispiel mit KL3064 (4x Analog):
  Holding Register 0: Kanal 1 (0-32767 = 0-10V)
  Holding Register 1: Kanal 2
  Holding Register 2: Kanal 3
  Holding Register 3: Kanal 4
```

---

## Links

- Beckhoff KL-Terminals: https://www.beckhoff.com/de-de/produkte/i-o/bus-terminals/
- BK9000 Dokumentation: https://infosys.beckhoff.com
