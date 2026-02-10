# Bill of Materials

## Core Components

| Qty | Component | Description | Approx. Cost | Link |
|-----|-----------|-------------|--------------|------|
| 1 | SenseCAP Indicator D1101 | 4" 480x480 touchscreen, ESP32-S3 | ~$50 | [Seeed Studio](https://www.seeedstudio.com/SenseCAP-Indicator-D1101-p-5648.html) |
| 1 | Raspberry Pi Zero 2 W | Quad-core ARM, WiFi, BT | ~$15 | [Pi Foundation](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) |
| 1 | Pimoroni Inventor HAT Mini | GPIO + servo headers + QW/ST | ~$22 | [Pimoroni](https://shop.pimoroni.com/products/inventor-hat-mini) |
| 1 | GeekServo 360° Continuous | 3-wire continuous rotation servo | ~$8-15 | [Amazon](https://www.amazon.com/dp/B07MQH1JFH) |

## Cables & Adapters

| Qty | Component | Description | Approx. Cost | Notes |
|-----|-----------|-------------|--------------|-------|
| 1 | Grove to Qwiic Cable | Connects SenseCAP to Inventor HAT | ~$3 | [SparkFun](https://www.sparkfun.com/products/15109) or [Seeed](https://www.seeedstudio.com/Grove-to-SparkFun-QWIIC-Cable-p-5131.html) |
| 1 | MicroSD Card | 16GB+ Class 10 | ~$8 | For Pi OS |
| 1 | USB-C Cable | For SenseCAP power | ~$5 | Included with SenseCAP |
| 1 | Micro-USB Cable | For Pi power | ~$5 | Or use GPIO power |

## Optional

| Qty | Component | Description | Approx. Cost | Notes |
|-----|-----------|-------------|--------------|-------|
| 1 | Pi Zero Case | Protective enclosure | ~$5-10 | Various styles |
| 1 | Servo Extension Cable | If needed for reach | ~$3 | Match connector type |
| 1 | 3D Printed Enclosure | Custom housing | ~$10-20 | Print or order |
| 1 | USB-C Power Supply (5V 2A) | For SenseCAP | ~$10 | If not using existing |

## Tools Needed

- Soldering iron (optional, for permanent build)
- Small screwdrivers
- Multimeter (for troubleshooting)

## Estimated Total Cost

| Scenario | Cost |
|----------|------|
| Core components only | ~$95 |
| With cables & accessories | ~$115 |

## Sourcing Notes

### SenseCAP Indicator
- Available directly from [Seeed Studio](https://www.seeedstudio.com/)
- Model D1101 includes all sensors; D1100 is display-only (cheaper)
- Check for availability and shipping times

### Grove to Qwiic Cable
- Also called "Grove to STEMMA QT" 
- Any 4-pin JST-SH to Grove cable works
- Can also make custom cable with jumper wires

### Raspberry Pi Zero 2 W
- Often in short supply
- Check Adafruit, SparkFun, PiShop.us
- Pi Zero (original) works but is slower

### GeekServo
- Also sold as "LEGO compatible continuous servo"
- Any 360° continuous rotation servo works
- Standard positional servos need code modification

## Alternative Components

| Instead of | Use | Notes |
|------------|-----|-------|
| SenseCAP D1101 | SenseCAP D1100 | No sensors, cheaper |
| Pi Zero 2 W | Pi Zero W | Slower, but works |
| Inventor HAT Mini | Direct wiring | Wire I2C to GPIO 2/3, servo to GPIO |
| GeekServo | Any 360° servo | Match voltage (5V) |
