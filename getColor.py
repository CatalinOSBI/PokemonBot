import pyautogui
import keyboard
import sys

print("Mouse Position and Color Tracker")
print("Press 'c' to capture current mouse position and color")
print("Press 'q' to quit\n")

while True:
    if keyboard.is_pressed('c'):
        x, y = pyautogui.position()
        screenshot = pyautogui.screenshot()
        pixel_color = screenshot.getpixel((x, y))
        print(f"Position: ({x}, {y}) | Color: RGB{pixel_color}")
        keyboard.wait('c', suppress=True)  
    elif keyboard.is_pressed('q'):
        print("\nTracker stopped")
        sys.exit(0)