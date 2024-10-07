from pyrogram import Client, filters
from simpleeval import simple_eval
import uuid


blacklist = []

with open("userbot.info", "r") as file:
    lines = file.readlines()

with open("bldb.info", "r") as file:
    for line in file:
        user_id = int(line.strip())
        blacklist.append(user_id)

cinfo = f"➕ `.math`"
ccomand = " Решает математические задачи."


def command_math(app):
    @app.on_message(filters.command("math", prefixes="."))
    def math_command(_, message):
        user_id = str(message.from_user.id)
        if user_id in open("bldb.info").read():
            message.reply("❌ **Вам запрещено использовать эту команду.**")
        else:
            try:
                expression = message.text.split(maxsplit=1)[1]
                result = simple_eval(expression)
                message.reply_text(f"➗ **Результат:** `{result}`")
            except IndexError:
                message.reply_text("❌ **Пожалуйста, введите математическое выражение после команды** `.math`.")
            except Exception as e:
                message.reply_text(f"❌ **Ошибка при вычислении выражения:** {e}")


print("Модуль math загружен!")