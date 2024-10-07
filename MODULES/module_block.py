from pyrogram import Client, filters, enums
import uuid

cinfo = "⛔ `.block`"
ccomand = " Блокирует пользователя в личных сообщениях."
with open("userbot.info", "r") as file:
    lines = file.readlines()


def command_block(app):
    @app.on_message(filters.me & filters.command("block", prefixes="."))
    def block_user(client, message):
        if message.chat.type == enums.ChatType.PRIVATE:
            user_id = message.chat.id
            user_name = message.chat.username
            message.edit(f"⛔ **Пользователь {user_name} заблокирован.**")
            client.block_user(user_id)
        else:
            message.edit(f"❌ **Команда работает только в личных сообщениях!**")

print("Модуль block загружен!")