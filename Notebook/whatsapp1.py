import streamlit as st
import pywhatkit
import pyautogui
import time

st.title("📱 WhatsApp Bulk Sender")

st.write("Send a message instantly to multiple WhatsApp numbers.")

# Input: List of numbers (comma separated)
numbers_input = st.text_area(
    "Enter phone numbers (with country code, comma separated):",
    "+918904311838"
)

# Input: Message to send
message = st.text_area("Enter your message:", "Hi, how are you 😊")

# Send button
if st.button("Send WhatsApp Messages"):
    if numbers_input.strip() == "" or message.strip() == "":
        st.error("Please enter numbers and a message!")
    else:
        numbers = [num.strip() for num in numbers_input.split(",")]
        st.info("Sending messages... Make sure your browser is logged in to WhatsApp Web!")

        for phone in numbers:
            try:
                # Send instantly
                pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=5)
                time.sleep(7)  # Small delay between messages
                pyautogui.press("enter")
                st.success(f"Message sent to {phone}")
            except Exception as e:
                st.error(f"Failed to send to {phone}: {e}")

        st.balloons()
