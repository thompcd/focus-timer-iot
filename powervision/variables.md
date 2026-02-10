# PowerVision Variables

## Internal Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `timer_seconds` | Integer | 300 | Countdown value in seconds |
| `timer_display` | String | "5:00" | Formatted timer string (M:SS) |
| `timer_running` | Boolean | 0 | 1 = running, 0 = stopped |
| `selected_duration` | Integer | 300 | Currently selected preset (seconds) |

## Digital Outputs

| Output | Pin | Description |
|--------|-----|-------------|
| `digital_output_1` | DO1 | HIGH when timer running, LOW when stopped |

## Digital Output Configuration

```
Output: DO1
Type: Sourcing (PNP) or Sinking (NPN) - configure based on wiring
Voltage: 5V or 12V (match to Pi GPIO levels via level shifter if needed)
Current: Sufficient to trigger GPIO input
```

### PV500 Digital Output Specs
- **Output Type:** Configurable PNP/NPN
- **Voltage:** 5-32V DC
- **Max Current:** 500mA per output

### Connection to Raspberry Pi

**IMPORTANT:** The PV500 digital outputs are industrial-grade (5-32V). If using 12V or higher:
- Use a **voltage divider** or **level shifter** to bring signal to 3.3V for Pi GPIO
- Or configure PV500 for 5V operation and use a level shifter

**Recommended: Use 5V output with level shifter:**
```
PV500 DO1 (5V) ──► Level Shifter ──► Pi GPIO 26 (3.3V)
```

**Alternative: Optocoupler isolation:**
```
PV500 DO1+ ──► Optocoupler LED+ 
PV500 GND  ──► Optocoupler LED-
Optocoupler OUT ──► Pi GPIO 26 (with pull-up)
```

## Variable Logic

### Timer Start
```
ON START_BUTTON_PRESS:
    timer_running = 1
    digital_output_1 = 1
    // Start 1-second interval timer
```

### Timer Tick (every 1 second)
```
IF timer_running = 1:
    IF timer_seconds > 0:
        timer_seconds = timer_seconds - 1
        UPDATE timer_display
    ELSE:
        timer_running = 0
        digital_output_1 = 0
```

### Timer Stop
```
ON STOP_BUTTON_PRESS:
    timer_running = 0
    digital_output_1 = 0
    timer_seconds = selected_duration
    UPDATE timer_display
```

### Duration Selection
```
ON 5MIN_BUTTON_PRESS:
    selected_duration = 300
    timer_seconds = 300
    timer_display = "5:00"

ON 15MIN_BUTTON_PRESS:
    selected_duration = 900
    timer_seconds = 900
    timer_display = "15:00"

ON 30MIN_BUTTON_PRESS:
    selected_duration = 1800
    timer_seconds = 1800
    timer_display = "30:00"
```

## Display Format Function

```
FUNCTION format_timer(seconds):
    minutes = FLOOR(seconds / 60)
    secs = seconds MOD 60
    RETURN FORMAT("{0}:{1:00}", minutes, secs)
```

Examples:
- 300 → "5:00"
- 299 → "4:59"
- 60 → "1:00"
- 5 → "0:05"
