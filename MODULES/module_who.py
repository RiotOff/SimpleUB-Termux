from pyrogram import Client, filters
import random
import asyncio


blacklist = []

with open("userbot.info", "r") as file:
    lines = file.readlines()

with open("bldb.info", "r") as file:
    for line in file:
        user_id = int(line.strip())
        blacklist.append(user_id)

cinfo = "❓ `.who`"
ccomand = " Говорит кто есть кто в чате."

def command_who(app):
    @app.on_message(filters.command("who", prefixes="."))
    async def who_module(client, message):
        user_id = str(message.from_user.id)
        if user_id in open("bldb.info").read():
            message.reply("❌ **Вам запрещено использовать эту команду.**")
        else:
            if message.chat.type == "private":
                await message.reply("❌ **Данная команда доступна только в группах.**")
                return
            
            args = message.text.split()[1:]
            if not args:
                await message.reply("❌ **Неверное содержимое команды. Пример:\n`.who смешной`**")
                return

            if message.chat.type not in ["group", "supergroup"]:
                members = []
                async for member in client.get_chat_members(message.chat.id):
                    if not member.user.is_deleted:
                        members.append(member.user)
            else:
                await message.reply("❌ **Команда работает только в группах!**")

            if members:
                random_user = random.choice(members)
                if random_user.username:
                    response = f"✅ **@{random_user.username} {' '.join(args)}**"
                else:
                    response = f"✅ **{random_user.first_name} {' '.join(args)}**"
                await asyncio.sleep(2)
                await message.reply(response)
            else:
                await message.reply("❌ **В чате нет активных участников.**")

print("Модуль who загружен!")