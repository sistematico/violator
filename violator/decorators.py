from functools import wraps

def restricted(func):
    @wraps(func)
    def wrapped(update, context):
        if update.effective_user.id in context.bot.get_chat_administrators(update.effective_chat.id):
            context.bot.send_message(update.message.chat_id, text="É admin")
            return
        return func(update, context)
    return wrapped