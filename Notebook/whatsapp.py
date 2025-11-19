import pywhatkit
import pyautogui
import time

# List of numbers (with country code)
numbers = [
    "+918904311838",
    "+919686629204"
]

# Message to send
message = "Hi, how are you 😊"

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
