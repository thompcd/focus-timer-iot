# Focus Timer IoT

A sleek "heads down" focus timer system using a **SenseCAP Indicator** touchscreen display and a **Raspberry Pi Zero 2 W** with servo-controlled physical indicator.

## Overview

When you need uninterrupted focus time, start the timer and a physical servo rotates a "Do Not Disturb" sign into view. When the timer expires, the servo returns to rest position.

### Components

| Component | Purpose |
|-----------|---------|
| **SenseCAP Indicator D1101** | 4" touchscreen with ESP32-S3 |
| **Raspberry Pi Zero 2 W** | Reads I2C, controls servo |
| **Pimoroni Inventor HAT Mini** | QW/ST (Qwiic) I2C + servo headers |
| **GeekServo 360° Continuous** | Rotates physical indicator |

## System Architecture

```
┌─────────────────────┐    I2C    ┌─────────────────────┐
│  SenseCAP Indicator │  ─────►  │  Raspberry Pi Zero  │
│                     │  (QW/ST) │  + Inventor HAT Mini│
│  ┌───────────────┐  │          │                     │
│  │ Countdown     │  │          │  Python script      │
│  │ Timer Display │  │          │  polls I2C status   │
│  │               │  │          │                     │
│  │   "5:00"      │  │          │  Controls servo     │
│  └───────────────┘  │          │  based on timer     │
│                     │          │                     │
│  [5m] [15m] [30m]   │          │      ┌───────┐      │
│      [START]        │          │      │ Servo │      │
│                     │          │      └───────┘      │
│  Grove ──► I2C ─────┼──────────┼──► QW/ST            │
└─────────────────────┘          └─────────────────────┘

I2C Address: 0x42
Registers: [status, minutes, seconds]
```

## UI Preview (SenseCAP Indicator)

```
┌─────────────────────────────────────────┐
│                                   480px │
│                                         │
│            Heads down.                  │
│                                         │
│           Be back in                    │
│                                         │
│              5:00                       │
│                                         │
│    ┌────────┐ ┌────────┐ ┌────────┐     │
│    │  5 min │ │ 15 min │ │ 30 min │     │
│    └────────┘ └────────┘ └────────┘     │
│                                         │
│           ┌────────────┐                │
│           │   START    │                │
│           └────────────┘                │
│                                   480px │
└─────────────────────────────────────────┘
```

## Quick Start

### 1. Flash SenseCAP Indicator

See [sensecap-indicator/SETUP.md](sensecap-indicator/SETUP.md) for detailed instructions.

**Quick version (PlatformIO):**
```bash
cd sensecap-indicator
pio run -t upload
```

### 2. Setup Raspberry Pi

```bash
# Clone this repo
git clone https://github.com/thompcd/focus-timer-iot.git
cd focus-timer-iot/raspberry-pi

# Install dependencies
pip3 install inventorhatmini smbus2

# Run the controller
python3 focus_servo.py
```

### 3. Wire It Up

Connect SenseCAP Grove → Inventor HAT QW/ST (Qwiic):

| SenseCAP Grove | Inventor HAT QW/ST |
|----------------|-------------------|
| GND (Black) | GND (Black) |
| VCC (Red) | 3V3 (Red) |
| SDA (White) | SDA (Blue) |
| SCL (Yellow) | SCL (Yellow) |

Connect servo to Inventor HAT Servo 1 header.

See [docs/wiring-diagram.md](docs/wiring-diagram.md) for complete pinouts.

### 4. Test

1. Power on both devices
2. Press **5 min** on SenseCAP, then **START**
3. Servo should rotate to active position
4. When timer expires (or press **STOP**), servo returns to rest

## Project Structure

```
focus-timer-iot/
├── README.md
├── sensecap-indicator/
│   ├── src/main.cpp        # ESP32-S3 Arduino code
│   ├── platformio.ini      # PlatformIO configuration
│   └── SETUP.md            # Upload instructions
├── raspberry-pi/
│   ├── focus_servo.py      # Python I2C + servo controller
│   ├── requirements.txt    # Python dependencies
│   ├── SETUP.md            # Pi setup guide
│   └── systemd/
│       └── focus-timer.service
└── docs/
    ├── wiring-diagram.md   # Complete pinouts
    ├── bom.md              # Bill of materials
    └── troubleshooting.md  # Common issues
```

## I2C Protocol

The SenseCAP Indicator acts as an I2C slave (address `0x42`):

| Register | Address | Description |
|----------|---------|-------------|
| STATUS | 0x00 | 0 = stopped, 1 = running |
| MINUTES | 0x01 | Minutes remaining (0-99) |
| SECONDS | 0x02 | Seconds remaining (0-59) |

The Pi polls these registers and controls the servo accordingly.

## Verify I2C Connection

```bash
# On Raspberry Pi
sudo i2cdetect -y 1

# Should show:
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 40: -- -- 42 -- -- -- -- -- -- -- -- -- -- -- -- --
```

## License

MIT License - See [LICENSE](LICENSE)

## Author

Corey Thompson - [Tulsa Software](https://tulsasoftware.com)
