from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
# from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from violator.decorators import group, restricted

MAX = 5

# def getwarn(update: Update, context: CallbackContext, key: str) -> int:
#     chat_id = update.message.chat.id

#     if chat_id in context.user_data.keys() and key in context.user_data[chat_id]:
#         return context.user_data[chat_id][key]
#     else: 
#         return 0

def getwarn(chat_id, context, key = 'warns'):
    if chat_id in context.user_data.keys() and key in context.user_data[chat_id]:
        return context.user_data[chat_id][key]
    else: 
        return 0

@group
def warns(update: Update, context: CallbackContext):
    if update.message.chat.id is not None:
        warnings = getwarn(update.message.chat.id, context)
    else:
        warnings = getwarn(update.callback_query.message.chat.id, context)
    
    update.message.reply_text(f'**Total de Warnings**: {warnings}')
 
@restricted
@group
def addwarn(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        reply = update.message.reply_to_message
        nick = f'@{reply.from_user.username}' if reply.from_user.username is not None else f'@{reply.from_user.first_name}'
        key = update.message.chat.id
        
        warnings = getwarn(update.message.chat.id, context)
        warnings = warnings + 1
        
        profile = { 'warns': warnings }
        context.user_data[key] = profile    

        context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
        context.bot.delete_message(chat_id=update.message.chat.id, message_id=reply.message_id)

        options = []
        options.append(InlineKeyboardButton(text='Remover Warning(somente admins)', callback_data='1'))
        reply_markup = InlineKeyboardMarkup([options])
        
        context.bot.send_message(chat_id=update.message.chat.id, text=f'Atenção {nick} você tem {warnings} warnings de um total de {MAX}!', reply_markup=reply_markup)
        

@restricted
@group
def rmwarn(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    key = update.callback_query.message.chat.id
    nick = f'@{update.callback_query.from_user.first_name}' if not update.callback_query.from_user.username else f'@{update.callback_query.from_user.username}'

    if update.message.chat.id in context.user_data.keys() and key in context.user_data[chat_id]:
        warnings = context.user_data[chat_id][key] 
        warnings = warnings-1 if warnings > 0 else 0
    else: 
        warnings = 0
    
    profile = { 'warns': warnings }
    context.user_data[key] = profile    
    
    context.bot.send_message(chat_id, f'Atenção {nick} você tem {warnings} warnings de um total de {MAX}!')