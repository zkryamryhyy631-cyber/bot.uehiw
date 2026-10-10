# -*- coding: utf-8 -*-
import os, json, threading, time
from flask import Flask, request
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7145036494
CHANNEL_ID = None  # رابطك خاص، نخليه يشتغل بدون آيدي لين تجيبه
CHANNEL_LINK = "https://t.me/+l20CWCyobz5mZDdk"

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)
os.makedirs("database", exist_ok=True)

def get_user(uid):
    p=f"database/{uid}.json"
    if os.path.exists(p):
        try: return json.load(open(p,encoding="utf-8"))
        except: pass
    return {"balance":0.0,"points":10,"hosts":0,"orders":0,"trial":False,"vip":False,"joined":datetime.now().isoformat()}
def save_user(uid,data):
    json.dump(data, open(f"database/{uid}.json","w",encoding="utf-8"), ensure_ascii=False)

def main_kb(uid):
    m=InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("🚀 خدمات السوشال", callback_data="services"),
        InlineKeyboardButton("🖥️ الاستضافات 24/7", callback_data="hosting"),
        InlineKeyboardButton("💰 شحن الرصيد", callback_data="recharge"),
        InlineKeyboardButton("👤 حسابي", callback_data="profile")
    )
    if uid == ADMIN_ID:
        m.add(InlineKeyboardButton("👑 تقرير الشهر 🔄 (للأدمن فقط)", callback_data="admin_month"))
    return m

def get_monthly_stats():
    total_users = len([f for f in os.listdir("database") if f.endswith(".json")])
    return total_users, datetime.now().strftime("%B %Y")

@bot.message_handler(commands=['start'])
def start_msg(message):
    uid=message.from_user.id
    user=get_user(uid)
    save_user(uid,user)
    bot.send_message(uid, f"👋 أهلاً {message.from_user.first_name}\n✅ البوت شغال 24/7\n📢 قناتنا: {CHANNEL_LINK}", reply_markup=main_kb(uid))

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    uid=call.from_user.id; cid=call.message.chat.id; d=call.data
    if d=="admin_month":
        if uid!=ADMIN_ID:
            bot.answer_callback_query(call.id, "للأدمن فقط", show_alert=True); return
        total, month = get_monthly_stats()
        text=f"👑 تقرير شهر {month}\n\n👥 المستخدمين: {total}\n📅 يتحدث تلقائياً كل شهر\n✅ البوت شغال 24/7 بدون توقف"
        m=InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("🔄 تحديث", callback_data="admin_month"))
        m.add(InlineKeyboardButton("🔙 رجوع", callback_data="main"))
        bot.edit_message_text(text, cid, call.message.message_id, reply_markup=m)
        return
    if d=="main":
        bot.edit_message_text("🏠 الرئيسية - شغال 24/7", cid, call.message.message_id, reply_markup=main_kb(uid))
    elif d=="hosting":
        m=InlineKeyboardMarkup().add(InlineKeyboardButton("🌐 مشتركة 5$", callback_data="buy"), InlineKeyboardButton("🔙 رجوع", callback_data="main"))
        bot.edit_message_text("🖥️ استضافات تعمل 24/7", cid, call.message.message_id, reply_markup=m)
    else:
        bot.edit_message_text("🏠 الرئيسية", cid, call.message.message_id, reply_markup=main_kb(uid))

def keep_alive():
    while True:
        time.sleep(500); print("Alive 24/7")

threading.Thread(target=keep_alive, daemon=True).start()

@app.route("/", methods=["GET","POST"])
def webhook():
    if request.method=="POST":
        bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode("utf-8"))])
    return "Bot Live 24/7",200

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))