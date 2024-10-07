from pyrogram import Client, filters
import random
import time


blacklist = []

with open("userbot.info", "r") as file:
    lines = file.readlines()

with open("bldb.info", "r") as file:
    for line in file:
        user_id = int(line.strip())
        blacklist.append(user_id)

cinfo = f"🪙 `.oorr`"
ccomand = " Орёл или решка."


def command_oorr(app):
    @app.on_message(filters.command("oorr", prefixes="."))
    def oorr_command(_, message):
        user_id = str(message.from_user.id)
        if user_id in open("bldb.info").read():
            message.reply("❌ **Вам запрещено использовать эту команду.**")
        else:
            random_number = random.randint(0, 1)
            if random_number == 0:
                coin_emoji = "🌑"
                new_emoji = "**🪙 Выпала решка!**"
            else:
                coin_emoji = "🌑"
                new_emoji = "**🦅 Выпал орёл!**"
            sent_message = message.reply_text(coin_emoji)
            time.sleep(2)
            sent_message.reply_text(new_emoji)

print("Модуль oorr загружен!")
