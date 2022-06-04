import os, random, string, time
from uuid import uuid4
from violator.mwt import MWT
from captcha.image import ImageCaptcha
from telegram import Update, Chat, ChatMember, ChatMemberUpdated, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, ChatMemberHandler, Filters, PicklePersistence, CallbackContext
from config.blacklist import blacklist
from violator.decorators import restricted
from violator.warn import *

MODE = os.environ.get('MODE', 'polling')
TOKEN = os.environ.get('TELEGRAM_TOKEN')
URL = 'https://violator-tgbot.herokuapp.com/'
PORT = int(os.environ.get('PORT', '8443'))
SEC = 300
EXP = time.strftime('%S segundos', time.gmtime(SEC)) if SEC < 60 else time.strftime('%M minutos', time.gmtime(SEC))
CAPTCHA, CHECK = range(2)

timestamp = int(time.time())

#@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]

def remove_job_if_exists(name: str, context: CallbackContext) -> None:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if current_jobs:
        for job in current_jobs:
            job.schedule_removal()

def bemvindo(context: CallbackContext) -> None:
    chat_data = context.job.context['chat_data']
    user_data = context.job.context['user_data']
    context.bot.delete_message(chat_id=chat_data['chat_id'], message_id=user_data['bemvindo_message'].message_id)

def expirado(context: CallbackContext) -> None:
    chat_data = context.job.context['chat_data']
    user_data = context.job.context['user_data']

    context.bot.delete_message(chat_id=chat_data['chat_id'], message_id=user_data['captcha_message'].message_id)
    context.bot.ban_chat_member(chat_data['chat_id'], user_data['user_id'], until_date=int(round(300 + timestamp)), revoke_messages=False)

def onleave(update: Update, context: CallbackContext) -> None:
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

def onjoin(update: Update, context: CallbackContext) -> int:
    # Delete join message?
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

    chat_id = update.message.chat_id
    me = context.bot.get_me()

    for member in update.message.new_chat_members:
        if me.id == member.id:
            context.bot.send_message(chat_id, text='💀 Cheguei pessoal!')
        elif not member.is_bot and me.id in get_admin_ids(context.bot, chat_id):
            nick = f'@{member.username}' if member.username != 'None' else f'@{member.first_name}'
            mensagem = f'\n💣 ATENÇÃO {nick} 💣\n\nResponda o captcha na imagem em até: {EXP}\n\nOu você será kickado do grupo!'
            captcha_text = random_char(3)

            context.user_data['captcha'] = captcha_text
            context.user_data['user_id'] = member.id
            context.chat_data['chat_id'] = chat_id

            image = ImageCaptcha(width=190, height=90)
            image.write(captcha_text, 'captcha.png')

            context.user_data['captcha_message'] = context.bot.send_photo(chat_id, photo=open('captcha.png', 'rb'), caption=mensagem)
            context.job_queue.run_once(expirado, SEC, context={'job_data': chat_id, 'user_data': context.user_data, 'chat_data': context.chat_data}, name=str(chat_id))

            return CAPTCHA

def captcha(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id

    if update.message.text.lower() == context.user_data['captcha']:
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['captcha_message'].message_id)
        context.user_data['bemvindo_message'] = context.bot.send_message(update.message.chat_id, text="Bem-vindo ao grupo!")
        remove_job_if_exists(str(update.message.chat_id), context)
        context.job_queue.run_once(bemvindo, SEC, context={'user_data': context.user_data, 'chat_data': context.chat_data}, name=str(chat_id))
    else:
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['captcha_message'].message_id)
        return CAPTCHA

    return ConversationHandler.END

def random_char(y):
    return ''.join(random.choice(string.ascii_letters.lower()) for x in range(y))

def pong(update: Update, context: CallbackContext) -> None:
    context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)

def cancel():
    return

@restricted
def censor(update: Update, context: CallbackContext) -> None:
    if any(x in update.message.text.lower() for x in blacklist):
        context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)

def main():
    persistence = PicklePersistence(filename='pickle')
    updater = Updater(TOKEN, persistence=persistence, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("ping", pong))
    
    # Ao entrar
    captcha_handler = ConversationHandler(
        entry_points=[CommandHandler('cap', onjoin), MessageHandler(Filters.status_update.new_chat_members, onjoin)],
        states={
            CAPTCHA: [MessageHandler(Filters.text & ~Filters.command, captcha)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(captcha_handler)

    # Ao sair     
    dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, onleave))

    # Censura
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, censor))
    
    # Warn
    dispatcher.add_handler(CommandHandler("warn", warn))
    dispatcher.add_handler(CommandHandler("warns", warns))
   
    if MODE == 'webhook':
        # enable webhook
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=URL + TOKEN)
        updater.idle()
    else:
        # enable polling
        updater.start_polling()

if __name__ == '__main__':
    main()


