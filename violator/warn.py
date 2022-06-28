from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from violator.decorators import group, restricted

MAX = 5

def getwarn(chat_id, context):
    if chat_id in context.user_data.keys() and 'warns' in context.user_data[chat_id]:
        return context.user_data[chat_id]['warns']
    else: 
        return 0

@group
def warns(update: Update, context: CallbackContext) -> None:
    chat_id = update.callback_query.message.chat.id if update.callback_query is not None else update.message.chat.id
    warnings = getwarn(chat_id, context)
    update.message.reply_text(f'***Total de Warnings***: {warnings}', parse_mode='MarkdownV2')
 
@restricted
@group
def addwarn(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:        
        reply = update.message.reply_to_message
        nick = f'@{reply.from_user.username}' if reply.from_user.username is not None else f'@{reply.from_user.first_name}'
        #chat_id = update.effective_chat.id
        chat_id = update.message.chat.id
        warnings = getwarn(chat_id, context) + 1
        
        profile = { 'warns': warnings }
        context.user_data[chat_id] = profile    

        context.bot.delete_message(chat_id, update.message.message_id)
        context.bot.delete_message(chat_id, reply.message_id)

        options = []
        options.append(InlineKeyboardButton(text=f'🚫 Remover Warning', callback_data='1'))
        reply_markup = InlineKeyboardMarkup([options])
        
        # context.job_queue.run_once(expirado, SEC, context={'job_data': chat_id, 'user_data': context.user_data, 'chat_data': context.chat_data}, name=str(chat_id))

        context.chat_data['remove_warning_message'] = context.bot.send_message(chat_id=chat_id, text=f'Atenção {nick} você tem {warnings} warnings de um total de {MAX}!', reply_markup=reply_markup)

@restricted
@group
def rmwarn(update: Update, context: CallbackContext) -> None:
    chat_id = update.callback_query.message.chat.id
    nick = f'@{update.callback_query.from_user.first_name}' if not update.callback_query.from_user.username else f'@{update.callback_query.from_user.username}'
    warnings = 0

    #if update.message.chat.id in context.user_data.keys() and chat_id in context.user_data:
    if chat_id in context.user_data.keys() and chat_id in context.user_data[chat_id]:
        warnings = context.user_data[chat_id]['warns'] if context.user_data[chat_id]['warns'] > 0 else 0
    
    profile = { 'warns': warnings }
    context.user_data[chat_id] = profile    
    
    context.bot.delete_message(chat_id, context.chat_data['remove_warning_message'].message_id)
    context.bot.send_message(chat_id, f'Agora ***{nick}*** tem ***{warnings}*** warnings de um total de ***{MAX}***', parse_mode='MarkdownV2')
