from functools import wraps

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):

        # try:
        #     update.message.from_user.id
        # except None:
        # # except NoneType:
        #     user_id = update.callback_query.from_user.id
        # else:
        #     user_id = update.message.from_user.id

        user_id = update.callback_query.from_user.id if not update.message else update.message.from_user.id
        chat_id = update.callback_query.message.chat.id if not update.message else update.message.chat_id
        admins = context.bot.get_chat_administrators(chat_id)
        
        for admin in admins:
            if user_id == admin.user.id:
                return func(update, context)
        return
    return wrapped

def group(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        chat = update.callback_query.message.chat if not update.message else update.message.chat
        if chat.type != 'supergroup' and chat.type != 'group':
            return
        return func(update, context)
    return wrapped