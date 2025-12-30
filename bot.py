import os
import telebot

# Get token from Koyeb environment
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot is active! Send a photo or video to get ID.")

# Function to get File ID
@bot.message_handler(content_types=['photo', 'video', 'document'])
def handle_docs(message):
    try:
        if message.content_type == 'photo':
            file_id = message.photo[-1].file_id
        elif message.content_type == 'video':
            file_id = message.video.file_id
        else:
            file_id = message.document.file_id
        
        bot.reply_to(message, f"File ID: {file_id}")
    except Exception as e:
        bot.reply_to(message, "Error processing file.")

# Keep bot running
if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
