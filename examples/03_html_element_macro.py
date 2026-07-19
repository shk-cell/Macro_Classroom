"""
[Method 3] API-Based Macro
Directly calls the server API using Python requests. Fastest and most powerful.
"""

import requests
import time
import sys

print("=" * 45)
print("   API-Based Auto Booking Macro")
print("=" * 45)
print()

# ── Input ──
server = input("Enter server address (e.g. http://192.168.0.1:3000): ").strip().rstrip('/')
if server and not server.startswith('http'):
    server = 'http://' + server
if not server:
    print("Server address is required.")
    input("Press Enter to exit...")
    sys.exit()

name = input("Enter your name: ").strip()
if not name:
    print("Name is required.")
    input("Press Enter to exit...")
    sys.exit()

print()

# ── STEP 1: Check status & wait for booking to open ──
print(">> STEP 1: Connecting to server and checking booking status...")
try:
    res = requests.get(f"{server}/api/state", timeout=5)
    state = res.json()
except Exception as e:
    print(f"  ERROR: Could not connect to server: {e}")
    print("  Please check the server address.")
    input("Press Enter to exit...")
    sys.exit()

print(f"  Booking open: {'Yes' if state['is_open'] else 'No'}")
print(f"  Seats left: {state['seats_left']} / {state['total_seats']}")

if state['seats_left'] == 0:
    print("  ERROR: Sold out.")
    input("Press Enter to exit...")
    sys.exit()

if not state['is_open']:
    print()
    print("  Booking is not open yet.")
    print("  Waiting for booking to open... (checking every 0.3s)")
    while not state['is_open']:
        time.sleep(0.3)
        try:
            state = requests.get(f"{server}/api/state", timeout=5).json()
        except:
            pass
    print("  Booking is now open! Reserving immediately!")

# ── STEP 2: Get token ──
print()
print(">> STEP 2: Getting token...")
try:
    res = requests.get(f"{server}/api/ticket", timeout=5)
    if res.status_code != 200:
        print(f"  ERROR: Failed to get token: {res.json().get('error')}")
        input("Press Enter to exit...")
        sys.exit()
    token = res.json()['token']
    print(f"  Token received!")
except Exception as e:
    print(f"  ERROR: {e}")
    input("Press Enter to exit...")
    sys.exit()

# ── STEP 3: Reserve ──
print()
print(">> STEP 3: Submitting reservation...")
try:
    res = requests.post(
        f"{server}/api/reserve",
        json={"name": name, "token": token},
        timeout=5
    )
    data = res.json()
    print()
    if data.get('success'):
        print("=" * 37)
        print(f"   Booking Successful!")
        print(f"   Name   : {name}")
        print(f"   Seat   : {data['seat_number']}")
        print("=" * 37)
    else:
        print(f"ERROR: Booking failed: {data.get('error')}")
except Exception as e:
    print(f"  ERROR: {e}")

input("\nPress Enter to exit...")
