import os
import random
import requests
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
HF_API_KEY = os.environ.get("HF_API_KEY")
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, (
        "👋 Halo, aku *LumulyBot*, asisten AI & game cuan!\n\n"
        "Ketik /tanya <pertanyaan>\n"
        "Ketik /spin untuk main roda hadiah 🎁"
    ), parse_mode='Markdown')

@bot.message_handler(commands=['tanya'])
def tanya(message):
    user_input = message.text.replace("/tanya", "").strip()
    if not user_input:
        bot.reply_to(message, "❗Tulis pertanyaan setelah /tanya\nContoh: /tanya Apa itu AI?")
        return

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_input}

    try:
        res = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        result = res.json()

        if isinstance(result, list) and result and 'generated_text' in result[0]:
            reply = result[0]['generated_text']
        elif isinstance(result, dict) and 'generated_text' in result:
            reply = result['generated_text']
        else:
            reply = "❌ Maaf, AI belum bisa menjawab pertanyaan itu."

        bot.reply_to(message, reply)
    except Exception:
        bot.reply_to(message, "⚠️ Terjadi kesalahan saat menghubungi AI.")

@bot.message_handler(commands=['spin'])
def spin(message):
    hadiah = [
        "🎉 Dapat 100 Poin!",
        "🎁 Klik & klaim: https://shrinke.me/lumulyreward",
        "💸 Diskon 30%: Gunakan kode LUMUDISKON",
        "💣 Zonk! Coba lagi 😅",
        "🔥 eBook gratis: https://shrinke.me/ebookcuan",
        "🧨 Undang 3 teman untuk hadiah spesial!"
    ]
    result = random.choice(hadiah)
    bot.reply_to(message, f"🔁 Memutar roda...\n\n{result}")

bot.polling()
