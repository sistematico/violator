from uuid import uuid4
from telegram import Update
from telegram.ext import CallbackContext

def warns(update: Update, context: CallbackContext):
    """Usage: /get uuid"""
    # Seperate ID from command
    # key = context.args[0]

    # Load value and send it to the user
    # value = context.user_data.get(key, 'Not found')
    # update.message.reply_text(value)

    # return context.user_data.get(key)
    # return context.user_data[key]
    key = context.args[0]
    update.message.reply_text(context.user_data[key])

def warn(update: Update, context: CallbackContext) -> str:
    key = str(uuid4())
    #value = update.message.text.partition(' ')[2]
    profile = {
        'warns': 0,
        'stars': 0
    }

    # Store value
    context.user_data[key] = profile
    # Send the key to the user
    
    
    # update.message.reply_text(key)
    update.message.reply_text(repr(update))

