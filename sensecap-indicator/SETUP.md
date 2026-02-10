# SenseCAP Indicator Setup Guide

## Hardware

**SenseCAP Indicator D1101** (or D1100)
- ESP32-S3 dual-core processor
- 4" 480x480 IPS touchscreen (ST7701S driver)
- Grove connectors (I2C compatible)
- USB-C for programming

## Option 1: Arduino IDE

### 1. Install Arduino IDE

Download from [arduino.cc](https://www.arduino.cc/en/software)

### 2. Add ESP32-S3 Board Support

1. Open **File → Preferences**
2. Add to "Additional Board Manager URLs":
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Open **Tools → Board → Board Manager**
4. Search "esp32" and install **esp32 by Espressif Systems** (v2.0.11+)

### 3. Install Libraries

**Tools → Manage Libraries**, install:
- **TFT_eSPI** by Bodmer (v2.5.0+)
- **lvgl** by LVGL (v8.3.x) — optional, for advanced UI

### 4. Configure TFT_eSPI

The SenseCAP Indicator uses an ST7701S display. You need to configure TFT_eSPI:

1. Find your Arduino libraries folder:
   - Windows: `Documents\Arduino\libraries\TFT_eSPI`
   - Mac: `~/Documents/Arduino/libraries/TFT_eSPI`
   - Linux: `~/Arduino/libraries/TFT_eSPI`

2. Edit `User_Setup.h` or create `User_Setup_Select.h`:

```cpp
// User_Setup.h for SenseCAP Indicator

#define ST7701_DRIVER

#define TFT_WIDTH  480
#define TFT_HEIGHT 480

// ESP32-S3 pins for SenseCAP Indicator
#define TFT_MOSI 11
#define TFT_SCLK 12
#define TFT_CS   10
#define TFT_DC   8
#define TFT_RST  3
#define TFT_BL   46  // Backlight

#define TOUCH_CS -1  // Capacitive touch, not SPI

#define LOAD_GLCD
#define LOAD_FONT2
#define LOAD_FONT4
#define LOAD_FONT6
#define LOAD_FONT7
#define LOAD_FONT8
#define LOAD_GFXFF

#define SMOOTH_FONT

#define SPI_FREQUENCY  40000000
#define SPI_READ_FREQUENCY  20000000
#define SPI_TOUCH_FREQUENCY  2500000
```

**Note:** Pin numbers may vary by SenseCAP Indicator revision. Check Seeed documentation.

### 5. Select Board Settings

**Tools menu:**
- **Board:** ESP32S3 Dev Module
- **USB CDC On Boot:** Enabled
- **Flash Size:** 8MB
- **Partition Scheme:** 8MB with spiffs
- **PSRAM:** OPI PSRAM
- **Upload Speed:** 921600
- **Port:** (select your USB port)

### 6. Upload Code

1. Copy contents of `src/main.cpp` to Arduino IDE
2. Click **Upload** (→ button)
3. Open **Serial Monitor** (115200 baud) to verify

---

## Option 2: PlatformIO (Recommended)

### 1. Install PlatformIO

- Install [VS Code](https://code.visualstudio.com/)
- Install PlatformIO extension from VS Code marketplace

### 2. Open Project

1. Open VS Code
2. **File → Open Folder** → select `sensecap-indicator/`
3. PlatformIO will auto-detect `platformio.ini`

### 3. Configure TFT_eSPI

Create `lib/TFT_eSPI/User_Setup.h` with the configuration above, or use build flags.

### 4. Build & Upload

Click the PlatformIO icons in the bottom toolbar:
- **✓ Build** - Compile the project
- **→ Upload** - Flash to device
- **🔌 Serial Monitor** - View output

Or use terminal:
```bash
cd sensecap-indicator
pio run -t upload
pio device monitor
```

---

## Option 3: Seeed Studio Arduino Library (Easiest)

Seeed provides a dedicated library for the SenseCAP Indicator:

### 1. Install Seeed Board Package

Add to Arduino Board Manager URLs:
```
https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json
```

### 2. Install Seeed Indicator Library

1. Download from [Seeed GitHub](https://github.com/Seeed-Solution/SenseCAP_Indicator_ESP32)
2. **Sketch → Include Library → Add .ZIP Library**

### 3. Use Seeed Examples

The library includes display and touch examples that work out-of-box.

---

## I2C Connection

The SenseCAP Indicator has a **Grove connector** for I2C:

```
Grove Connector (on SenseCAP Indicator)
┌─────────────────┐
│  ●   ●   ●   ●  │
│ GND VCC SDA SCL │
└─────────────────┘
      │   │   │
      │   │   └── I2C Clock (GPIO 40)
      │   └────── I2C Data  (GPIO 39)
      └────────── 3.3V
```

Connect to Inventor HAT Mini QW/ST (Qwiic) connector:
```
Grove (SenseCAP)     QW/ST (Inventor HAT)
    GND  ───────────────  GND (Black)
    VCC  ───────────────  3.3V (Red)
    SDA  ───────────────  SDA (Blue)
    SCL  ───────────────  SCL (Yellow)
```

**Cable:** Use a Grove-to-Qwiic adapter cable, or wire directly.

---

## Verify Upload

After uploading, you should see on the display:
- "Heads down." text
- "Be back in" subtitle
- "5:00" timer
- Three duration buttons (5, 15, 30 min)
- Green START button

Serial monitor output:
```
Focus Timer - SenseCAP Indicator
I2C slave started at address 0x42
Ready!
```

---

## Troubleshooting

### Display is white/blank
- Check TFT_eSPI pin configuration
- Verify backlight pin is correct
- Try different SPI frequency

### Touch not working
- SenseCAP uses capacitive touch (FT5x06 or GT911)
- May need additional touch library
- Check touch I2C address

### I2C not responding
- Verify Grove connector wiring
- Check I2C address (0x42)
- Use `i2cdetect` on Pi to scan

### Upload fails
- Hold BOOT button while clicking Upload
- Try different USB-C cable
- Check COM port selection

---

## Pin Reference (SenseCAP Indicator D1101)

| Function | GPIO | Notes |
|----------|------|-------|
| LCD MOSI | 11 | SPI data |
| LCD SCLK | 12 | SPI clock |
| LCD CS | 10 | Chip select |
| LCD DC | 8 | Data/Command |
| LCD RST | 3 | Reset |
| LCD BL | 46 | Backlight PWM |
| Touch SDA | 39 | I2C (shared with Grove) |
| Touch SCL | 40 | I2C (shared with Grove) |
| Grove SDA | 39 | I2C to Pi |
| Grove SCL | 40 | I2C to Pi |
| USB D+ | 20 | USB CDC |
| USB D- | 19 | USB CDC |

**Note:** Pins may differ on D1100 or other variants. Check Seeed wiki.
