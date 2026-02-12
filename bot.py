import telebot
import time

TOKEN = "8599913087:AAHejrM-0_KZOmGwOxUUghqgxzfczCiDOSs"
CHANNEL_USERNAME = "@gd_purohit_official"

def is_user_joined(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False
bot = telebot.TeleBot(TOKEN)

users = {}
videos = []

@bot.message_handler(commands=['start'])
def start(m):

    if not is_user_joined(m.chat.id):
        from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ Join Channel", url="https://t.me/gd_purohit_official"))
        markup.add(InlineKeyboardButton("🔄 Check Join", callback_data="check_join"))

        bot.send_message(m.chat.id, "⚠️ Pehle channel join karo tab bot chalega!", reply_markup=markup)
        return

    users[m.chat.id] = 0
    bot.send_message(
        m.chat.id,
        "🔥 YouTube View Exchange Bot\n\n"
        "/watch - Video dekho (5 coins)\n"
        "/submit - Apna video do (10 coins)\n"
        "/balance - Coins dekho"
        )

@bot.message_handler(commands=['balance'])
def bal(m):
    coins = users.get(m.chat.id, 0)
    bot.send_message(m.chat.id, f"💰 Tumhare coins: {coins}")

@bot.message_handler(commands=['watch'])
def watch(m):
    if not videos:
        bot.send_message(m.chat.id, "❌ Koi video nahi hai")
        return
    users[m.chat.id] = users.get(m.chat.id, 0)
    bot.send_message(m.chat.id, f"🎥 Ye video dekho:\n{videos[0]}\n\n30 sec baad /done bhejo")

@bot.message_handler(commands=['done'])
def done(m):
    users[m.chat.id] += 5
    bot.send_message(m.chat.id, "✅ +5 coins mil gaye")

@bot.message_handler(commands=['submit'])
def submit(m):
    if users.get(m.chat.id, 0) < 10:
        bot.send_message(m.chat.id, "❌ 10 coins chahiye")
        return
    bot.send_message(m.chat.id, "Apna YouTube link bhejo")

@bot.message_handler(func=lambda m: "youtu" in m.text)
def addvideo(m):
    videos.append(m.text)
    users[m.chat.id] -= 10
    bot.send_message(m.chat.id, "✅ Video submit ho gaya")

bot.infinity_polling()
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join(call):
    if is_user_joined(call.from_user.id):
        bot.edit_message_text(
            "✅ Verified! Ab bot use kar sakte ho 🔥",
            call.message.chat.id,
            call.message.message_id
        )
    else:
        bot.answer_callback_query(
            call.id,
            "❌ Pehle channel join karo!",
            show_alert=True
)
