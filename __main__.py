import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import telegram

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Информация, которая должна быть закреплена за клавиатурой:
# Пост ВК (его айди)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button_list = [
        ["Случайный пост", "Отправить в отложку"]
    ]

    reply_markup = telegram.ReplyKeyboardMarkup(button_list)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите опцию:",
        reply_markup=reply_markup
    )
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

TOKEN = open("token.txt").readline().strip()

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
