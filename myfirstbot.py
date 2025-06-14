import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅Life with Jesus")

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Available commands:\n/start - Start the bot\n/help - Show this message\n/echo <text> - Repeat your message")

# Echo command
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        response = " ".join(context.args)
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("⚠️ Please provide some text to echo.\nUsage: /echo Hello")

# Message logger
async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[{update.effective_user.username}]: {update.message.text}")

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("echo", echo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_message))

    app.run_polling()
