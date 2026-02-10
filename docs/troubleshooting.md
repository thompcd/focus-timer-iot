# Troubleshooting Guide

## Common Issues

### 1. Servo Doesn't Move

**Symptoms:** Timer starts on PV500, but servo stays still.

**Checks:**
1. **Servo power**: Is the servo connected to Inventor HAT Servo 1 header?
   ```
   Red wire → (+)
   Brown wire → (-)
   Orange wire → (S)
   ```

2. **Python script running?**
   ```bash
   ps aux | grep focus_servo
   ```

3. **Test servo directly:**
   ```python
   from inventorhatmini import InventorHATMini
   board = InventorHATMini()
   board.servos[0].value(1.0)  # Should rotate
   ```

4. **Check GPIO input:**
   ```python
   from gpiozero import InputDevice
   inp = InputDevice(26, pull_up=False)
   print(inp.value)  # Should be 1 when timer running
   ```

### 2. GPIO Always Reads LOW (0)

**Symptoms:** Servo never activates even when PV500 timer is running.

**Checks:**
1. **Wiring:**
   - Is PV500 DO1+ connected through level shifter to GPIO 26?
   - Is there a common ground between PV500 and Pi?

2. **Level shifter:**
   - Check HV and LV reference voltages
   - Verify GND connections

3. **PV500 output:**
   - Use multimeter to verify DO1 goes HIGH (5V+) when timer runs
   - Check PV500 digital output configuration

4. **Measure at GPIO:**
   ```bash
   # Read GPIO 26 state
   cat /sys/class/gpio/gpio26/value
   ```

### 3. GPIO Always Reads HIGH (1)

**Symptoms:** Servo is always in active position.

**Checks:**
1. **Pull configuration:** Script should use `pull_up=False`
2. **Floating input:** Ensure level shifter is properly connected
3. **Short circuit:** Check for shorts in wiring

### 4. Servo Jitters or Moves Erratically

**Symptoms:** Servo twitches instead of smooth rotation.

**Causes & Fixes:**
1. **Insufficient power:**
   - Use external 5V supply for servo
   - Ensure power supply can deliver enough current

2. **Signal noise:**
   - Add 0.1μF capacitor across servo power
   - Shorten wires
   - Use shielded cable

3. **PWM frequency:**
   - Check Inventor HAT Mini PWM settings

### 5. PV500 Timer Not Working

**Symptoms:** Display shows timer but buttons don't work.

**Checks:**
1. **Touch calibration:** Recalibrate touch screen in PV500 settings
2. **Variable initialization:** Ensure variables are defined
3. **Script errors:** Check PowerVision Builder for compile errors

### 6. Python Script Crashes

**Error: `ModuleNotFoundError: No module named 'inventorhatmini'`**
```bash
pip3 install inventorhatmini
```

**Error: `RuntimeError: Cannot determine SOC peripheral base address`**
```bash
# Enable I2C and SPI
sudo raspi-config
# Interface Options → I2C → Enable
# Interface Options → SPI → Enable
sudo reboot
```

**Error: `PermissionError: [Errno 13] Permission denied`**
```bash
# Add user to gpio group
sudo usermod -aG gpio $USER
# Logout and login again
```

### 7. Service Won't Start

**Check service status:**
```bash
sudo systemctl status focus-timer.service
sudo journalctl -u focus-timer.service -f
```

**Common fixes:**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Check file paths in service file
cat /etc/systemd/system/focus-timer.service

# Check permissions
ls -la /home/pi/focus-timer-iot/raspberry-pi/focus_servo.py
chmod +x /home/pi/focus-timer-iot/raspberry-pi/focus_servo.py
```

---

## Diagnostic Commands

### Test GPIO Input
```python
#!/usr/bin/env python3
from gpiozero import InputDevice
import time

inp = InputDevice(26, pull_up=False)
print("Monitoring GPIO 26 (Ctrl+C to exit)...")
while True:
    print(f"GPIO 26: {'HIGH' if inp.value else 'LOW'}")
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
print("Forward")
servo.value(1.0)
time.sleep(1)

print("Stop")
servo.value(0)
time.sleep(1)

print("Reverse")
servo.value(-1.0)
time.sleep(1)

print("Stop")
servo.value(0)
print("Done")
```

### Check I2C Devices
```bash
# Inventor HAT Mini uses I2C
sudo i2cdetect -y 1
```

### Monitor System Logs
```bash
# Watch for GPIO/hardware errors
dmesg -w

# Watch Python script output
sudo journalctl -u focus-timer.service -f
```

---

## LED Indicators (Inventor HAT Mini)

The Inventor HAT Mini has onboard LEDs. You can use them for debugging:

```python
# Add to focus_servo.py for visual feedback
board.leds[0].on()   # LED 1 on when signal HIGH
board.leds[0].off()  # LED 1 off when signal LOW
```

---

## Getting Help

1. **Check logs first:** Most issues are visible in `journalctl`
2. **Simplify:** Test each component independently
3. **Measure:** Use multimeter to verify voltages
4. **GitHub Issues:** File an issue with logs and wiring photos
