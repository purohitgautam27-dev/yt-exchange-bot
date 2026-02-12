import telebot
import time

TOKEN = "8599913087:AAHejrM-0_KZOmGwOxUUghqgxzfczCiDOSs"

bot = telebot.TeleBot(TOKEN)

users = {}
videos = []

@bot.message_handler(commands=['start'])
def start(m):
    users[m.chat.id] = 0
    bot.send_message(m.chat.id,
        "🔥 YouTube View Exchange Bot\n\n"
        "/watch - Video dekho (5 coins)\n"
        "/submit - Apna video do (10 coins)\n"
        "/balance - Coins dekho")

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
