"""
[Method 2] Image-Based Macro
Finds button images on screen and clicks them automatically.
"""

import pyautogui
import time
import sys
import os

print("=" * 45)
print("   Image-Based Auto Booking Macro")
print("=" * 45)
print()

# Base path when running as exe
BASE_DIR = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
BTN_PATH   = os.path.join(BASE_DIR, "images", "button.png")
INPUT_PATH = os.path.join(BASE_DIR, "images", "input.png")

# ── Check image files ──
if not os.path.exists(BTN_PATH):
    print("ERROR: Button image not found!")
    print(f"   Please save the image to:")
    print(f"   {BTN_PATH}")
    print()
    print("How to capture: In your browser, capture only the 'Book Now' button")
    print("                using Win+Shift+S, then save it as button.png")
    input("Press Enter to exit...")
    sys.exit()

# ── Enter name ──
name = input("Enter your name: ").strip()
if not name:
    print("Name is required.")
    input("Press Enter to exit...")
    sys.exit()

print()
print("Booking will start in 3 seconds. Switch to your browser now!")
time.sleep(3)

# ── Find name input field ──
if os.path.exists(INPUT_PATH):
    print(">> Looking for name input field...")
    loc = pyautogui.locateOnScreen(INPUT_PATH, confidence=0.8)
    if loc:
        pyautogui.click(pyautogui.center(loc))
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.typewrite(name, interval=0.05)
        print(f"  -> Name entered: {name}")
    else:
        print("  ERROR: Input field not found. Please recapture the image.")
        input("Press Enter to exit...")
        sys.exit()
else:
    print("WARNING: input.png not found -> Skipping input field click (enter name manually)")
    input("Enter your name in the input field manually, then press Enter...")

time.sleep(0.2)

# ── Find & click button ──
print(">> Looking for Book Now button...")
loc = pyautogui.locateOnScreen(BTN_PATH, confidence=0.8)
if loc:
    print(f"  -> Button found! Clicking...")
    pyautogui.click(pyautogui.center(loc))
    print()
    print("Done! Check the result in your browser.")
else:
    print("ERROR: Button not found.")
    print("  - Try recapturing button.png")
    print("  - Make sure the browser window size matches when you captured the image")

input("Press Enter to exit...")
