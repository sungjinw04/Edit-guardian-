# bot.py
import os
from pyrogram import Client, filters
from pymongo import MongoClient
from pyrogram.types import Message

# Initialize Pyrogram Client
app = Client(
    "my_bot",
    api_id="25064357",  # Replace with your own API ID
    api_hash="cda9f1b3f9da4c0c93d1f5c23ccb19e2",  # Replace with your own API HASH
    bot_token="7329929698:AAGD5Ccwm0qExCq9_6GVHDp2E7iidLH-McU"  # Replace with your Bot Token
)

# MongoDB Setup
MONGO_URI = os.getenv("MONGO_URI")  # Ensure you set the environment variable MONGO_URI properly
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["telegram_bot"]
messages_collection = db["messages"]

# Function to save messages to MongoDB
def save_message_to_db(message: Message):
    messages_collection.insert_one({
        "user_id": message.from_user.id,
        "chat_id": message.chat.id,
        "message_id": message.id,  # Corrected: message.id instead of message.message_id
        "text": message.text or message.caption,
        "timestamp": message.date,
    })

# Function to handle edited messages
@app.on_edited_message(filters.group)
def handle_edited_message(client, message: Message):
    # Delete the edited message
    client.delete_messages(chat_id=message.chat.id, message_ids=message.id)  # Corrected: message.id instead of message.message_id
    
    # Send an alert message
    alert_text = f"⚠️ {message.from_user.first_name} has edited a message. It was deleted."
    client.send_message(chat_id=message.chat.id, text=alert_text)

# Function to handle incoming messages
@app.on_message(filters.group)
def handle_messages(client, message: Message):
    # Save message to MongoDB
    save_message_to_db(message)

# Start the bot
if __name__ == "__main__":  # Corrected line
    print("Bot is running...")
    app.run()  # Corrected: use app.run() to start the bot session correctly

