from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import importlib
import sys
import time
import requests
import psutil
import platform
from datetime import timedelta
import os
from time import sleep


blacklist = []

with open("userbot.info", "r") as file:
    lines = file.readlines()
    api_id = int(lines[0].strip())
    api_hash = lines[1].strip()
    prefixes_bot = lines[2].strip()

app = Client("SimpleUB", api_id=api_id, api_hash=api_hash)
start_time = time.time()
loaded_modules = {}

MODULES_DIR = os.path.join(os.path.dirname(__file__), 'MODULES')
sys.path.append(MODULES_DIR)

def reload_modules():
    global loaded_modules
    modules_to_reload = list(loaded_modules.keys())
    loaded_modules.clear()
    for module_name in modules_to_reload:
        try:
            if module_name in sys.modules:
                module = importlib.reload(sys.modules[module_name])
            else:
                module = importlib.import_module(module_name)
            loaded_modules[module_name] = module
        except Exception as e:
            print(f"Ошибка перезагрузки модуля {module_name}: {e}")

    for module in loaded_modules.values():
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and (attr_name.startswith("register_") or attr_name.startswith("command_")):
                try:
                    attr(app)
                except Exception as e:
                    print(f"Ошибка вызова функции {attr_name} из модуля {module.__name__}: {e}")

def load_modules():
    global loaded_modules
    modules = []
    loaded_modules.clear()

    info_file_path = os.path.join(os.path.dirname(__file__), "modules.info")

    with open(info_file_path, "r") as file:
        for line in file:
            module_name = line.strip()
            if module_name:
                try:
                    if module_name in sys.modules:
                        module = importlib.reload(sys.modules[module_name])
                    else:
                        module = importlib.import_module(module_name)
                    loaded_modules[module_name] = module
                    modules.append(module)
                except Exception as e:
                    print(f"Ошибка загрузки модуля {module_name}: {e}")
    return modules

def load_and_exec_modules():
    modules = load_modules()
    for module in modules:
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and (attr_name.startswith("register_") or attr_name.startswith("command_")):
                try:
                    attr(app)
                except Exception as e:
                    print(f"Ошибка вызова функции {attr_name} из модуля {module.__name__}: {e}")


@app.on_message(filters.me & filters.command("help", prefixes="."))
async def help_command(_, message):
    prefix = "."
    help_text = "**⚙ Модулей загружено: {}**\n\n".format(len(loaded_modules))
    for module_name, module in loaded_modules.items():
        cinfo = module.cinfo if isinstance(module.cinfo, tuple) else (module.cinfo,)
        ccomand = module.ccomand if isinstance(module.ccomand, tuple) else (module.ccomand,)
        for info, command in zip(cinfo, ccomand):
            help_text += f"{info} - {command}\n"
    await message.edit("🌕")
    sleep(1)
    help_text += (f"**\n\n💬 Команды:**\n\n"
                  f"ℹ `{prefix}info` - Инфо о юзерботе.\n"
                  f"⌛ `{prefix}ping` - Пинг юзербота.\n"
                  f"💤 `{prefix}off` - Отключает юзербота.\n"
                  f"🔄 `{prefix}restart` - Перезагрузить все модули.\n"
                  f"🚫 `{prefix}addbl` / `{prefix}delbl` - Добавить/удалить из чёрного списка общедоступных команд.\n")
    await message.edit(help_text)

@app.on_message(filters.me & filters.command("test", prefixes="."))
async def test_command(client, message):
    keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Тестовая кнопка", url="https://telegram.org")]]
    )
    await message.reply("Тестовая кнопка", reply_markup=keyboard)

@app.on_message(filters.me & filters.command("info", prefixes="."))
async def info_command(_, message):
    prefix = "."
    current_time = time.time()
    uptime_seconds = int(round(current_time - start_time))
    uptime = str(timedelta(seconds=uptime_seconds))
    ram = psutil.virtual_memory().percent
    system_info = platform.system()
    system_release = platform.release()
    architecture = platform.architecture()[0]

    ping_start_time = time.time()
    await message.edit("🌕")
    sleep(1)
    ping_end_time = time.time()
    ping_time = round((ping_end_time - ping_start_time) * 1000, 1)

    user = message.from_user
    username = f"@username" # Замените на свой никнейм
    
    info_text = (f"**✨ SimpleUB**\n\n"
                 f"**😎 Владелец:** {username}\n\n"
                 f"**💫 Версия:** 3.1.2.\n"
                 f"**🌟 Обновление не требуется**\n"
                 f"**👥 ForUsers (Пользовательская версия)**\n\n"
                 f"**⌨️ Префикс:** «{prefix}»\n"
                 f"**⌛ Аптайм:** {uptime}\n\n"
                 f"**⚡️ Использование CPU:** __~NaN %__\n"
                 f"**💼 Использование RAM:** __~{ram} MB__\n"
                 f"**✌️ {system_info} {system_release} ({architecture})**")
    
    await message.edit(info_text)


@app.on_message(filters.me & filters.command(["off"], prefixes="."))
async def turn_off(_, message):
    await message.edit("🌕")
    sleep(1)
    await message.edit("**💤 Отключаю юзербота...**")
    exit()


@app.on_message(filters.me & filters.command(["ping"], prefixes="."))
async def ping(_, message):
    ping_start_time = time.time()
    await message.edit("🌕")
    ping_end_time = time.time()
    ping_time = round((ping_end_time - ping_start_time) * 1000)
    uptime_seconds = int(round(time.time() - start_time))
    uptime = str(timedelta(seconds=uptime_seconds))
    await message.edit(f"**⚡ Ваш пинг: {ping_time} мс**\n**🚀 Прошло с последней перезагрузки: {uptime}**\n\n 💡 __Скорость отклика Telegram в большей степени зависит от загруженности серверов Telegram и других внешних факторов и никак не связана с параметрами сервера, на который установлен юзербот__")


@app.on_message(filters.me & filters.command(["restart"], prefixes="."))
async def restart(_, message):
    await message.edit("**Перезапускаю модули...**")
    restart_start_time = time.time()
    reload_modules()
    restart_end_time = time.time()
    restart_time = round(restart_end_time - restart_start_time, 2)
    await message.edit(f"**✅ Модули перезапущены. Это заняло {restart_time} секунд.**")


@app.on_message(filters.me & filters.command("addbl", prefixes="."))
async def add_blacklist_command(_, message):
    userid_telegram = 1234567890 # Замените на свой ID
    if message.from_user.id == userid_telegram:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            if user_id not in blacklist:
                    if user_id == userid_telegram:
                        await message.edit("🌕")
                        time.sleep(1)
                        await message.edit("❌ **Вы не можете добавить себя в чёрный список.**")
                    else:
                        with open("bldb.info", "a") as file:
                            file.write(str(user_id) + "\n")
                        await message.edit("🌕")
                        time.sleep(1)
                        await message.edit("✅ **Пользователь добавлен в чёрный список клиента SimpleUB.**")
                        blacklist.append(user_id)
            else:
                await message.edit("🌕")
                time.sleep(1)
                await message.edit("🚫 **Пользователь уже находится в чёрном списке.**")
        else:
            await message.edit("🌕")
            time.sleep(1)
            await message.edit("🚫 **Выберите сообщение пользователя, чтобы заблокировать его.**")
    else:
        await message.edit("🌕")
        time.sleep(1)
        await message.edit("❌ **Вы не можете использовать данную команду.**")

@app.on_message(filters.me & filters.command("delbl", prefixes="."))
async def remove_blacklist_command(_, message):
    userid_telegram = 1234567890 # Замените на свой ID
    if message.from_user.id == userid_telegram:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            if user_id in blacklist:
                blacklist.remove(user_id)
                with open("bldb.info", "w") as file:
                    for id in blacklist:
                        file.write(str(id) + "\n")
                await message.edit("🌕")
                time.sleep(1)
                await message.edit("✅ **Пользователь удален из чёрного списка.**")
            else:
                await message.edit("🌕")
                time.sleep(1)
                await message.edit("🚫 **Пользователь не найден в чёрном списке.**")
        else:
            await message.edit("🌕")
            time.sleep(1)
            await message.edit("🚫 **Выберите сообщение пользователя, чтобы разблокировать его.**")
    else:
        await message.edit("🌕")
        time.sleep(1)
        await message.edit("❌ **Вы не можете использовать данную команду.**")


load_and_exec_modules()
print("Основа SimpleUB запущена! Актуальная версия: 3.1.2.")
app.run()
