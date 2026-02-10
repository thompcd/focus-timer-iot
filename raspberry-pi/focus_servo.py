#!/usr/bin/env python3
"""
Focus Timer Servo Controller
============================

Reads timer state via I2C from SenseCAP Indicator and controls a GeekServo 360°
continuous rotation servo via Pimoroni Inventor HAT Mini.

I2C Protocol (SenseCAP as slave):
- Address: 0x42
- Register 0x00: Timer status (0 = stopped, 1 = running)
- Register 0x01: Minutes remaining
- Register 0x02: Seconds remaining

When timer is running: Servo rotates to 180° (focus mode active)
When timer is stopped: Servo returns to 0° (rest position)

Hardware:
- Raspberry Pi Zero 2 W
- Pimoroni Inventor HAT Mini (QW/ST connector for I2C)
- SenseCAP Indicator D1101 (via I2C)
- GeekServo 360° Continuous (3-wire)

Wiring:
- SenseCAP Grove → Inventor HAT QW/ST (Qwiic) connector
- Servo → Inventor HAT Mini Servo 1 header
"""

import time
import sys

try:
    import smbus2
    from inventorhatmini import InventorHATMini
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip3 install inventorhatmini smbus2")
    sys.exit(1)

# ============================================
# Configuration
# ============================================

# I2C address of SenseCAP Indicator
I2C_ADDRESS = 0x42
I2C_BUS = 1  # /dev/i2c-1 on Raspberry Pi

# I2C register addresses
REG_STATUS = 0x00   # 0 = stopped, 1 = running
REG_MINUTES = 0x01  # Minutes remaining
REG_SECONDS = 0x02  # Seconds remaining

# Servo timing for continuous rotation servo
ROTATION_TIME = 0.5  # Seconds to rotate (adjust based on servo speed)

# Polling interval
POLL_INTERVAL_MS = 100

# ============================================
# I2C Communication
# ============================================

class SenseCapTimer:
    """Reads timer state from SenseCAP Indicator via I2C."""
    
    def __init__(self, bus_num: int = I2C_BUS, address: int = I2C_ADDRESS):
        self.address = address
        self.bus = None
        self.connected = False
        
        try:
            self.bus = smbus2.SMBus(bus_num)
            # Test connection
            self._read_register(REG_STATUS)
            self.connected = True
            print(f"[I2C] Connected to SenseCAP at 0x{address:02X}")
        except Exception as e:
            print(f"[I2C] Failed to connect: {e}")
            print("[I2C] Will retry on each read...")
    
    def _read_register(self, register: int) -> int:
        """Read a single byte from a register."""
        # Write register address, then read one byte
        self.bus.write_byte(self.address, register)
        time.sleep(0.001)  # Small delay for I2C
        return self.bus.read_byte(self.address)
    
    def get_status(self) -> dict:
        """
        Get current timer status.
        
        Returns:
            dict with keys: running (bool), minutes (int), seconds (int)
            Returns None if communication fails.
        """
        try:
            status = self._read_register(REG_STATUS)
            minutes = self._read_register(REG_MINUTES)
            seconds = self._read_register(REG_SECONDS)
            
            if not self.connected:
                self.connected = True
                print("[I2C] Connection restored")
            
            return {
                'running': status == 1,
                'minutes': minutes,
                'seconds': seconds
            }
        except Exception as e:
            if self.connected:
                print(f"[I2C] Communication error: {e}")
                self.connected = False
            return None


# ============================================
# Servo Control
# ============================================

class FocusServo:
    """Controls the focus indicator servo."""
    
    def __init__(self, board: InventorHATMini, servo_num: int = 1):
        self.board = board
        self.servo_num = servo_num
        self.current_position = "unknown"
        
        print(f"[SERVO] Initialized on port {servo_num}")
        self.go_to_rest()
    
    def go_to_rest(self):
        """Move servo to rest position (0°)."""
        if self.current_position == "rest":
            return
            
        print("[SERVO] Rotating to REST position")
        
        # For continuous servo: rotate backwards
        self.board.servos[self.servo_num - 1].value(-1.0)
        time.sleep(ROTATION_TIME)
        self.board.servos[self.servo_num - 1].value(0)  # Stop
        
        self.current_position = "rest"
    
    def go_to_active(self):
        """Move servo to active position (180°)."""
        if self.current_position == "active":
            return
            
        print("[SERVO] Rotating to ACTIVE position")
        
        # For continuous servo: rotate forwards
        self.board.servos[self.servo_num - 1].value(1.0)
        time.sleep(ROTATION_TIME)
        self.board.servos[self.servo_num - 1].value(0)  # Stop
        
        self.current_position = "active"
    
    def stop(self):
        """Stop the servo."""
        self.board.servos[self.servo_num - 1].value(0)


# ============================================
# Main Controller
# ============================================

class FocusTimerController:
    """Main controller that polls I2C and controls servo."""
    
    def __init__(self):
        print("=" * 50)
        print("Focus Timer Servo Controller (I2C)")
        print("=" * 50)
        
        # Initialize Inventor HAT Mini
        print("[INIT] Initializing Inventor HAT Mini...")
        self.board = InventorHATMini()
        
        # Initialize servo
        self.servo = FocusServo(self.board, servo_num=1)
        
        # Initialize I2C connection to SenseCAP
        print(f"[INIT] Connecting to SenseCAP at I2C address 0x{I2C_ADDRESS:02X}...")
        self.timer = SenseCapTimer()
        
        # Track last known state
        self.last_running = False
        
        print("[INIT] Ready! Polling SenseCAP for timer state...")
        print("-" * 50)
    
    def run(self):
        """Main loop - poll I2C and control servo."""
        try:
            while True:
                # Read timer status
                status = self.timer.get_status()
                
                if status is not None:
                    running = status['running']
                    
                    # State change detection
                    if running != self.last_running:
                        mins = status['minutes']
                        secs = status['seconds']
                        
                        if running:
                            print(f"[TIMER] Started: {mins}:{secs:02d} remaining")
                            self.servo.go_to_active()
                        else:
                            print("[TIMER] Stopped")
                            self.servo.go_to_rest()
                        
                        self.last_running = running
                
                # Poll interval
                time.sleep(POLL_INTERVAL_MS / 1000)
                
        except KeyboardInterrupt:
            print("\n[EXIT] Shutting down...")
            self.servo.go_to_rest()
            self.servo.stop()
            print("[EXIT] Done.")


# ============================================
# Entry Point
# ============================================

if __name__ == "__main__":
    controller = FocusTimerController()
    controller.run()
