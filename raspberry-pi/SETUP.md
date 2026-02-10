# Raspberry Pi Setup Guide

## 1. Flash Raspberry Pi OS

1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Flash **Raspberry Pi OS Lite (64-bit)** to microSD card
3. Configure WiFi and SSH in imager settings (gear icon)

## 2. First Boot & Update

```bash
# SSH into Pi
ssh pi@raspberrypi.local

# Update system
sudo apt update && sudo apt upgrade -y

# Enable I2C and SPI (required for Inventor HAT Mini)
sudo raspi-config
# → Interface Options → I2C → Enable
# → Interface Options → SPI → Enable
sudo reboot
```

## 3. Install Dependencies

```bash
# Install Python packages
sudo apt install -y python3-pip python3-dev

# Install Inventor HAT Mini library
pip3 install inventorhatmini gpiozero

# Verify installation
python3 -c "from inventorhatmini import InventorHATMini; print('OK')"
```

## 4. Clone Repository

```bash
cd ~
git clone https://github.com/thompcd/focus-timer-iot.git
cd focus-timer-iot/raspberry-pi
```

## 5. Test the Script

```bash
# Run manually first
python3 focus_servo.py

# You should see:
# ==================================================
# Focus Timer Servo Controller
# ==================================================
# [INIT] Initializing Inventor HAT Mini...
# [SERVO] Initialized on port 1
# [SERVO] Rotating to REST position (0°)
# [INIT] Ready! Waiting for signal from PV500...
```

## 6. Install as Service (Auto-Start)

```bash
# Copy service file
sudo cp systemd/focus-timer.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start
sudo systemctl enable focus-timer.service
sudo systemctl start focus-timer.service

# Check status
sudo systemctl status focus-timer.service
```

## 7. View Logs

```bash
# Real-time logs
sudo journalctl -u focus-timer.service -f

# Recent logs
sudo journalctl -u focus-timer.service --since "10 minutes ago"
```

## 8. Hardware Connections

Connect components as per [wiring diagram](../docs/wiring-diagram.md):

1. **Attach Inventor HAT Mini** to Pi GPIO header
2. **Connect servo** to Servo 1 header (Red=+, Brown=-, Orange=S)
3. **Connect PV500 signal** via level shifter to GPIO 26

## 9. Verify Everything

```bash
# Check I2C (should see device at 0x17 or similar)
sudo i2cdetect -y 1

# Check GPIO
cat /sys/class/gpio/gpio26/value
```

## Troubleshooting

See [troubleshooting guide](../docs/troubleshooting.md) for common issues.

## Useful Commands

```bash
# Stop service
sudo systemctl stop focus-timer.service

# Restart service
sudo systemctl restart focus-timer.service

# Disable auto-start
sudo systemctl disable focus-timer.service

# Run script manually (for debugging)
python3 ~/focus-timer-iot/raspberry-pi/focus_servo.py
```
