import pyautogui
import time

# Move your mouse to a seat and check the coordinates
# Press Ctrl+C to quit

print("Move your mouse to the desired position.")
print("Press Ctrl+C to quit.\n")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Position: ({x}, {y})", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\nDone.")
