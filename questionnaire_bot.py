import telebot
import time
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from questionnaire_info import *


token = '6752421018:AAE3t9pFAZkhDC_zphZLC24ml1WHFhDN8TM'
bot = telebot.TeleBot(token)
test_start = False
answers_list = []
continuing = False


def waiting(n, long):
    # while True:
    #     if n > long:
    #         break
    while True:
        if continuing:
            break


def file_generation(topic, number):
    return f'questions/{topic}_{number}.png'


def check(l):
    pass

@bot.message_handler(commands=['start'])
def send_start_message(message):
    start_markup = InlineKeyboardMarkup(keyboard=None, row_width=3)
    start_markup.add(InlineKeyboardButton('Начать тест', callback_data='start'))
    bot.send_photo(message.chat.id, 'https://yandex.ru/images/search?img_url=https%3A%2F%2Fsun3-13.userapi.com%2Fvadh'
                                    '7WKEXKdt6t9cwBk3Q1imxSJGwi_0IZGkeA%2Fh9cNyZhSMlk.jpg&lr=39&pos=0&rpt=simage&'
                                    'source=serp&text=%D1%84%D0%BE%D1%82%D0%BE', reply_markup=start_markup)
    global test_start
    test_start = False


@bot.message_handler(commands=['help'])
def send_help_message(message):
    bot.send_message(message.chat.id, help_message)
    global test_start
    test_start = False


@bot.callback_query_handler(func=lambda call: call.data)
def callback(call):
    global test_start
    if call.data == 'start':
        if call.message.chat.id not in users:
            users[call.message.chat.id] = {'Сделано': 0}
        print(users)
        test_start = True
        for key in questions.keys():
            long = 0
            users[call.message.chat.id][key] = 0
            print(users)
            for i in questions[key]['answers']:
                topic = questions[key]['topic']
                answers_markup = InlineKeyboardMarkup(keyboard=None, row_width=3)
                buttons = []
                long = users[call.message.chat.id][key]
                for a in range(len(i) - 1):
                    buttons.append(InlineKeyboardButton(i[a], callback_data=str(i.index(i[a]))))
                for b in range(len(buttons)):
                    if b % 2 == 0:
                        try:
                            answers_markup.row(buttons[b], buttons[b+1])
                        except:
                            answers_markup.row(buttons[b])
                with open(file_generation(questions[key]['topic'],
                                          questions[key]['answers'].index(i) + 1), 'rb') as file:
                    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                           media=InputMediaPhoto(file), reply_markup=answers_markup)
                file.close()
                continuing = False
                #waiting(users[call.message.chat.id][key], long)
                while True:
                    if continuing:
                        break
                    else:
                        time.sleep(0.001)
    else:
        users[call.message.chat.id]['Сделано'] += 1
        print(users)
        continuing = True
        #users[call.message.chat.id][] = ''
        #check(answers_list, )


bot.polling()


# @bot.callback_query_handler(func=lambda call: call.data)
# def callback(call):
#     if call.data == 'start':
#         for i in l:
#             ...
#             continuing = False
#             while True:
#                 if continuing:
#                     break
#     else:
#          continuing = True
