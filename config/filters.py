from telegram import Update, Chat, ChatMember, ChatMemberUpdated, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageFilter, ChatMemberHandler, Filters

#me = bot.get_me()

class FilterAwesome(MessageFilter):
    def filter(self, message):
        return 'python-telegram-bot is awesome' in message.text

filter_awesome = FilterAwesome()