# Troubleshooting Guide

## Common Issues

### 1. I2C Device Not Found (0x42 missing)

**Symptom:** `i2cdetect` doesn't show address 0x42

```bash
sudo i2cdetect -y 1
# Expected:
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 40: -- -- 42 -- -- -- -- -- -- -- -- -- -- -- -- --
```

**Checks:**

1. **SenseCAP running?**
   - Is the focus timer code uploaded and running?
   - Check for display showing the timer UI

2. **Cable connected?**
   - Grove connector seated on SenseCAP
   - QW/ST connector seated on Inventor HAT
   - Check for bent/damaged pins

3. **Correct cable?**
   - Grove to Qwiic adapter (not Grove to Grove)
   - Wire mapping: GND-GND, VCC-3V3, SDA-SDA, SCL-SCL

4. **I2C enabled on Pi?**
   ```bash
   sudo raspi-config
   # Interface Options → I2C → Enable
   sudo reboot
   ```

5. **Check I2C bus:**
   ```bash
   ls /dev/i2c*
   # Should show /dev/i2c-1
   ```

### 2. Servo Doesn't Move

**Symptom:** Timer starts but servo stays still.

**Checks:**

1. **Servo connections:**
   ```
   Orange → S (Signal)
   Red    → + (5V)
   Brown  → - (GND)
   ```

2. **Correct header?** Must be Servo 1 (not Servo 2)

3. **Test servo directly:**
   ```python
   from inventorhatmini import InventorHATMini
   board = InventorHATMini()
   board.servos[0].value(1.0)  # Should spin
   time.sleep(1)
   board.servos[0].value(0)    # Stop
   ```

4. **Sufficient power?** Try external 5V for servo if it stutters

### 3. SenseCAP Display Issues

**Blank/white screen:**
- Check TFT_eSPI configuration (User_Setup.h)
- Verify pin definitions match your SenseCAP model
- Try different SPI frequency

**Touch not responding:**
- SenseCAP uses capacitive touch (GT911 or FT5x06)
- May need separate touch library initialization
- Check touch I2C address conflicts

**Upload fails:**
- Hold BOOT button while clicking Upload
- Try different USB-C cable (data capable)
- Check COM port selection in IDE

### 4. Python Script Errors

**`ModuleNotFoundError: No module named 'inventorhatmini'`**
```bash
pip3 install inventorhatmini
```

**`ModuleNotFoundError: No module named 'smbus2'`**
```bash
pip3 install smbus2
```

**`OSError: [Errno 121] Remote I/O error`**
- I2C communication failure
- Check cable connections
- Verify SenseCAP is powered and running
- Try slower I2C bus speed

**`PermissionError: [Errno 13] Permission denied`**
```bash
# Add user to i2c group
sudo usermod -aG i2c $USER
# Logout and login again
```

### 5. Timer Running but Servo Wrong Direction

**For continuous servos, rotation direction depends on:**
- `value(1.0)` = full speed forward
- `value(-1.0)` = full speed reverse
- `value(0)` = stop

**To swap directions, edit `focus_servo.py`:**
```python
# In go_to_active():
self.board.servos[0].value(-1.0)  # Was 1.0

# In go_to_rest():
self.board.servos[0].value(1.0)   # Was -1.0
```

### 6. Systemd Service Won't Start

**Check status:**
```bash
sudo systemctl status focus-timer.service
sudo journalctl -u focus-timer.service -f
```

**Common fixes:**
```bash
# Reload after editing service file
sudo systemctl daemon-reload

# Check file paths
cat /etc/systemd/system/focus-timer.service

# Ensure script is executable
chmod +x ~/focus-timer-iot/raspberry-pi/focus_servo.py
```

---

## Diagnostic Commands

### Scan I2C Bus
```bash
sudo i2cdetect -y 1
```

### Test I2C Read from SenseCAP
```python
#!/usr/bin/env python3
import smbus2
import time

bus = smbus2.SMBus(1)
address = 0x42

while True:
    try:
        bus.write_byte(address, 0x00)  # Status register
        status = bus.read_byte(address)
        
        bus.write_byte(address, 0x01)  # Minutes
        mins = bus.read_byte(address)
        
        bus.write_byte(address, 0x02)  # Seconds
        secs = bus.read_byte(address)
        
        running = "RUNNING" if status else "STOPPED"
        print(f"Timer: {running} - {mins}:{secs:02d}")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(0.5)
```

### Test Servo
```python
#!/usr/bin/env python3
from inventorhatmini import InventorHATMini
import time

board = InventorHATMini()
servo = board.servos[0]

print("Testing servo...")
print("Forward 1 second")
servo.value(1.0)
time.sleep(1)

print("Stop")
servo.value(0)
time.sleep(1)

print("Reverse 1 second")
servo.value(-1.0)
time.sleep(1)

print("Stop")
servo.value(0)
print("Done!")
```

### Check GPIO/I2C Kernel Modules
```bash
lsmod | grep i2c
# Should show: i2c_bcm2835, i2c_dev
```

### View Serial Output from SenseCAP
```bash
# After connecting USB
screen /dev/ttyACM0 115200
# or
pio device monitor
```

---

## LED Debugging (Inventor HAT Mini)

Add visual feedback to the Python script:

```python
# In FocusTimerController.__init__():
self.board.leds[0].off()  # LED 1 = I2C status
self.board.leds[1].off()  # LED 2 = Timer status

# In run loop:
if self.timer.connected:
    self.board.leds[0].on()   # I2C connected
else:
    self.board.leds[0].off()  # I2C disconnected

if status and status['running']:
    self.board.leds[1].on()   # Timer running
else:
    self.board.leds[1].off()  # Timer stopped
```

---

## Factory Reset

### SenseCAP Indicator
1. Hold BOOT button
2. Press and release RESET button
3. Release BOOT button
4. Upload fresh firmware

### Raspberry Pi
```bash
# Reinstall dependencies
pip3 uninstall inventorhatmini smbus2
pip3 install inventorhatmini smbus2

# Reset I2C
sudo modprobe -r i2c_bcm2835
sudo modprobe i2c_bcm2835
```

---

## Getting Help

1. **Check logs:** `journalctl -u focus-timer.service`
2. **Serial monitor:** Both Pi and SenseCAP output debug info
3. **Simplify:** Test each component independently
4. **GitHub Issues:** Include logs, wiring photos, and component versions
