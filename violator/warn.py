from uuid import uuid4
from telegram import Update
from telegram.ext import CallbackContext

async def warn(update: Update, context: CallbackContext) -> str:
    """Usage: /put value"""
    # Generate ID and separate value from command
    key = str(uuid4())
    # We don't use context.args here, because the value may contain whitespaces
    value = update.message.text.partition(' ')[2]

    # Store value
    context.user_data[key] = value
    # Send the key to the user
    await update.message.reply_text(key)

async def warns(update: Update, context: CallbackContext) -> str:
    """Usage: /get uuid"""
    # Seperate ID from command
    key = context.args[0]

    # Load value and send it to the user
    value = context.user_data.get(key, 'Not found')
    await update.message.reply_text(value)