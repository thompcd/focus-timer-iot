#!/usr/bin/env python3
"""
Focus Timer Servo Controller
============================

Reads digital input from PowerVision PV500 and controls a GeekServo 360°
continuous rotation servo via Pimoroni Inventor HAT Mini.

When input is HIGH: Servo rotates to 180° (focus mode active)
When input is LOW:  Servo returns to 0° (rest position)

Hardware:
- Raspberry Pi Zero 2 W
- Pimoroni Inventor HAT Mini
- GeekServo 360° Continuous (3-wire)

Wiring:
- PV500 DO1 → GPIO 26 (via level shifter if needed)
- Servo → Inventor HAT Mini Servo 1 header
"""

import time
import sys

try:
    from gpiozero import InputDevice
    from inventorhatmini import InventorHATMini
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip3 install inventorhatmini gpiozero")
    sys.exit(1)

# ============================================
# Configuration
# ============================================

# GPIO pin for PV500 digital input (directly from PV500 via level shifter to 3.3V)
SIGNAL_PIN = 26

# Servo positions (for 360° continuous servo, these control direction/speed)
# Note: Continuous servos interpret position as speed/direction
# 0 = full speed one direction, 90 = stop, 180 = full speed other direction
SERVO_REST = 0        # Rest position (or stopped for continuous)
SERVO_ACTIVE = 180    # Active position (or opposite direction for continuous)

# For a CONTINUOUS servo (360°), we actually need to:
# - Run at speed to reach position, then stop
# - Use timing to determine rotation amount
ROTATION_TIME = 0.5   # Seconds to rotate (adjust based on servo speed)

# Debounce time to avoid rapid switching
DEBOUNCE_MS = 100

# ============================================
# Servo Control for Continuous Rotation Servo
# ============================================

class FocusServo:
    """Controls the focus indicator servo."""
    
    def __init__(self, board: InventorHATMini, servo_num: int = 1):
        """
        Initialize servo controller.
        
        Args:
            board: InventorHATMini instance
            servo_num: Servo port number (1 or 2)
        """
        self.board = board
        self.servo_num = servo_num
        self.current_position = "rest"
        
        # For continuous servo:
        # - Value < 0: Rotate one direction
        # - Value = 0: Stop
        # - Value > 0: Rotate other direction
        
        print(f"[SERVO] Initialized on port {servo_num}")
        self.go_to_rest()
    
    def go_to_rest(self):
        """Move servo to rest position (0°)."""
        if self.current_position == "rest":
            return
            
        print("[SERVO] Rotating to REST position (0°)")
        
        # For continuous servo: rotate backwards
        self.board.servos[self.servo_num - 1].value(-1.0)  # Full speed reverse
        time.sleep(ROTATION_TIME)
        self.board.servos[self.servo_num - 1].value(0)     # Stop
        
        self.current_position = "rest"
        print("[SERVO] At REST position")
    
    def go_to_active(self):
        """Move servo to active position (180°)."""
        if self.current_position == "active":
            return
            
        print("[SERVO] Rotating to ACTIVE position (180°)")
        
        # For continuous servo: rotate forwards
        self.board.servos[self.servo_num - 1].value(1.0)   # Full speed forward
        time.sleep(ROTATION_TIME)
        self.board.servos[self.servo_num - 1].value(0)     # Stop
        
        self.current_position = "active"
        print("[SERVO] At ACTIVE position")
    
    def stop(self):
        """Stop the servo."""
        self.board.servos[self.servo_num - 1].value(0)


# ============================================
# Main Controller
# ============================================

class FocusTimerController:
    """Main controller that monitors input and controls servo."""
    
    def __init__(self):
        print("=" * 50)
        print("Focus Timer Servo Controller")
        print("=" * 50)
        
        # Initialize Inventor HAT Mini
        print("[INIT] Initializing Inventor HAT Mini...")
        self.board = InventorHATMini()
        
        # Initialize servo
        self.servo = FocusServo(self.board, servo_num=1)
        
        # Initialize GPIO input with internal pull-down
        # (PV500 will drive HIGH when timer is running)
        print(f"[INIT] Configuring GPIO {SIGNAL_PIN} with internal pull-down...")
        self.signal_input = InputDevice(SIGNAL_PIN, pull_up=False)
        
        # Track state
        self.last_state = False
        self.last_change_time = 0
        
        print("[INIT] Ready! Waiting for signal from PV500...")
        print("-" * 50)
    
    def read_input(self) -> bool:
        """Read the digital input state with debouncing."""
        current_state = self.signal_input.value
        current_time = time.time() * 1000  # ms
        
        # Debounce
        if current_time - self.last_change_time < DEBOUNCE_MS:
            return self.last_state
        
        if current_state != self.last_state:
            self.last_change_time = current_time
            self.last_state = current_state
            
        return current_state
    
    def run(self):
        """Main loop - monitor input and control servo."""
        try:
            while True:
                signal_high = self.read_input()
                
                if signal_high:
                    # Timer is running - move to active position
                    self.servo.go_to_active()
                else:
                    # Timer stopped - return to rest
                    self.servo.go_to_rest()
                
                # Small sleep to prevent CPU spinning
                time.sleep(0.05)
                
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
