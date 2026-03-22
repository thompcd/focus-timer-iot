"""
Focus Timer Servo Controller
Maker Pi RP2040 firmware

Reads timer state from SenseCAP Indicator via I2C (Grove 1)
Controls servo on GP5 based on timer running/stopped

I2C Protocol (SenseCAP at address 0x42):
  Register 0x00: Status (0=stopped, 1=running)
  Register 0x01: Minutes remaining  
  Register 0x02: Seconds remaining
"""

import time
import board
import busio
import pwmio
from adafruit_motor import servo

# === Configuration ===
SENSECAP_I2C_ADDR = 0x42
SERVO_PIN = board.GP5

# Grove 1 on Maker Pi RP2040 uses GP0 (SDA) and GP1 (SCL)
I2C_SDA = board.GP0
I2C_SCL = board.GP1

# Servo positions (adjust these for your setup)
SERVO_IDLE_ANGLE = 0      # Position when timer stopped
SERVO_ACTIVE_ANGLE = 90   # Position when timer running

# === Setup ===
print("Focus Timer Servo Controller")
print("============================")

# Setup I2C
try:
    i2c = busio.I2C(I2C_SCL, I2C_SDA)
    print(f"I2C initialized on GP0/GP1")
except Exception as e:
    print(f"I2C init failed: {e}")
    i2c = None

# Setup Servo
pwm = pwmio.PWMOut(SERVO_PIN, frequency=50)
servo_motor = servo.Servo(pwm, min_pulse=500, max_pulse=2500)
print(f"Servo initialized on {SERVO_PIN}")

# Start at idle position
servo_motor.angle = SERVO_IDLE_ANGLE
print(f"Servo set to idle position: {SERVO_IDLE_ANGLE}°")

# === Helper Functions ===
def read_timer_status():
    """Read timer status from SenseCAP Indicator"""
    if i2c is None:
        return None, None, None
    
    while not i2c.try_lock():
        pass
    
    try:
        # Read register 0 (status)
        i2c.writeto(SENSECAP_I2C_ADDR, bytes([0x00]))
        result = bytearray(1)
        i2c.readfrom_into(SENSECAP_I2C_ADDR, result)
        status = result[0]
        
        # Read register 1 (minutes)
        i2c.writeto(SENSECAP_I2C_ADDR, bytes([0x01]))
        i2c.readfrom_into(SENSECAP_I2C_ADDR, result)
        minutes = result[0]
        
        # Read register 2 (seconds)
        i2c.writeto(SENSECAP_I2C_ADDR, bytes([0x02]))
        i2c.readfrom_into(SENSECAP_I2C_ADDR, result)
        seconds = result[0]
        
        return status, minutes, seconds
        
    except OSError as e:
        print(f"I2C read error: {e}")
        return None, None, None
    finally:
        i2c.unlock()

def set_servo_position(running):
    """Set servo position based on timer state"""
    if running:
        servo_motor.angle = SERVO_ACTIVE_ANGLE
    else:
        servo_motor.angle = SERVO_IDLE_ANGLE

# === Main Loop ===
print("\nStarting main loop...")
print("Polling SenseCAP for timer status...\n")

last_status = None

while True:
    status, minutes, seconds = read_timer_status()
    
    if status is not None:
        running = (status == 1)
        
        # Only update servo and print when status changes
        if status != last_status:
            if running:
                print(f"Timer STARTED - {minutes}:{seconds:02d} remaining")
                print(f"  -> Servo to {SERVO_ACTIVE_ANGLE}° (active)")
            else:
                print(f"Timer STOPPED")
                print(f"  -> Servo to {SERVO_IDLE_ANGLE}° (idle)")
            
            set_servo_position(running)
            last_status = status
        
        # Periodic status (every ~10 seconds when running)
        elif running and (int(time.monotonic()) % 10 == 0):
            print(f"  Timer: {minutes}:{seconds:02d}")
    
    else:
        if last_status is not None:
            print("Lost connection to SenseCAP")
            last_status = None
    
    time.sleep(0.5)  # Poll every 500ms
