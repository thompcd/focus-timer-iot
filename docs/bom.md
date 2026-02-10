# Bill of Materials

## Core Components

| Qty | Component | Description | Approx. Cost | Link |
|-----|-----------|-------------|--------------|------|
| 1 | PowerVision PV500 | 5" HMI Display (800x480) | ~$300-400 | [Enovation Controls](https://www.enovationcontrols.com/displays) |
| 1 | Raspberry Pi Zero 2 W | Quad-core ARM, WiFi | ~$15 | [Pi Foundation](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) |
| 1 | Pimoroni Inventor HAT Mini | GPIO breakout with servo headers | ~$22 | [Pimoroni](https://shop.pimoroni.com/products/inventor-hat-mini) |
| 1 | GeekServo 360° Continuous | 3-wire continuous rotation servo | ~$8-15 | [Amazon](https://www.amazon.com/dp/B07MQH1JFH) |

## Electronics

| Qty | Component | Description | Approx. Cost | Notes |
|-----|-----------|-------------|--------------|-------|
| 1 | Level Shifter (Bi-directional) | 4-channel 3.3V ↔ 5V | ~$5 | BSS138 or TXB0104 based |
| 1 | MicroSD Card | 16GB+ Class 10 | ~$8 | For Pi OS |
| 1 | Micro-USB Power Supply | 5V 2.5A | ~$10 | For Pi Zero |
| 1 | Jumper Wires | Male-to-female, various | ~$5 | For prototyping |

## Optional

| Qty | Component | Description | Approx. Cost | Notes |
|-----|-----------|-------------|--------------|-------|
| 1 | Pi Zero Case | Protective enclosure | ~$5-10 | Various styles |
| 1 | Optocoupler (PC817) | For isolated signal | ~$2 | Alternative to level shifter |
| 1 | Proto Board | For permanent build | ~$5 | Solder connections |
| 1 | 3D Printed Enclosure | Custom housing | ~$10-20 | Print or order |

## Cables & Connectors

| Qty | Component | Description | Notes |
|-----|-----------|-------------|-------|
| 1 | 3-wire Servo Extension | If needed for reach | Match servo connector |
| 2 | 2-pin JST Connector | For PV500 DO connection | Or use screw terminals |
| 1 | USB-A to Micro-USB | For Pi power | Or use header power |

## Tools Needed

- Soldering iron (for permanent build)
- Wire strippers
- Multimeter (for troubleshooting)
- Small screwdrivers

## Estimated Total Cost

| Scenario | Cost |
|----------|------|
| Minimum (if you have a PV500) | ~$50 |
| Full build with new PV500 | ~$400-450 |

## Sourcing Notes

### PowerVision PV500
- Contact Enovation Controls directly for quotes
- May be available through industrial distributors
- Check eBay/surplus for used units

### Raspberry Pi Zero 2 W
- Often in short supply
- Check Adafruit, SparkFun, PiShop.us
- Pi Zero (non-W) works too but no WiFi

### GeekServo
- Also called "LEGO compatible servo"
- Any 360° continuous servo works
- Standard servos need modified code (position vs speed control)
