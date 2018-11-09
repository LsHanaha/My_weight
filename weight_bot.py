import datetime
import telebot
import os
import matplotlib
import matplotlib.pyplot as plt
from telebot import types
from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify


bot = telebot.TeleBot('737207157:AAEDHI33HFow2WnGpDHSkyZe8ffscOlqs3I')

app = Flask(__name__)
sslify = SSLify(app)

# https://api.telegram.org/bot737207157:AAEDHI33HFow2WnGpDHSkyZe8ffscOlqs3I/setWebhook?url=howru.pythonanywhere.com/737207157:AAEDHI33HFow2WnGpDHSkyZe8ffscOlqs3I

@app.route('/737207157:AAEDHI33HFow2WnGpDHSkyZe8ffscOlqs3I', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        try:
            chat_id = r['message']['chat']['id']
            text = r['message']['text']
            username = r['message']['from']['username']
            time = datetime.datetime.now()
            f = open('/home/HowRU/My_weight/log.txt', 'a')
            f.write('date: {}, id: {}, username: {},  text: {}\n'.format(time, chat_id, username, text))
            f.close()
        except KeyError:
            chat_id = r['callback_query']['message']['chat']['id']
        if text == '/start':
            bot.send_message(chat_id, "Hello, Friend!")
        elif text == '/help':
            bot.send_message(chat_id, "I can help!")
        elif ft_is_float(text):
            input_weight(text, chat_id)
        elif text == '/plot_morning':
            create_plot(morning, date_inp, 'Morning plot')
            bot.send_photo(chat_id, open('/home/HowRU/My_weight/foo.png', 'rb'))
        elif text == '/plot_noon':
            create_plot(noon, date_inp, 'Noon plot')
            bot.send_photo(chat_id, open('/home/HowRU/My_weight/foo.png', 'rb'))
        elif text == '/plot_afternoon':
            create_plot(afternoon, date_inp, 'Afternoon plot')
            bot.send_photo(chat_id, open('/home/HowRU/My_weight/foo.png', 'rb'))
        elif text == '/plot_mid':
            add_data_to_lists()
            create_plot(middle, date_inp, 'Middle plot')
            bot.send_photo(chat_id, open('/home/HowRU/My_weight/foo.png', 'rb'))
        else:
            bot.send_message(chat_id, "What?")
        return jsonify(r)
    return '<h1>Hello</h1>'

morning = [85.7, 84.8, 84.9]
noon = [86.2, 85.5, 85.3]
afternoon = [85.5, 85.5, 85.75]
middle = [85.8, 85.2]
date_inp = [06.11, 07.11, 08.11]

def ft_is_float(text):
    try:
        float(text)
        return True
    except ValueError:
        return False

def input_weight(text, chat_id):
    if float(datetime.datetime.strftime(datetime.datetime.now(), "%d.%m")) not in date_inp:
        date_inp.append(float(datetime.datetime.strftime(datetime.datetime.now(), "%d.%m")))
        write_in_log('date_list', date_inp)
        bot.send_message(chat_id, "Date add!")
    if int(datetime.datetime.strftime(datetime.datetime.now(), "%H")) + 3 <= 12:
        add_data_to_lists()
        if len(morning) != len(date_inp):
            morning.append(float(text))
            write_in_log('morning_list', morning)
        else:
            bot.send_message(chat_id, "You already add morning today! Wait till tomorrow!")
    elif int(datetime.datetime.strftime(datetime.datetime.now(), "%H")) +3 <= 18 and int(datetime.datetime.strftime(datetime.datetime.now(), "%H")) +3 > 12:
        add_data_to_lists()
        if len(noon) != len(date_inp):
            noon.append(float(text))
            write_in_log('noon_list', noon)
        else:
            bot.send_message(chat_id, "You already add noon today! Wait till tomorrow.")
    elif int(datetime.datetime.strftime(datetime.datetime.now(), "%H")) +3 > 18:
        add_data_to_lists()
        if len(afternoon) != len(date_inp):
            afternoon.append(float(text))
            write_in_log('afternoon_list', afternoon)
        else:
            bot.send_message(chat_id, "You already add afternoon today! Wait till tomorrow!")

def add_data_to_lists():
    while len(date_inp) - len(morning) > 1:
        morning.append(morning[-1])
        write_in_log('morning_list', morning)
    while len(date_inp) - len(noon) > 1:
        noon.append(noon[-1])
        write_in_log('noon_list', noon)
    while len(date_inp) - len(afternoon) > 1:
        afternoon.append(afternoon[-1])
        write_in_log('afternoon_list', afternoon)
    if int(datetime.datetime.strftime(datetime.datetime.now(), "%H")) > 12:
        if len(morning) != len(date_inp):
            morning.append(morning[-1])
            write_in_log('morning_list', morning)
    if int(datetime.datetime.strftime(datetime.datetime.now(), "%H")) > 18:
        if len(noon) != len(date_inp):
            noon.append(noon[-1])
            write_in_log('noon_list', noon)
    if len(morning) == len(noon) and len(noon) == len(afternoon) and len(middle) != len(date_inp):
        a = float('{:.3f}'.format((morning[-1] + noon[-1] + afternoon[-1]) / 3))
        middle.append(a)
        write_in_log('Change middle', middle)


def write_in_log(text, information):
    f = open('/home/HowRU/My_weight/log.txt', 'a')
    f.write('date: {}, {}: {}\n'.format(datetime.datetime.now(), text, information))
    f.close()

def create_plot(data, date_inp, inp_title):
    try:
        os.remove('/home/HowRU/My_weight/foo.png')
    except FileNotFoundError:
        pass
    s = data
    t = date_inp

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='Date (d%m)', ylabel='Weght (kg)',
           title=inp_title)
    ax.grid()
    write_in_log('save', inp_title)
    fig.savefig('/home/HowRU/My_weight/foo.png', bbox_inches='tight')

if __name__ == "__main__":
    app.run()