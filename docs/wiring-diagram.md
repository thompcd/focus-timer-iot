# Focus Timer System Diagram

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FOCUS TIMER SYSTEM                                │
│                       (Serial Communication)                                │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────┐       ┌─────────────────────────┐
  │        SenseCAP Indicator D1101        │       │   Maker Pi RP2040       │
  │                                        │       │                         │
  │  ┌──────────────────────────────────┐  │       │   ┌─────────────────┐   │
  │  │         ESP32-S3 (Top USB)       │  │       │   │    RP2040       │   │
  │  │                                  │  │       │   │                 │   │
  │  │  ┌────────────────────────────┐  │  │       │   │  CircuitPython  │   │
  │  │  │    4" Touch LCD (LVGL)     │  │  │       │   │    code.py      │   │
  │  │  │                            │  │  │       │   │                 │   │
  │  │  │   "Heads down. Be back in" │  │  │       │   └────────┬────────┘   │
  │  │  │          25:00             │  │  │       │            │            │
  │  │  │                            │  │  │       │     ┌──────┴──────┐     │
  │  │  │    [5m] [15m] [30m]        │  │  │       │     │  Grove 1    │     │
  │  │  │        [START]             │  │  │       │     │  GP0/GP1    │     │
  │  │  └────────────────────────────┘  │  │       │     │  (UART RX)  │     │
  │  │                                  │  │       │     └──────┬──────┘     │
  │  │  GPIO 19/20 (UART + COBS)        │  │       │            │            │
  │  └───────────────┬──────────────────┘  │       │     ┌──────┴──────┐     │
  │                  │                     │       │     │    S4       │     │
  │                  ▼                     │       │     │   GP15      │     │
  │  ┌──────────────────────────────────┐  │       │     │  (Servo)    │     │
  │  │       RP2040 (Bottom USB)        │  │       │     └──────┬──────┘     │
  │  │                                  │  │       │            │            │
  │  │    Serial Bridge Firmware        │  │       └────────────┼────────────┘
  │  │    (Arduino/PlatformIO)          │  │                    │
  │  │                                  │  │                    │
  │  │  ┌────────────────────────────┐  │  │                    ▼
  │  │  │   Grove Connector          │  │  │         ┌─────────────────────┐
  │  │  │   GP20 (TX) ─────────────────────────────► │   Continuous        │
  │  │  │   GP21 (RX) ◄──────────────────────────────│   Rotation Servo    │
  │  │  │   GND ─────────────────────────────────────│                     │
  │  │  │   VCC ─────────────────────────────────────│   (GeekServo 360°)  │
  │  │  └────────────────────────────┘  │  │         │                     │
  │  │                                  │  │         │   throttle control: │
  │  └──────────────────────────────────┘  │         │   0 = stop          │
  │                                        │         │   ±0.5 = spin       │
  └────────────────────────────────────────┘         └─────────────────────┘
```

---

## Data Flow

```
┌─────────────┐    UART     ┌─────────────┐   Grove    ┌─────────────┐
│   ESP32-S3  │────────────►│   RP2040    │───Serial──►│  Maker Pi   │
│  (Touch UI) │  GPIO 19/20 │  (Bridge)   │  GP20→GP0  │  RP2040     │
│             │  COBS frame │             │  GP21←GP1  │             │
└─────────────┘             └─────────────┘  (SWAPPED) └──────┬──────┘
                                                              │
      Timer state: "T<running>,<mm>,<ss>\n"                   │
      Example: "T1,25,00\n" = running, 25:00                  │
                                                              ▼
                                                     ┌─────────────────┐
                                                     │  Servo on GP15  │
                                                     │  (S4 port)      │
                                                     │                 │
                                                     │  START → spin   │
                                                     │  STOP  → spin   │
                                                     │          back   │
                                                     └─────────────────┘
```

---

## Physical Connections

### Grove Cable (SenseCAP RP2040 → Maker Pi)

**IMPORTANT: TX/RX must be crossed!**

| SenseCAP RP2040 Grove | Wire  | Maker Pi Grove 1 |
|-----------------------|-------|------------------|
| GP20 (TX)             | ────► | GP0 (RX)         |
| GP21 (RX)             | ◄──── | GP1 (TX)         |
| VCC                   | ───── | VCC              |
| GND                   | ───── | GND              |

If using a standard Grove cable, **swap the data lines** (yellow/white wires)
or use a crossover adapter.

### Servo Connection

| Servo Wire | Color  | Maker Pi Port |
|------------|--------|---------------|
| Signal     | Orange | S4 (GP15)     |
| Power      | Red    | VCC (5V)      |
| Ground     | Brown  | GND           |

---

## Serial Protocol

**Baud Rate:** 115200  
**Format:** `T<running>,<minutes>,<seconds>\n`

| Field     | Values        | Example |
|-----------|---------------|---------|
| running   | 0=stopped, 1=running | 1 |
| minutes   | 00-99         | 25      |
| seconds   | 00-59         | 00      |

**Examples:**
- `T1,25,00\n` → Timer running, 25:00 remaining
- `T0,00,00\n` → Timer stopped

---

## USB Ports

```
     SenseCAP Indicator D1101
    ┌─────────────────────────┐
    │                         │
    │         [TOP USB-C]     │  ← ESP32-S3 (upload UI firmware)
    │                         │    /dev/cu.usbserial-1110
    │                         │    Baud: 460800
    │    ┌───────────────┐    │
    │    │   4" Touch    │    │
    │    │     LCD       │    │
    │    └───────────────┘    │
    │                         │
    │         [BTM USB-C]     │  ← RP2040 (upload bridge firmware)
    │                         │    /dev/cu.usbmodem11201
    └─────────────────────────┘

     Maker Pi RP2040
    ┌─────────────────────────┐
    │                         │
    │          [USB-C]        │  ← RP2040 (CircuitPython)
    │                         │    /dev/cu.usbmodem2301
    │   ┌─────────────────┐   │    or /Volumes/CIRCUITPY
    │   │ [S1][S2][S3][S4]│   │
    │   │ Servo ports     │   │    Servo on S4 (GP15)
    │   └─────────────────┘   │
    │                         │
    │   [Grove 1]  [Grove 2]  │  ← Grove 1 = GP0/GP1 (serial RX)
    └─────────────────────────┘
```

---

## Firmware Locations

| Component | Path | Notes |
|-----------|------|-------|
| ESP32 UI | `SenseCAP_Indicator_ESP32/examples/focus_timer/` | LVGL dark theme |
| RP2040 Bridge | `SenseCAP_Indicator_RP2040/examples/focus_timer_bridge/` | PlatformIO |
| Maker Pi | `/Volumes/CIRCUITPY/code.py` | CircuitPython |

---

## Lessons Learned

1. **GPIO 39/40 conflict**: Can't use external I2C on SenseCAP — those pins are used by the touch controller
2. **1200 baud trap**: Touching RP2040 serial at 1200 baud triggers bootloader mode
3. **Grove serial pinout**: SenseCAP RP2040 Grove uses GP20/GP21, not GP0/GP1
4. **TX/RX swap required**: Grove cables are straight-through; serial needs crossover
5. **Continuous servo**: Uses throttle (0=stop, ±0.5=spin), not angle positioning
