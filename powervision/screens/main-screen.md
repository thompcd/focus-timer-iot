# Main Screen - Focus Timer

**Resolution:** 800 x 480 (PV500)

## Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                              800px                              │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │                    "Heads down."                          │  │ 80px
│  │                    Font: Bold 36px                        │  │
│  │                    Color: #94A3B8 (muted)                 │  │
│  │                    Y: 60                                  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │                    "Be back in"                           │  │ 50px
│  │                    Font: Regular 24px                     │  │
│  │                    Color: #64748B (lighter)               │  │
│  │                    Y: 140                                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │                       5:00                                │  │ 120px
│  │                    Font: Bold 96px                        │  │
│  │                    Color: #F5F5F5 (bright)                │  │
│  │                    Variable: timer_display                │  │
│  │                    Format: "M:SS"                         │  │
│  │                    Y: 180                                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│  │    5 min    │   │   15 min    │   │   30 min    │           │ 60px
│  │  (140x60)   │   │  (140x60)   │   │  (140x60)   │           │
│  │  X: 100     │   │  X: 330     │   │  X: 560     │           │
│  │  Y: 340     │   │  Y: 340     │   │  Y: 340     │           │
│  └─────────────┘   └─────────────┘   └─────────────┘           │
│                                                                 │
│                    ┌─────────────────┐                          │
│                    │      START      │                          │ 60px
│                    │    (200x60)     │                          │
│                    │    X: 300       │                          │
│                    │    Y: 420       │                          │
│                    └─────────────────┘                          │
│                                                            480px│
└─────────────────────────────────────────────────────────────────┘
```

## Components

### Background
- **Color:** `#0A0A0A` (near black)
- **Full screen:** 800 x 480

### Label: "Heads down."
- **Type:** Static Label
- **Position:** X: 400 (centered), Y: 80
- **Size:** 400 x 50
- **Alignment:** Center
- **Font:** Bold, 36px
- **Color:** `#94A3B8`

### Label: "Be back in"
- **Type:** Static Label  
- **Position:** X: 400 (centered), Y: 150
- **Size:** 300 x 40
- **Alignment:** Center
- **Font:** Regular, 24px
- **Color:** `#64748B`

### Timer Display
- **Type:** Text Field (Dynamic)
- **Variable:** `timer_display` (string)
- **Position:** X: 400 (centered), Y: 220
- **Size:** 400 x 120
- **Alignment:** Center
- **Font:** Bold Mono, 96px
- **Color:** `#F5F5F5`
- **Default:** "5:00"

### Button: 5 min
- **Type:** Button
- **Position:** X: 100, Y: 340
- **Size:** 140 x 60
- **Label:** "5 min"
- **Font:** Bold, 18px
- **Normal State:**
  - Background: `#1E293B`
  - Border: `#334155`, 2px
  - Text: `#E2E8F0`
- **Pressed State:**
  - Background: `#334155`
- **Action:** 
  - Set `timer_seconds` = 300
  - Set `timer_display` = "5:00"

### Button: 15 min
- **Type:** Button
- **Position:** X: 330, Y: 340
- **Size:** 140 x 60
- **Label:** "15 min"
- **Font:** Bold, 18px
- **Normal State:**
  - Background: `#1E293B`
  - Border: `#334155`, 2px
  - Text: `#E2E8F0`
- **Pressed State:**
  - Background: `#334155`
- **Action:**
  - Set `timer_seconds` = 900
  - Set `timer_display` = "15:00"

### Button: 30 min
- **Type:** Button
- **Position:** X: 560, Y: 340
- **Size:** 140 x 60
- **Label:** "30 min"
- **Font:** Bold, 18px
- **Normal State:**
  - Background: `#1E293B`
  - Border: `#334155`, 2px
  - Text: `#E2E8F0`
- **Pressed State:**
  - Background: `#334155`
- **Action:**
  - Set `timer_seconds` = 1800
  - Set `timer_display` = "30:00"

### Button: START
- **Type:** Button
- **Position:** X: 300, Y: 410
- **Size:** 200 x 60
- **Label:** "START"
- **Font:** Bold, 20px
- **Visibility:** Visible when `timer_running` = 0
- **Normal State:**
  - Background: `#22C55E` (green)
  - Border: none
  - Text: `#FFFFFF`
  - Corner Radius: 8px
- **Pressed State:**
  - Background: `#16A34A`
- **Action:**
  - Set `timer_running` = 1
  - Set `digital_output_1` = 1 (HIGH)
  - Start timer script

### Button: STOP
- **Type:** Button
- **Position:** X: 300, Y: 410
- **Size:** 200 x 60
- **Label:** "STOP"
- **Font:** Bold, 20px
- **Visibility:** Visible when `timer_running` = 1
- **Normal State:**
  - Background: `#EF4444` (red)
  - Border: none
  - Text: `#FFFFFF`
  - Corner Radius: 8px
- **Pressed State:**
  - Background: `#DC2626`
- **Action:**
  - Set `timer_running` = 0
  - Set `digital_output_1` = 0 (LOW)
  - Stop timer script
  - Reset `timer_display` to selected duration

---

## Timer Script (Internal)

```
// Runs every 1 second when timer_running = 1

IF timer_seconds > 0 THEN
    timer_seconds = timer_seconds - 1
    
    // Format display
    minutes = timer_seconds / 60
    seconds = timer_seconds % 60
    timer_display = FORMAT("{0}:{1:00}", minutes, seconds)
ELSE
    // Timer expired
    timer_running = 0
    digital_output_1 = 0
    timer_display = "Done!"
    
    // Optional: play beep
    // BEEP(3)
    
    // Reset after 3 seconds
    DELAY(3000)
    timer_display = "5:00"
    timer_seconds = 300
ENDIF
```

---

## Running State UI

When `timer_running` = 1:
- START button hidden
- STOP button visible
- Timer counts down
- Quick select buttons disabled (grayed)
- Optional: pulsing border on timer display

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                      Heads down.                                │
│                                                                 │
│                    Be back in                                   │
│                                                                 │
│                     ┌─────────┐                                 │
│                     │  3:42   │  ← Counting down                │
│                     └─────────┘                                 │
│                                                                 │
│    ┌──────────┐   ┌──────────┐   ┌──────────┐                   │
│    │  5 min   │   │  15 min  │   │  30 min  │  ← Disabled       │
│    │ (grayed) │   │ (grayed) │   │ (grayed) │                   │
│    └──────────┘   └──────────┘   └──────────┘                   │
│                                                                 │
│                      ┌──────────┐                               │
│                      │   STOP   │  ← Red, visible               │
│                      └──────────┘                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
