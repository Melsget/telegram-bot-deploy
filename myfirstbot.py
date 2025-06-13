import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.error import Forbidden

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # or hardcode your ID here
CHANNEL_USERNAME = "@FreshToSenior"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)
    if chat_member.status not in ['member', 'administrator', 'creator']:
        await update.message.reply_text(
            f"Please join our channel first: https://t.me/{CHANNEL_USERNAME[1:]}"
        )
        return
    await update.message.reply_text("Welcome! You can now send your message.")

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text
    chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)
    if chat_member.status not in ['member', 'administrator', 'creator']:
        await update.message.reply_text(
            f"Please join our channel first: https://t.me/{CHANNEL_USERNAME[1:]}"
        )
        return
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"From {user.full_name} (@{user.username}):\n{message}"
    )
    await update.message.reply_text("Your message has been sent to the admin!")

async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID or not update.message.reply_to_message:
        return
    original = update.message.reply_to_message.text
    username_line = original.splitlines()[0]
    username = username_line.split("@")[-1].rstrip(":")
    try:
        await context.bot.send_message(
            chat_id=f"@{username}",
            text=f"Reply from admin:\n\n{update.message.text}"
        )
        await update.message.reply_text("Reply sent.")
    except Forbidden:
        await update.message.reply_text("Failed to deliver message.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
    app.run_polling()
