import telebot
import time
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from questionnaire_info import *
import json

class State:

    def __init__(self):
        self.file_name = "state.json"
        self.answers_file_name = "answers.json"

    def next(self):
        with open(self.file_name, "r") as file:
            d = json.load(file)
        step = d['step']
        d['step'] += 1
        d['step'] %= 5 # когда step превысит 5 то он станет равен 0 и отсчёт начнётся заново
        print(d)
        with open(self.file_name, "w") as file:
            json.dump(d, file)

        with open(self.answers_file_name, "r") as file:
            answers = json.load(file)['answers']
            return answers[step]

    def save_user_id(self, user_id):
        print("try save json")
        with open(self.file_name, "w") as file:
            try:
                json.dump({'step': 0, 'userId': user_id}, file)
            except Exception as e:
                print(e)


token = '6752421018:AAE3t9pFAZkhDC_zphZLC24ml1WHFhDN8TM'
bot = telebot.TeleBot(token)

answers_list = []

def file_generation(topic, number):
    return f'questions/{topic}_{number}.png'

@bot.message_handler(commands=['start'])
def send_start_message(message):
    print("start")
    state = State()
    user_id = message.from_user.id
    print(f"user id= {user_id}")
    state.save_user_id(user_id)


@bot.message_handler(content_types=['text'])
def handler_message(message):
    print(message.text)
    if message.text == "/help":
        bot.send_message(message.chat.id, help_message)
    else:
        state = State()
        answer = state.next()

        # print(f"step {js['step']}")
        bot.send_message(message.chat.id, answer['text'])



@bot.callback_query_handler(func=lambda call: call.data)
def callback(call):
    global test_start
    print("query")
    print(call.data)
    if call.data == 'start':
        pass
        # bot.send_message()
    else:
        users[call.message.chat.id]['Сделано'] += 1
        print(users)

print("init")
bot.polling(non_stop=False, timeout=10)
