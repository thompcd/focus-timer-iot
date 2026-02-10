# Wiring Diagram

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FOCUS TIMER SYSTEM                                │
└─────────────────────────────────────────────────────────────────────────────┘

     ┌─────────────────────┐              ┌─────────────────────────────────┐
     │   PowerVision PV500 │              │    Raspberry Pi Zero 2 W        │
     │                     │              │    + Inventor HAT Mini          │
     │   ┌─────────────┐   │              │                                 │
     │   │   5" LCD    │   │              │   ┌───────────────────────┐     │
     │   │  800x480    │   │              │   │   Inventor HAT Mini   │     │
     │   └─────────────┘   │              │   │                       │     │
     │                     │              │   │  [Servo 1] [Servo 2]  │     │
     │   Digital Outputs   │              │   │     │                 │     │
     │   ┌───┐ ┌───┐       │              │   │     └──────────┐      │     │
     │   │DO1│ │DO2│ ...   │              │   │                │      │     │
     │   └─┬─┘ └───┘       │              │   │  GPIO Header   │      │     │
     │     │               │              │   │  ┌─────────┐   │      │     │
     │     │               │              │   │  │ ○ ○ ○ ○ │   │      │     │
     └─────┼───────────────┘              │   │  │ ○ ○ ○ ○ │   │      │     │
           │                              │   └──┼─────────┼───┼──────┘     │
           │                              │      │         │   │            │
           │      Level Shifter           │      │  GPIO26 │   │            │
           │      (3.3V ↔ 5V)             │      │         │   │            │
           │   ┌─────────────┐            │      │         │   │            │
           └───┤ HV      LV  ├────────────┼──────┘         │   │            │
               │ GND    GND  │            │                │   │            │
               └──────┬──────┘            └────────────────┼───┼────────────┘
                      │                                    │   │
                      └──────────────── GND ───────────────┘   │
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

## Component Pinouts

### PowerVision PV500 - Digital Output Connector

```
PV500 I/O Connector (rear)
┌─────────────────────────────┐
│  DO1+  DO1-  DO2+  DO2-  ...│
│   ●     ●     ○     ○       │
│   │     │                   │
│   │     └── Ground (connect to common GND)
│   │
│   └── Digital Output 1 (HIGH when timer running)
│        Voltage: Configurable 5V-32V
│        Current: Up to 500mA
└─────────────────────────────┘
```

### Pimoroni Inventor HAT Mini

```
Inventor HAT Mini (Top View)
┌────────────────────────────────────────────┐
│                                            │
│  ┌──────────┐        ┌──────────┐          │
│  │ SERVO 1  │        │ SERVO 2  │          │
│  │ ┌─┬─┬─┐  │        │ ┌─┬─┬─┐  │          │
│  │ │S│+│-│  │        │ │S│+│-│  │          │
│  │ └─┴─┴─┘  │        │ └─┴─┴─┘  │          │
│  └──────────┘        └──────────┘          │
│     │ │ │               │ │ │              │
│     │ │ └─ GND (Brown)  │ │ └─ GND         │
│     │ └─── 5V (Red)     │ └─── 5V          │
│     └───── Signal (Org) └───── Signal      │
│                                            │
│  ┌─────────────────────────────────────┐   │
│  │          40-pin GPIO Header         │   │
│  │  (directly maps to Pi GPIO pins)    │   │
│  │                                     │   │
│  │  Pin 37 = GPIO 26 ◄── PV500 Signal  │   │
│  │  Pin 39 = GND      ◄── Common GND   │   │
│  └─────────────────────────────────────┘   │
│                                            │
│           Inventor HAT Mini                │
└────────────────────────────────────────────┘
```

### GPIO Pin Reference (BCM Numbering)

```
Raspberry Pi GPIO Header (relevant pins)
┌────────────────────────────────────────┐
│  Physical Pin    BCM GPIO    Function  │
├────────────────────────────────────────┤
│      37           GPIO 26    Signal IN │ ◄── PV500 DO1 (via level shifter)
│      39           GND        Ground    │ ◄── Common ground
│      1            3.3V       Power     │ ◄── Level shifter LV
│      2            5V         Power     │ ◄── Level shifter HV
└────────────────────────────────────────┘
```

### GeekServo 360° Continuous

```
GeekServo 3-Wire Cable
┌─────────────────────────────┐
│  Wire Color    Connection   │
├─────────────────────────────┤
│  Red           5V Power     │ → Inventor HAT Servo 1 (+)
│  Brown         Ground       │ → Inventor HAT Servo 1 (-)
│  Orange        Signal/PWM   │ → Inventor HAT Servo 1 (S)
└─────────────────────────────┘

Note: This is a CONTINUOUS rotation servo
- PWM signal controls SPEED and DIRECTION, not position
- 0% duty cycle = full speed one direction
- 50% duty cycle = stopped
- 100% duty cycle = full speed opposite direction
```

---

## Level Shifter Wiring

**Required because:** PV500 outputs 5V-32V, Pi GPIO is 3.3V tolerant only.

### Using Bi-directional Level Shifter (e.g., BSS138-based)

```
                ┌─────────────────┐
  PV500 DO1+ ───┤ HV1         LV1 ├─── Pi GPIO 26
                │                 │
  PV500 5V   ───┤ HV          LV  ├─── Pi 3.3V
  (or ext 5V)   │                 │
                │                 │
  Common GND ───┤ GND        GND  ├─── Pi GND
                └─────────────────┘
```

### Alternative: Voltage Divider (simple, input-only)

```
                    R1 (10kΩ)
  PV500 DO1+ ───────/\/\/\───┬─── Pi GPIO 26
                              │
                    R2 (20kΩ) │
  Common GND ─────────/\/\/\──┘

  Voltage: 5V × (20k / 30k) = 3.33V ✓
```

### Alternative: Optocoupler (isolated)

```
  PV500 DO1+ ───┐
                │   ┌────────────┐
             R 330Ω │            │
                │   │  PC817     │
                ├───┤ LED    OUT ├─── Pi GPIO 26 (with pull-up)
                │   │            │
  PV500 GND ────┴───┤ GND    GND ├─── Pi GND
                    └────────────┘
```

---

## Complete Wiring Table

| From | To | Wire Color | Notes |
|------|-----|------------|-------|
| PV500 DO1+ | Level Shifter HV1 | Any | Signal wire |
| PV500 DO1- | Common GND | Black | Ground reference |
| Level Shifter LV1 | Pi GPIO 26 (Pin 37) | Any | 3.3V signal |
| Level Shifter HV | PV500 5V or external 5V | Red | High voltage reference |
| Level Shifter LV | Pi 3.3V (Pin 1) | Red | Low voltage reference |
| Level Shifter GND | Common GND | Black | Ground |
| GeekServo Red | Inventor HAT Servo 1 (+) | Red | 5V power |
| GeekServo Brown | Inventor HAT Servo 1 (-) | Brown | Ground |
| GeekServo Orange | Inventor HAT Servo 1 (S) | Orange | PWM signal |
| Pi GND (Pin 39) | Common GND | Black | System ground |

---

## Internal Pull Configuration

The Python script configures GPIO 26 with an internal **pull-down** resistor:

```python
from gpiozero import InputDevice
signal_input = InputDevice(26, pull_up=False)  # Internal pull-down enabled
```

This means:
- When PV500 DO1 is LOW (timer stopped): GPIO reads LOW (0)
- When PV500 DO1 is HIGH (timer running): GPIO reads HIGH (1)

---

## Power Requirements

| Component | Voltage | Current | Notes |
|-----------|---------|---------|-------|
| Pi Zero 2 W | 5V | ~400mA | Via micro-USB |
| Inventor HAT Mini | 5V (from Pi) | ~50mA | Servo power separate |
| GeekServo | 5V | ~200mA | Continuous rotation |
| PV500 | 9-32V DC | ~500mA | Check spec sheet |

**Servo Power Note:** The Inventor HAT Mini powers servos from its onboard regulator (5V). For high-torque servos, you may need external 5V power connected to the servo header.

---

## Troubleshooting Wiring

| Symptom | Check |
|---------|-------|
| Servo doesn't move | Verify servo connections to Inventor HAT |
| Pi doesn't detect signal | Check level shifter wiring, verify voltages |
| Erratic servo behavior | Check for common ground between all components |
| Pi GPIO damaged | Level shifter may have failed or is wired wrong |
