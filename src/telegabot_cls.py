import telebot

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def send_message(self, chat_id, message):
        self.bot.send_message(chat_id, message)

    def start_listening(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.send_message(message.chat.id, "хэлоу")

        self.bot.polling()
