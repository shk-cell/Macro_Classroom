"""
[Method 1] Coordinate-Based Macro
Clicks on screen elements using fixed X, Y coordinates.
"""

import pyautogui
import time
import sys

print("=" * 45)
print("   Coordinate-Based Auto Booking Macro")
print("=" * 45)
print()

# ── Enter name ──
name = input("Enter your name: ").strip()
if not name:
    print("Name is required.")
    input("Press Enter to exit...")
    sys.exit()

print()
print("[ Find Coordinates ]")
print("Hover your mouse over the name input field.")
print("Coordinates will be captured in 3 seconds...")
time.sleep(3)
nx, ny = pyautogui.position()
print(f"  -> Input field coordinates: ({nx}, {ny})")

print()
print("Hover your mouse over the 'Book Now' button.")
print("Coordinates will be captured in 3 seconds...")
time.sleep(3)
bx, by = pyautogui.position()
print(f"  -> Button coordinates: ({bx}, {by})")

print()
print(f"Name: {name}")
print(f"Input field: ({nx}, {ny})  |  Button: ({bx}, {by})")
print()
go = input("Start booking with these settings? (y/n): ").strip().lower()
if go != 'y':
    print("Cancelled.")
    input("Press Enter to exit...")
    sys.exit()

print()
print("Booking will start in 3 seconds. Switch to your browser now!")
time.sleep(3)

# ── Auto click ──
print(">> Clicking name input field...")
pyautogui.click(nx, ny)
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'a')
pyautogui.typewrite(name, interval=0.05)

time.sleep(0.2)
print(">> Clicking Book Now button!")
pyautogui.click(bx, by)

print()
print("Done! Check the result in your browser.")
input("Press Enter to exit...")
