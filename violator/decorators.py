from functools import wraps

def restricted(func):
    @wraps(func)
    def wrapped(update, context):
        if context.message.user_id in context.bot.get_chat_administrators(update.effective_chat.id):
            context.bot.send_message(update.message.chat_id, text="Apesar do bloqueio, por ser admin, o usuário é imune.")
            return
        return func(update, context)
    return wrapped