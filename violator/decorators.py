from functools import wraps

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id 

        #context.bot.send_message(update.message.chat_id, text=str(update.message))

        if user_id in context.bot.get_chat_administrators(update.effective_chat.id):
            context.bot.send_message(update.message.chat_id, text="Apesar do bloqueio, por ser admin, o usuário é imune.")
            return
        return func(update, context)
    return wrapped

def group(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        if update.message.chat.type != 'supergroup' and update.message.chat.type != 'group':
            return
        return func(update, context)
    return wrapped