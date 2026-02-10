# Focus Timer IoT

A sleek "heads down" focus timer system using a PowerVision PV500 HMI display and a Raspberry Pi Zero 2 W with servo-controlled physical indicator.

![Focus Timer Concept](docs/concept.png)

## Overview

When you need uninterrupted focus time, start the timer and a physical servo rotates a "Do Not Disturb" sign into view. When the timer expires, the servo returns to rest position.

### Components

| Component | Purpose |
|-----------|---------|
| **PowerVision PV500** | 5" HMI display with countdown timer UI |
| **Raspberry Pi Zero 2 W** | Reads digital signal, controls servo |
| **Pimoroni Inventor HAT Mini** | GPIO breakout with servo headers |
| **GeekServo 360° Continuous** | Rotates physical indicator |

## System Architecture

```
┌─────────────────────┐         ┌─────────────────────┐
│   PowerVision PV500 │         │  Raspberry Pi Zero  │
│                     │         │  + Inventor HAT Mini│
│  ┌───────────────┐  │  GPIO   │  ┌───────────────┐  │
│  │ Countdown     │  │ ─────►  │  │ Python Script │  │
│  │ Timer Display │  │ (HIGH/  │  │               │  │
│  │               │  │  LOW)   │  │ Servo Control │  │
│  └───────────────┘  │         │  └───────┬───────┘  │
│                     │         │          │          │
│  [5m] [15m] [30m]   │         │          ▼          │
│      [START]        │         │   ┌───────────┐     │
│                     │         │   │ GeekServo │     │
│  Digital Output ────┼─────────┼──►│  360° CW  │     │
└─────────────────────┘         │   └───────────┘     │
                                └─────────────────────┘
```

## Wiring Diagram

See [docs/wiring-diagram.md](docs/wiring-diagram.md) for complete pinout.

### Quick Reference

**PV500 Digital Output → Pi GPIO:**
```
PV500 DO1+ ────────► Pi GPIO 26 (via Inventor HAT)
PV500 DO1- ────────► Pi GND
```

**Servo Connection (Inventor HAT Mini Servo 1):**
```
Servo Red ─────────► 5V (Servo header)
Servo Brown ───────► GND (Servo header)  
Servo Orange ──────► Signal (Servo header S1)
```

## Quick Start

### 1. PowerVision PV500 Setup

1. Open PowerVision Builder
2. Import project from `powervision/focus-timer.pvproj`
3. Build and deploy to PV500

### 2. Raspberry Pi Setup

```bash
# Clone this repo
git clone https://github.com/thompcd/focus-timer-iot.git
cd focus-timer-iot/raspberry-pi

# Install dependencies
pip3 install inventorhatmini gpiozero

# Run the servo controller
python3 focus_servo.py
```

### 3. Wire It Up

Connect PV500 digital output to Pi GPIO 26 (see wiring diagram).

### 4. Test

1. Press **5m** on PV500, then **START**
2. Servo should rotate to 180°
3. When timer expires, servo returns to 0°

## Project Structure

```
focus-timer-iot/
├── README.md
├── powervision/
│   ├── focus-timer.pvproj      # PowerVision Builder project
│   ├── screens/
│   │   └── main-screen.md      # Screen layout documentation
│   └── variables.md            # Variable definitions
├── raspberry-pi/
│   ├── focus_servo.py          # Main Python script
│   ├── requirements.txt        # Python dependencies
│   └── systemd/
│       └── focus-timer.service # Auto-start service
└── docs/
    ├── wiring-diagram.md       # Complete pinout
    ├── bom.md                  # Bill of materials
    └── troubleshooting.md      # Common issues
```

## UI Preview (PV500)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                           800px │
│                                                                 │
│                      Heads down.                                │
│                                                                 │
│                   Be back in                                    │
│                                                                 │
│                     5:00                                        │
│                                                                 │
│                                                                 │
│    ┌──────────┐   ┌──────────┐   ┌──────────┐                   │
│    │   5 min  │   │  15 min  │   │  30 min  │                   │
│    └──────────┘   └──────────┘   └──────────┘                   │
│                                                                 │
│                      ┌──────────┐                               │
│                      │  START   │                               │
│                      └──────────┘                               │
│                                                           480px │
└─────────────────────────────────────────────────────────────────┘
```

## License

MIT License - See [LICENSE](LICENSE)

## Author

Corey Thompson - [Tulsa Software](https://tulsasoftware.com)
