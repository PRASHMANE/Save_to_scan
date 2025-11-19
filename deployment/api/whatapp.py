import pywhatkit
import pyautogui
import time

def alert(msg,no1):
# List of numbers (with country code)
    numbers = [
        f"+91{no1}"
    ]

    # Message to send
    message = msg

    # Loop through numbers
    for phone in numbers:
        try:
            # Send instantly (browser must be logged in)
            pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=5)
            time.sleep(7)  # Small delay between messages to avoid overlap

            # Press enter to actually send
            pyautogui.press("enter")
            print(f"Message sent to {phone}")

        except Exception as e:
            print(f"Failed to send to {phone}: {e}")
