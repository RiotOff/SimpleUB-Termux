from pyrogram import Client, filters
import g4f

g4f.debug.logging = False
g4f.check_version = False

with open("userbot.info", "r") as file:
    lines = file.readlines()
    prefix_userbot = lines[2].strip()

cinfo = f"🧠`.gpt`"
ccomand = " ChatGPT"


def load_blocklist(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]
blocklist = load_blocklist("blocklist.info")


def contains_blocked_word(text):
    for word in blocklist:
        if word in text:
            return True
    return False


def replace_blocked_words(text): 
    for word in blocklist:
        text = text.replace(word, "DELETED")
    return text


def command_gpt(app):
    @app.on_message(filters.command("gpt", prefixes="."))
    def gpt_command(client, message):
        user_input = message.text.split(f".gpt ", maxsplit=1)[1]
        if contains_blocked_word(user_input):
            message.reply_text("В вашем запросе есть запрещённые слова/словосочетания.")
        else:
            initial_prompt = "You are ChatGPT, a large language model trained by OpenAI. Carefully heed the user's instructions. Respond using Markdown. Language - Russian"
            response = g4f.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": initial_prompt},
                    {"role": "user", "content": user_input}
                ],
            )

            if isinstance(response, str):
                response_text = response
            else:
                response_text = response['choices'][0]['message']['content']

            response_text = replace_blocked_words(response_text)
            reply_text = f"**👨Ваш запрос: {user_input}**\n🧠Ответ от ChatGPT: `{response_text}`"
            message.reply_text(reply_text)

print("Модуль gpt загружен!")