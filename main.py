import telebot
from telebot import types

BUTTONS = ["Новая задача", "Список дел"]
todolist = []
WEEK_BUTTONS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
TIME_START = 7
TIME_END = 21


class Task:
    def __init__(self, name, task_day="", task_time=""):
        self.name = name
        self.day = task_day
        self.time = task_time


bot = telebot.TeleBot("6949879089:AAFnK5cvyVQxV6iVltunOrWBRdPSWJSZ5bw")


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    newtask_btn = types.KeyboardButton(BUTTONS[0])
    todolist_btn = types.KeyboardButton(BUTTONS[1])
    # markup.add(todolist_btn)
    # markup.add(newtask_btn)
    markup.row(newtask_btn, todolist_btn)
    bot.send_message(message.chat.id, "Привет! Что нужно сделать?", reply_markup=markup)


def add_new_task(message):
    bot.send_message(message.chat.id, "Введите название задачи")


@bot.message_handler(commands=["newtask"])
def new_task(message):
    add_new_task(message)


def print_todolist(message):
    bot.send_message(message.chat.id, "Вот твой список дел: ")
    text_list = ""
    for i, task in enumerate(todolist):
        text_list += f" задача №{i + 1}: {task.name}\n{task.day} {task.time}\n"
    bot.send_message(message.chat.id, text_list)


@bot.message_handler(commands=["todolist"])
def list(message):
    print_todolist(message)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "Привет! Вот список доступных команд: \n /start - начало работы")


@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text == BUTTONS[0]:
        add_new_task(message)
    elif message.text == BUTTONS[1]:
        print_todolist(message)
    else:
        newtask = Task(message.text)
        todolist.append(newtask)
        bot.send_message(message.chat.id, f"Добавлена задача \n {newtask.name}")
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard_buttons = []
        for day in WEEK_BUTTONS:
            day_btn = types.InlineKeyboardButton(day, callback_data=day)
            keyboard_buttons.append(day_btn)
        keyboard.add(*keyboard_buttons)
        bot.send_message(message.chat.id, "Выберите день начала задачи", reply_markup=keyboard)
        keyboard_time = types.InlineKeyboardMarkup(row_width=5)
        keyboard_buttons_time = []
        for time in range(TIME_START,TIME_END+1):
            time_text = f"{time}:00"
            time_btn = types.InlineKeyboardButton(time_text,callback_data=time_text)
            keyboard_buttons_time.append(time_btn)
        keyboard_time.add(*keyboard_buttons_time)
        bot.send_message(message.chat.id,"Выберете время начала задачи",reply_markup=keyboard_time)


@bot.callback_query_handler(func=lambda call: True)
def day_select(call):
    if len(todolist) > 0:
        todolist[-1].day = call.data
    bot.edit_message_text(f"запланирована на {call.data}",call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: True)
def time_select(call):
    if len(todolist) > 0:
        todolist[-1].time = call.data
    bot.edit_message_text(f"запланирована на {call.data}",call.message.chat.id,call.message.message_id)




bot.polling(none_stop=True, interval=0)
