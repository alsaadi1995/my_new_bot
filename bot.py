import telebot
import pandas as pd
import os

# التوكن يتم سحبه تلقائياً من Koyeb
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# اسم الملف اللي راح ينحفظ بالسيرفر
DATA_FILE = "data.xlsx"

# رسالة البداية (Start)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "هلا بيك! أنا بوت السجل الذكي 🤖\n\n- دز لي ملف إكسل (Excel) حتى أحفظه.\n- وراها اكتب أي اسم أو رقم وراح أطلع لك النتيجة.")

# استلام ملف الإكسل
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.file_name.endswith('.xlsx'):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open(DATA_FILE, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.reply_to(message, "✅ عاشت إيدك، استلمت الملف وحفظت البيانات. هسه تكدر تبحث!")
    else:
        bot.reply_to(message, "⚠️ عذراً، دز لي ملف بصيغة إكسل (xlsx) فقط.")

# البحث عن الأسماء
@bot.message_handler(func=lambda message: True)
def search_data(message):
    if not os.path.exists(DATA_FILE):
        bot.reply_to(message, "⚠️ السجل فارغ حالياً، دز ملف الإكسل أولاً.")
        return

    query = message.text # النص اللي كتبه المستخدم
    try:
        df = pd.read_excel(DATA_FILE)
        # البحث في كل الجدول
        results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
        
        if not results.empty:
            response = "🔎 نتائج البحث اللي لكيتها:\n"
            for index, row in results.head(5).iterrows():
                line = " | ".join([str(v) for v in row.values])
                response += f"----------\n{line}\n"
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "❌ ماملتقي بهذا الاسم أو الرقم بالسجل.")
    except Exception as e:
        bot.reply_to(message, "صار خطأ بقراءة الملف، تأكد من الملف شغال.")

bot.polling()
