from pyrogram import Client, filters

with open("userbot.info", "r") as file:
    lines = file.readlines()

cinfo = f"✉ `.spam`"
ccomand = f" Начинает спамить сообщением, выбранным вами."


def command_spam(app):
    @app.on_message(filters.me & filters.command(["spam"], prefixes="."))
    def spam_message(_, message):
        _, count, *words = message.text.split()
        count = int(count)
        text = ' '.join(words)
        message.delete()
        for _ in range(count):
            app.send_message(message.chat.id, text)

print("Модуль spam загружен!")
