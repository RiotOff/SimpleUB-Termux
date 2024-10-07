from pyrogram import Client, filters
from time import sleep

cinfo = "🔒 `.defense`"
ccomand = " Включает/Отключает защиту для пользователя."
with open("userbot.info", "r") as file:
    lines = file.readlines()

def load_whitelist():
    with open("whitelist.info", "r") as file:
        return {line.strip() for line in file.readlines()}

whitelist = load_whitelist()
defense_status = False
userid_telegram = 1234567890 # Замените на свой ID

def command_protect(app):
    @app.on_message(filters.me & filters.command("defense", prefixes="."))
    async def toggle_protect_user(_, message):
        global defense_status
        defense_status = not defense_status
        await message.edit(f"🌕")
        await message.edit(f"**{'🔒 Защитная функция включена' if defense_status else '🔓 Защитная функция выключена'}.**")

    @app.on_message(filters.private)
    async def block_unauthorized_users(client, message):
        global defense_status
        global userid_telegram
        if message.from_user and defense_status and str(message.from_user.id) not in whitelist and not message.from_user.is_bot and str(message.from_user.id) != {userid_telegram}:
            await message.reply_text(f'🔒 **Здравствуйте! Юнит "SimpleDefense" защищает данный аккаунт. Вы не подтверждены!**\nЯ вынужден заблокировать вас из соображений безопасности.')
            await app.block_user(message.from_user.id)

print("Модуль defense загружен!")