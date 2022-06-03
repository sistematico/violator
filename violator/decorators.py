from functools import wraps

def restricted(func):
    @wraps(func)
    def wrapped(context, update, *args, **kwargs):
        user_id = args[0].effective_user.id 
        if user_id in context.bot.get_chat_administrators(update.effective_chat.id):
            context.bot.send_message(update.message.chat_id, text="Apesar do bloqueio, por ser admin, o usuário é imune.")
            return
        return func(update, context)
    return wrapped