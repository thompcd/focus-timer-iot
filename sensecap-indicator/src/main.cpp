/**
 * Focus Timer - SenseCAP Indicator
 * =================================
 * 
 * Displays a minimalist countdown timer with quick-select buttons.
 * Communicates timer state via I2C to Raspberry Pi.
 * 
 * Hardware: SenseCAP Indicator D1101 (ESP32-S3 + 4" 480x480 touch LCD)
 * 
 * I2C Protocol:
 * - Device Address: 0x42
 * - Register 0x00: Timer status (0 = stopped, 1 = running)
 * - Register 0x01: Minutes remaining (0-99)
 * - Register 0x02: Seconds remaining (0-59)
 */

#include <Arduino.h>
#include <Wire.h>
#include <TFT_eSPI.h>
#include <lvgl.h>

// ===========================================
// Configuration
// ===========================================

#define I2C_ADDRESS 0x42          // I2C slave address for Pi communication
#define I2C_SDA_PIN 39            // Grove I2C SDA (check your indicator model)
#define I2C_SCL_PIN 40            // Grove I2C SCL

#define SCREEN_WIDTH 480
#define SCREEN_HEIGHT 480

// Colors (dark theme)
#define COLOR_BG        0x0000    // Black
#define COLOR_TEXT      0xF7BE    // Light gray (#F5F5F5)
#define COLOR_TEXT_DIM  0x9492    // Muted gray (#94A3B8)
#define COLOR_TEXT_DARK 0x6B4D    // Darker gray (#64748B)
#define COLOR_BTN_BG    0x1926    // Dark blue-gray (#1E293B)
#define COLOR_BTN_BORDER 0x3186   // Border (#334155)
#define COLOR_GREEN     0x2E89    // Green (#22C55E)
#define COLOR_RED       0xE8E4    // Red (#EF4444)

// ===========================================
// Global State
// ===========================================

TFT_eSPI tft = TFT_eSPI();

// Timer state
volatile uint16_t timerSeconds = 300;    // Current countdown value
volatile uint16_t selectedDuration = 300; // Selected preset
volatile bool timerRunning = false;
volatile bool stateChanged = true;        // Flag to trigger redraw

// I2C registers (read by Pi)
volatile uint8_t i2cRegisters[3] = {0, 5, 0}; // [status, minutes, seconds]

// Timing
unsigned long lastTickMs = 0;
unsigned long lastTouchMs = 0;

// Touch regions
struct TouchRegion {
    int16_t x, y, w, h;
};

TouchRegion btn5min = {40, 320, 120, 60};
TouchRegion btn15min = {180, 320, 120, 60};
TouchRegion btn30min = {320, 320, 120, 60};
TouchRegion btnStart = {140, 400, 200, 60};

// ===========================================
// I2C Slave Handlers
// ===========================================

volatile uint8_t i2cRegisterIndex = 0;

void onI2CRequest() {
    // Pi is reading data
    Wire.write(i2cRegisters[i2cRegisterIndex]);
}

void onI2CReceive(int numBytes) {
    // Pi is writing (register select)
    if (numBytes > 0) {
        i2cRegisterIndex = Wire.read();
        if (i2cRegisterIndex > 2) i2cRegisterIndex = 0;
    }
}

void updateI2CRegisters() {
    uint8_t mins = timerSeconds / 60;
    uint8_t secs = timerSeconds % 60;
    
    noInterrupts();
    i2cRegisters[0] = timerRunning ? 1 : 0;
    i2cRegisters[1] = mins;
    i2cRegisters[2] = secs;
    interrupts();
}

// ===========================================
// Display Functions
// ===========================================

void drawBackground() {
    tft.fillScreen(COLOR_BG);
}

void drawStaticText() {
    // "Heads down."
    tft.setTextColor(COLOR_TEXT_DIM, COLOR_BG);
    tft.setTextDatum(TC_DATUM);
    tft.setTextSize(2);
    tft.drawString("Heads down.", SCREEN_WIDTH / 2, 60);
    
    // "Be back in"
    tft.setTextColor(COLOR_TEXT_DARK, COLOR_BG);
    tft.setTextSize(1);
    tft.drawString("Be back in", SCREEN_WIDTH / 2, 120);
}

void drawTimer() {
    // Format time as M:SS or MM:SS
    char timeStr[8];
    uint8_t mins = timerSeconds / 60;
    uint8_t secs = timerSeconds % 60;
    sprintf(timeStr, "%d:%02d", mins, secs);
    
    // Clear timer area
    tft.fillRect(40, 160, 400, 100, COLOR_BG);
    
    // Draw timer
    tft.setTextColor(COLOR_TEXT, COLOR_BG);
    tft.setTextDatum(TC_DATUM);
    tft.setTextSize(6);
    tft.drawString(timeStr, SCREEN_WIDTH / 2, 180);
}

void drawButton(TouchRegion &btn, const char* label, uint16_t bgColor, uint16_t textColor, bool border = true) {
    // Background
    tft.fillRoundRect(btn.x, btn.y, btn.w, btn.h, 8, bgColor);
    
    // Border
    if (border) {
        tft.drawRoundRect(btn.x, btn.y, btn.w, btn.h, 8, COLOR_BTN_BORDER);
    }
    
    // Label
    tft.setTextColor(textColor, bgColor);
    tft.setTextDatum(MC_DATUM);
    tft.setTextSize(2);
    tft.drawString(label, btn.x + btn.w / 2, btn.y + btn.h / 2);
}

void drawDurationButtons() {
    uint16_t bg5 = (selectedDuration == 300) ? COLOR_BTN_BORDER : COLOR_BTN_BG;
    uint16_t bg15 = (selectedDuration == 900) ? COLOR_BTN_BORDER : COLOR_BTN_BG;
    uint16_t bg30 = (selectedDuration == 1800) ? COLOR_BTN_BORDER : COLOR_BTN_BG;
    
    // Disable appearance when running
    uint16_t textColor = timerRunning ? COLOR_TEXT_DARK : COLOR_TEXT;
    
    drawButton(btn5min, "5 min", bg5, textColor);
    drawButton(btn15min, "15 min", bg15, textColor);
    drawButton(btn30min, "30 min", bg30, textColor);
}

void drawStartStopButton() {
    // Clear button area
    tft.fillRect(btnStart.x - 10, btnStart.y - 5, btnStart.w + 20, btnStart.h + 10, COLOR_BG);
    
    if (timerRunning) {
        drawButton(btnStart, "STOP", COLOR_RED, COLOR_TEXT, false);
    } else {
        drawButton(btnStart, "START", COLOR_GREEN, COLOR_TEXT, false);
    }
}

void fullRedraw() {
    drawBackground();
    drawStaticText();
    drawTimer();
    drawDurationButtons();
    drawStartStopButton();
}

// ===========================================
// Touch Handling
// ===========================================

bool inRegion(int16_t x, int16_t y, TouchRegion &r) {
    return (x >= r.x && x < r.x + r.w && y >= r.y && y < r.y + r.h);
}

void handleTouch(int16_t x, int16_t y) {
    // Debounce
    if (millis() - lastTouchMs < 200) return;
    lastTouchMs = millis();
    
    // Duration buttons (only when stopped)
    if (!timerRunning) {
        if (inRegion(x, y, btn5min)) {
            selectedDuration = 300;
            timerSeconds = 300;
            stateChanged = true;
            return;
        }
        if (inRegion(x, y, btn15min)) {
            selectedDuration = 900;
            timerSeconds = 900;
            stateChanged = true;
            return;
        }
        if (inRegion(x, y, btn30min)) {
            selectedDuration = 1800;
            timerSeconds = 1800;
            stateChanged = true;
            return;
        }
    }
    
    // Start/Stop button
    if (inRegion(x, y, btnStart)) {
        if (timerRunning) {
            // Stop
            timerRunning = false;
            timerSeconds = selectedDuration;
        } else {
            // Start
            timerRunning = true;
            lastTickMs = millis();
        }
        stateChanged = true;
    }
}

// ===========================================
// Timer Logic
// ===========================================

void tickTimer() {
    if (!timerRunning) return;
    
    unsigned long now = millis();
    if (now - lastTickMs >= 1000) {
        lastTickMs = now;
        
        if (timerSeconds > 0) {
            timerSeconds--;
            stateChanged = true;
        } else {
            // Timer expired
            timerRunning = false;
            timerSeconds = selectedDuration;
            stateChanged = true;
            
            // Optional: beep or flash
        }
    }
}

// ===========================================
// Setup & Loop
// ===========================================

void setup() {
    Serial.begin(115200);
    Serial.println("Focus Timer - SenseCAP Indicator");
    
    // Initialize I2C as slave
    Wire.begin(I2C_ADDRESS, I2C_SDA_PIN, I2C_SCL_PIN, 100000);
    Wire.onRequest(onI2CRequest);
    Wire.onReceive(onI2CReceive);
    Serial.printf("I2C slave started at address 0x%02X\n", I2C_ADDRESS);
    
    // Initialize display
    tft.init();
    tft.setRotation(0);
    tft.fillScreen(COLOR_BG);
    
    // Initial draw
    fullRedraw();
    
    Serial.println("Ready!");
}

void loop() {
    // Update timer
    tickTimer();
    
    // Update I2C registers
    updateI2CRegisters();
    
    // Handle touch
    uint16_t x, y;
    if (tft.getTouch(&x, &y)) {
        handleTouch(x, y);
    }
    
    // Redraw if needed
    if (stateChanged) {
        stateChanged = false;
        drawTimer();
        drawDurationButtons();
        drawStartStopButton();
    }
    
    // Small delay to prevent CPU spinning
    delay(10);
}
