from telegram import Update
from telegram.ext import CallbackContext
from violator.decorators import group

def get(update: Update, context: CallbackContext, key: str) -> int:
    chat_id = update.message.chat.id

    if chat_id in context.user_data.keys() and key in context.user_data[chat_id]:
        return context.user_data[chat_id][key]
    else: 
        return 0

@group
def warns(update: Update, context: CallbackContext):
    if update.message.chat.type != 'supergroup' and update.message.chat.type != 'group':
        return

    warnings = get(update, context, 'warns')
    stars = get(update, context, 'stars')

    if warnings < 1:
        update.message.reply_text('Sem warnings')
    else:
        update.message.reply_text(warnings)
 

@group
def warn(update: Update, context: CallbackContext):
    if update.message.chat.type != 'supergroup' and update.message.chat.type != 'group':
        return

    key = update.message.chat.id
    warnings = get(update, context, 'warns') + 1
    stars = get(update, context, 'stars')
      
    profile = {
        'warns': warnings,
        'stars': stars
    }

    context.user_data[key] = profile