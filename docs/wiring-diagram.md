# Wiring Diagram

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FOCUS TIMER SYSTEM                                │
│                         (I2C Communication)                                 │
└─────────────────────────────────────────────────────────────────────────────┘

     ┌──────────────────────┐              ┌─────────────────────────────────┐
     │  SenseCAP Indicator  │              │    Raspberry Pi Zero 2 W        │
     │       D1101          │              │    + Inventor HAT Mini          │
     │                      │              │                                 │
     │   ┌──────────────┐   │              │   ┌───────────────────────┐     │
     │   │  4" LCD      │   │              │   │   Inventor HAT Mini   │     │
     │   │  480x480     │   │              │   │                       │     │
     │   │  Touchscreen │   │              │   │  [Servo 1] [Servo 2]  │     │
     │   └──────────────┘   │              │   │     │                 │     │
     │                      │              │   │     └──────────┐      │     │
     │   Grove Connector    │    I2C       │   │                │      │     │
     │   ┌──────────────┐   │   ┌─────┐    │   │  ┌─────────┐   │      │     │
     │   │ GND VCC SDA SCL│◄──┼───┤QW/ST├────┼───►│ QW/ST   │   │      │     │
     │   └──────────────┘   │   └─────┘    │   │  │Connector│   │      │     │
     │         │   │        │              │   │  └─────────┘   │      │     │
     │         │   │        │              │   │                │      │     │
     └─────────┼───┼────────┘              │   └────────────────┼──────┘     │
               │   │                       │                    │            │
               │   │                       └────────────────────┼────────────┘
               │   │                                            │
               │   └───── I2C Bus (SDA/SCL) ────────────────────┘
               │                                                │
               └──────────────── 3.3V + GND ────────────────────┘
                                                               │
                                                               ▼
                                                    ┌─────────────────┐
                                                    │   GeekServo     │
                                                    │   360° Cont.    │
                                                    │                 │
                                                    │  Red ── 5V      │
                                                    │  Brn ── GND     │
                                                    │  Org ── Signal  │
                                                    └─────────────────┘
```

---

## I2C Connection (QW/ST / Qwiic / STEMMA QT)

The Inventor HAT Mini has a **QW/ST** connector (compatible with Qwiic and STEMMA QT).
The SenseCAP Indicator has a **Grove** connector for I2C.

### Connector Pinouts

**Grove Connector (SenseCAP Indicator):**
```
┌─────────────────┐
│  ●   ●   ●   ●  │
│ GND VCC SDA SCL │
│  Bk  Rd  Wh  Yl │  (typical Grove wire colors)
└─────────────────┘
```

**QW/ST Connector (Inventor HAT Mini):**
```
┌─────────────────┐
│  ●   ●   ●   ●  │
│ GND 3V3 SDA SCL │
│  Bk  Rd  Bl  Yl │  (Qwiic standard colors)
└─────────────────┘
```

### Wiring Table

| SenseCAP Grove | Wire Color | Inventor HAT QW/ST | Notes |
|----------------|------------|-------------------|-------|
| GND | Black | GND | Common ground |
| VCC | Red | 3V3 | 3.3V power |
| SDA | White | SDA (Blue) | I2C Data |
| SCL | Yellow | SCL (Yellow) | I2C Clock |

### Cable Options

1. **Grove to Qwiic Adapter Cable** (recommended)
   - Available from Seeed Studio, SparkFun, Adafruit
   - Plug-and-play, no soldering

2. **DIY Cable**
   - Cut and splice Grove and Qwiic cables
   - Match colors per table above

3. **Direct Wiring**
   - Use jumper wires from Grove header to QW/ST pads/header

```
         Grove Cable              Qwiic Cable
    ┌────────────────┐        ┌────────────────┐
    │ GND VCC SDA SCL│        │ GND 3V3 SDA SCL│
    │  Bk  Rd  Wh  Yl│───────►│  Bk  Rd  Bl  Yl│
    └────────────────┘        └────────────────┘
        SenseCAP                 Inventor HAT
```

---

## Servo Connection

Connect GeekServo to **Servo 1** header on Inventor HAT Mini:

```
Inventor HAT Mini - Servo Headers
┌────────────────────────────────────────────┐
│                                            │
│  ┌──────────┐        ┌──────────┐          │
│  │ SERVO 1  │        │ SERVO 2  │          │
│  │ ┌─┬─┬─┐  │        │ ┌─┬─┬─┐  │          │
│  │ │S│+│-│  │        │ │S│+│-│  │          │
│  │ └─┴─┴─┘  │        │ └─┴─┴─┘  │          │
│  └──────────┘        └──────────┘          │
│     │ │ │                                  │
│     │ │ └─ GND (Brown wire)                │
│     │ └─── 5V  (Red wire)                  │
│     └───── Sig (Orange wire)               │
│                                            │
└────────────────────────────────────────────┘
```

**GeekServo 360° Wiring:**

| Servo Wire | Color | Inventor HAT Pin |
|------------|-------|-----------------|
| Signal | Orange | S (Signal) |
| Power | Red | + (5V) |
| Ground | Brown | - (GND) |

---

## Complete Wiring Diagram

```
                    ┌─────────────────────────────┐
                    │     SenseCAP Indicator      │
                    │         D1101               │
                    │                             │
                    │  ┌───────────────────────┐  │
                    │  │     4" Touchscreen    │  │
                    │  │       480x480         │  │
                    │  │                       │  │
                    │  │    "Heads down."      │  │
                    │  │    "Be back in"       │  │
                    │  │        5:00           │  │
                    │  │                       │  │
                    │  │  [5m] [15m] [30m]     │  │
                    │  │      [START]          │  │
                    │  │                       │  │
                    │  └───────────────────────┘  │
                    │                             │
                    │  Grove I2C ──┐              │
                    └──────────────┼──────────────┘
                                   │
                         ┌─────────┴─────────┐
                         │ Grove-to-Qwiic    │
                         │ Adapter Cable     │
                         │                   │
                         │  GND ─── GND      │
                         │  VCC ─── 3V3      │
                         │  SDA ─── SDA      │
                         │  SCL ─── SCL      │
                         └─────────┬─────────┘
                                   │
    ┌──────────────────────────────┴────────────────────────────────┐
    │                     Raspberry Pi Zero 2 W                      │
    │                   + Inventor HAT Mini                          │
    │                                                                │
    │  ┌────────────────────────────────────────────────────────┐    │
    │  │                  Inventor HAT Mini                     │    │
    │  │                                                        │    │
    │  │   ┌──────┐  ┌──────┐        ┌───────────────────────┐  │    │
    │  │   │QW/ST │◄─┤ I2C  │        │      SERVO 1          │  │    │
    │  │   │ Port │  │ Bus  │        │   ┌───┬───┬───┐       │  │    │
    │  │   └──────┘  └──────┘        │   │ S │ + │ - │       │  │    │
    │  │                             │   └─┬─┴─┬─┴─┬─┘       │  │    │
    │  │   I2C Address: 0x42         │     │   │   │         │  │    │
    │  │   (SenseCAP slave)          │     │   │   │         │  │    │
    │  │                             └─────┼───┼───┼─────────┘  │    │
    │  │                                   │   │   │            │    │
    │  └───────────────────────────────────┼───┼───┼────────────┘    │
    │                                      │   │   │                 │
    └──────────────────────────────────────┼───┼───┼─────────────────┘
                                           │   │   │
                                           │   │   │
                                    ┌──────┴───┴───┴──────┐
                                    │     GeekServo       │
                                    │   360° Continuous   │
                                    │                     │
                                    │   Orange ── Signal  │
                                    │   Red ───── 5V      │
                                    │   Brown ─── GND     │
                                    │                     │
                                    │   ┌───────────┐     │
                                    │   │  Rotates  │     │
                                    │   │  physical │     │
                                    │   │ indicator │     │
                                    │   └───────────┘     │
                                    └─────────────────────┘
```

---

## I2C Protocol

The SenseCAP Indicator acts as an I2C **slave** device.
The Raspberry Pi is the I2C **master**.

**I2C Address:** `0x42`

**Registers:**

| Register | Address | Description | Values |
|----------|---------|-------------|--------|
| STATUS | 0x00 | Timer running state | 0 = stopped, 1 = running |
| MINUTES | 0x01 | Minutes remaining | 0-99 |
| SECONDS | 0x02 | Seconds remaining | 0-59 |

**Read Sequence:**
```
1. Pi sends: [0x42] [register_addr]  (write register pointer)
2. Pi reads: [0x42] [data_byte]      (read register value)
```

**Example (Python):**
```python
import smbus2

bus = smbus2.SMBus(1)
address = 0x42

# Read status register
bus.write_byte(address, 0x00)  # Select register 0
status = bus.read_byte(address)  # Read value

print(f"Timer running: {status == 1}")
```

---

## Power Requirements

| Component | Voltage | Current | Power Source |
|-----------|---------|---------|--------------|
| Pi Zero 2 W | 5V | ~400mA | USB-C or GPIO |
| Inventor HAT Mini | 5V (from Pi) | ~50mA | Pi GPIO |
| GeekServo | 5V | ~200mA | Inventor HAT |
| SenseCAP Indicator | 5V | ~300mA | USB-C (separate) |

**Note:** The SenseCAP Indicator has its own USB-C power input.
Do NOT try to power it from the Pi.

---

## Troubleshooting

### I2C Device Not Found

```bash
# Scan I2C bus
sudo i2cdetect -y 1

# Should show 0x42:
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 40: -- -- 42 -- -- -- -- -- -- -- -- -- -- -- -- --
```

If 0x42 not found:
- Check cable connections
- Verify SenseCAP is running the focus timer firmware
- Check Grove/Qwiic cable orientation

### Servo Not Moving

1. Check servo connections to Servo 1 header
2. Verify servo wire colors match documentation
3. Test servo directly:
   ```python
   from inventorhatmini import InventorHATMini
   board = InventorHATMini()
   board.servos[0].value(1.0)  # Should spin
   ```

### I2C Errors

- Ensure I2C is enabled: `sudo raspi-config` → Interface Options → I2C
- Check for conflicting I2C addresses
- Try slower I2C speed if getting errors
