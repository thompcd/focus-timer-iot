/**
 * Focus Timer - SenseCAP Indicator D1101
 * Simplified ST7701S test
 */

#include <Arduino.h>

// ===========================================
// Pin Definitions - Based on Seeed schematic
// ===========================================

// ST7701S 3-wire SPI (directly from schematic)
#define LCD_SPI_CS   45
#define LCD_SPI_SCK  48
#define LCD_SPI_SDA  38

// Backlight - separate pin!
#define LCD_BL       -1  // Try to find via brute force

void lcd_spi_init() {
    pinMode(LCD_SPI_CS, OUTPUT);
    pinMode(LCD_SPI_SCK, OUTPUT);
    pinMode(LCD_SPI_SDA, OUTPUT);
    digitalWrite(LCD_SPI_CS, HIGH);
    digitalWrite(LCD_SPI_SCK, HIGH);
}

void lcd_spi_write_9bit(bool dc, uint8_t data) {
    digitalWrite(LCD_SPI_CS, LOW);
    delayMicroseconds(1);
    
    // First bit is DC (0=cmd, 1=data)
    digitalWrite(LCD_SPI_SCK, LOW);
    delayMicroseconds(1);
    digitalWrite(LCD_SPI_SDA, dc ? HIGH : LOW);
    delayMicroseconds(1);
    digitalWrite(LCD_SPI_SCK, HIGH);
    delayMicroseconds(1);
    
    // Then 8 bits of data, MSB first
    for (int i = 7; i >= 0; i--) {
        digitalWrite(LCD_SPI_SCK, LOW);
        delayMicroseconds(1);
        digitalWrite(LCD_SPI_SDA, (data >> i) & 0x01 ? HIGH : LOW);
        delayMicroseconds(1);
        digitalWrite(LCD_SPI_SCK, HIGH);
        delayMicroseconds(1);
    }
    
    digitalWrite(LCD_SPI_CS, HIGH);
    delayMicroseconds(1);
}

#define LCD_CMD(x)  lcd_spi_write_9bit(false, x)
#define LCD_DATA(x) lcd_spi_write_9bit(true, x)

// Minimal ST7701S init
void st7701_init() {
    Serial.println("ST7701S init...");
    lcd_spi_init();
    delay(100);
    
    // Software Reset
    LCD_CMD(0x01);
    delay(150);
    
    // Sleep Out
    LCD_CMD(0x11);
    delay(150);
    
    // Normal Display Mode On
    LCD_CMD(0x13);
    delay(10);
    
    // Display Inversion Off
    LCD_CMD(0x20);
    delay(10);
    
    // Interface Pixel Format - 16bit/pixel
    LCD_CMD(0x3A);
    LCD_DATA(0x55);  // RGB565
    delay(10);
    
    // Display On
    LCD_CMD(0x29);
    delay(50);
    
    Serial.println("ST7701S basic init done!");
}

void setup() {
    Serial.begin(115200);
    delay(2000);
    
    Serial.println("\n========================================");
    Serial.println("SenseCAP Indicator - ST7701S Test v2");
    Serial.println("========================================\n");
    
    // Initialize ST7701S via SPI
    st7701_init();
    
    Serial.println("\nST7701S should now be ready for RGB signals.");
    Serial.println("If screen is still black, RGB panel setup needed.");
    Serial.println("\nBacklight test - trying different pins:");
    
    // Try various pins for backlight
    int test_pins[] = {45, 46, 48, 38, 47, 21, 20, 19, 4, 5, 6, 7};
    int num_pins = sizeof(test_pins) / sizeof(test_pins[0]);
    
    for (int i = 0; i < num_pins; i++) {
        int pin = test_pins[i];
        // Skip SPI pins we're using
        if (pin == LCD_SPI_CS || pin == LCD_SPI_SCK || pin == LCD_SPI_SDA) {
            continue;
        }
        pinMode(pin, OUTPUT);
        digitalWrite(pin, HIGH);
        Serial.printf("  Trying GPIO %d HIGH...\n", pin);
        delay(500);
    }
    
    Serial.println("\nAll test pins set HIGH.");
}

void loop() {
    // Just keep serial alive
    static int count = 0;
    if (count % 10 == 0) {
        Serial.printf("Tick %d - Display should show something if RGB is wired correctly\n", count);
    }
    count++;
    delay(1000);
}
