import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from datetime import datetime, timezone, timedelta

import utils
from post import Post

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

config_file = open("config.txt")
TOKEN = config_file.readline().strip()
CHANNEL_ID = config_file.readline().strip()
GROUP_ID = config_file.readline().strip()
VK_TOKEN = config_file.readline().strip()
WHITELIST = config_file.readline().strip().split(' ')

scheduled_posts = []

CHOOSING, POST_QUEUEING, TIME_SELECTED = range(3)

keyboard_start = [["Случайный пост", "Показать отложку"]]
keyboard_normal = [["Случайный пост", "В отложку"],
                   ["Показать отложку"]]

markup_start = ReplyKeyboardMarkup(keyboard_start, one_time_keyboard=True)
markup_normal = ReplyKeyboardMarkup(keyboard_normal, one_time_keyboard=True)

async def schedule_checker_and_poster(context: ContextTypes.DEFAULT_TYPE):
    offset = timedelta(hours=3)
    now = datetime.now().astimezone(timezone(offset))
    current_time = now.strftime("%H:%M")
    for post in scheduled_posts:
        if current_time == post.time:
            if post.img_url != "":
                await context.bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=post.img_url,
                    caption=post.text,
                )
            else:
                await context.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=post.text,
                )
            scheduled_posts.remove(post)

async def show_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for post in scheduled_posts:
        await update.message.reply_text(
            text="Время: " + post.time + '\n\n' + post.text + '\n' + post.img_url,
            reply_markup=markup_start
        )
    return CHOOSING

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    username = update.message.from_user["username"]
    if not (username in WHITELIST):
        await update.message.reply_text(
            text="Пошёл нахуй чёрт ебаный"
        )
        return ConversationHandler.END
    await update.message.reply_text(
        text="Жми на кнопку",
        reply_markup=markup_start
    )
    return CHOOSING

async def choosing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    post_id = utils.get_random_post_id(GROUP_ID, VK_TOKEN)
    post_url = utils.get_post_url(post_id)
    context.user_data["post_id"] = post_id
    await update.message.reply_text(
        text=f"Случайный пост: {post_url}",
        reply_markup=markup_normal
    )
    return CHOOSING

async def queueing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="На какое время залить пост?"
    )
    return POST_QUEUEING

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    time = update.message.text
    post_id = context.user_data["post_id"]

    post_text, post_photo = utils.parse_post(post_id, VK_TOKEN)

    scheduled_posts.append(Post(post_text, post_photo, time))

    del context.user_data["post_id"]

    await update.message.reply_text(
        text="Пост в отложке! В канале её не видно, однако она есть! Продолжить?",
        reply_markup=markup_start
    )
    return TIME_SELECTED

async def fallback_func(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Что-то пошло не так...",
    )
    return CHOOSING

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    job_queue = application.job_queue
    job_queue.run_repeating(schedule_checker_and_poster, interval=15, first=10)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(filters.Regex("^(В отложку)$"), queueing),
                MessageHandler(filters.Regex("^(Случайный пост)$"), choosing),
                MessageHandler(filters.Regex("^(Показать отложку)$"), show_schedule),
            ],
            POST_QUEUEING: [
                MessageHandler(filters.Regex("^(\d\d:\d\d)$"), post),
                MessageHandler(filters.TEXT, queueing),
            ],
            TIME_SELECTED: [
                MessageHandler(filters.Regex("^(Случайный пост)$"), choosing),
                MessageHandler(filters.Regex("^(Показать отложку)$"), show_schedule),
            ]
        },
        fallbacks=[MessageHandler(filters.TEXT, fallback_func)]
    )
    application.add_handler(conv_handler)
    application.run_polling()