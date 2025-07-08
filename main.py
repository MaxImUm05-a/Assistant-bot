import telebot as t
from telebot import types
import maindb as data
import states as st
import questions as qu
import superstates as sust
import peewee as pw

TOKEN = ''
password = '1029384756'
bot = t.TeleBot(TOKEN)
text_osn = ['I have a question', 'Questions', 'What is your question?']
text_osob = ['I have an idea', 'Ideas', 'What is your idea?']

sust.delete_all_users()                   #Cleaning the table in which all superusers who have viewed the message are

@bot.message_handler(commands=["start"])
def start(message):
    """The main function in which the user chooses to which section he wants to write a message"""

    try:
        st.set_user(message.chat.id)
    except pw.IntegrityError:
        st.delete_user(message.chat.id)
        st.set_user(message.chat.id)

    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=text_osn[0], callback_data='osn')
    btn2 = types.InlineKeyboardButton(text=text_osob[0], callback_data='osob')
    #btn3 = types.InlineKeyboardButton(text='Critics', callback_data='propos')
    kb.add(btn1, btn2)

    bot.send_message(message.chat.id, 'Hello!')
    bot.send_message(message.chat.id, 'Choose in which section you want to contact', reply_markup=kb)



def question(message):
    id = message.chat.id

    state = st.get_state(id)

    try:
        if state == 'osn':
            qu.set_question(message.text, 'osn')
            bot.send_message(message.chat.id, 'Your question has been sent to managers')
        elif state == 'osob':
            qu.set_question(message.text, 'osob')
            bot.send_message(message.chat.id, 'Your idea has been sent to managers')
        elif state == 'propos':
            qu.set_question(message.text, 'propos')
    except:
        bot.send_message(message.chat.id, 'Sorry but I only forward text messages')
    finally:
        st.delete_user(id)


@bot.message_handler(commands=["super"])
def superuser(message):
    """Become a superuser"""

    mesg = bot.send_message(message.chat.id, 'Enter the password to become a superuser')

    bot.register_next_step_handler(mesg, superuser_next)


def superuser_next(message):
    """Verification of the password"""

    if message.text == password:
        msg = bot.send_message(message.chat.id, 'Enter your name')

        bot.register_next_step_handler(msg, register)
    else:
        bot.send_message(message.chat.id, 'The password is wrong')


def register(message):
    name = message.text
    tg_nick = message.from_user.username
    id = str(message.chat.id)

    data.set_super(name, tg_nick, id)

    bot.send_message(message.chat.id, "You are now a superuser")


@bot.message_handler(commands=["ques"])
def perevir_super(message):
    """Verification whether the user is the superuser"""

    user = message.chat.id
    supers = data.get_super()

    r = False

    for sup in supers:
        if user == sup:
            keyboard = types.InlineKeyboardMarkup()
            osn_button = types.InlineKeyboardButton(text=text_osn[1], callback_data='osn_q')
            osob_button = types.InlineKeyboardButton(text=text_osob[1], callback_data='osob_q')
            #propos_button = types.InlineKeyboardButton(text='Пропозиції', callback_data='propos_q')
            keyboard.add(osn_button, osob_button)

            bot.send_message(message.chat.id, "Which section would you like to see questions from?", reply_markup = keyboard)
            r = True

    if r == False:
        bot.send_message(message.chat.id, "You aren't a superuser")


def next_or_back(message_id, chat_id, deleted = 0):
    """Sends an edited message with the following or previous application"""

    q, q_info = sust.get_state(chat_id)

    keyboard = types.InlineKeyboardMarkup()
    if q_info != 0:
        back_button = types.InlineKeyboardButton(text='Previous', callback_data='back')
    lk_button = types.InlineKeyboardButton(text='Like', callback_data='lk')
    ds_button = types.InlineKeyboardButton(text='Dislike', callback_data='ds')
    del_button = types.InlineKeyboardButton(text='Delete', callback_data='del')
    if (len(q) - 1 > q_info and deleted == 0) or (len(q) - 2 > q_info and deleted == 1):
        next_button = types.InlineKeyboardButton(text='Next', callback_data='next')
    if q_info != 0 and ((len(q) - 1 > q_info and deleted == 0) or (len(q) - 2 > q_info and deleted == 1)):
        keyboard.add(back_button, next_button)
    elif q_info != 0:
        keyboard.add(back_button)
    elif (len(q) - 1 > q_info and deleted == 0) or (len(q) - 2 > q_info and deleted == 1):
        keyboard.add(next_button)
    #keyboard.add(lk_button, ds_button)
    keyboard.add(del_button)
    if deleted == 1:
        if len(q) == 1:
            bot.edit_message_text(message_id = message_id, chat_id = chat_id, text = 'No more new messages')
            sust.delete_user(chat_id)
        elif len(q) - 1 == q_info:
            nu_info = q_info - 1
        else:
            nu_info = q_info + 1
    elif deleted == 0:
        nu_info = q_info
    if len(q) != 1:
        try:
            bot.edit_message_text(message_id = message_id, chat_id = chat_id, text =  q[nu_info], reply_markup=keyboard)
        except t.apihelper.ApiTelegramException:
            bot.edit_message_text(message_id = message_id, chat_id = chat_id, text = q[nu_info] + '(This question already exists)',
                                  reply_markup = keyboard)


@bot.message_handler(commands=['ques_list'])
def questions_list(message):
    """Sends a list of messages from a particular section"""

    user = message.chat.id
    supers = data.get_super()

    r = False

    for sup in supers:
        if user == sup:
            keyboard = types.InlineKeyboardMarkup()
            osn_button = types.InlineKeyboardButton(text=text_osn[1], callback_data='osn_q_list')
            osob_button = types.InlineKeyboardButton(text=text_osob[1], callback_data='osob_q_list')
            #propos_button = types.InlineKeyboardButton(text='Critics', callback_data='propos_q_list')
            keyboard.add(osn_button, osob_button)

            bot.send_message(message.chat.id, "Which section would you like to see the whoke list of questions from?", reply_markup=keyboard)
            r = True

    if r == False:
        bot.send_message(message.chat.id, "You aren't a superuser")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    """A function that processes the pressed buttons"""


    id = call.message.chat.id

    if call.data == 'osn':
        msg = bot.send_message(call.message.chat.id, text_osn[2])
        st.change_state(id, 'osn')
    elif call.data == 'osob':
        msg = bot.send_message(call.message.chat.id, text_osob[2])
        st.change_state(id, 'osob')
    # # elif call.data == 'propos':
    # #     msg = bot.send_message(call.message.chat.id, text_osn[2])
    #     st.change_state(id, 'propos')
    if call.data in ('osn', 'osob', 'propos'):
        bot.register_next_step_handler(msg, question)


    if call.data in ('back', 'next', 'lk', 'ds', 'del'):
        q, q_info = sust.get_state(id)
    if call.data == 'back':
        q_info = q_info - 1
        sust.change_state(id, q, q_info)
        next_or_back(call.message.message_id, call.message.chat.id)
    elif call.data == 'lk':
        nom = qu.get_id(q, q_info)
        qu.like(nom)

        next_or_back(call.message.message_id, call.message.chat.id, 1)
        del q[q_info]
        if len(q) == q_info:
            q_info = q_info - 1
        sust.change_state(id, q, q_info)
    elif call.data == 'ds':
        nom = qu.get_id(q, q_info)
        qu.dislike(nom)

        next_or_back(call.message.message_id, call.message.chat.id, 1)
        del q[q_info]
        if len(q) == q_info:
            q_info = q_info - 1
        sust.change_state(id, q, q_info)
    elif call.data == 'del':
        nom = qu.get_id(q, q_info)
        qu.delete_question(nom)

        next_or_back(call.message.message_id, call.message.chat.id, 1)
        del q[q_info]
        if len(q) == q_info:
            q_info = q_info - 1
        sust.change_state(id, q, q_info)
    elif call.data == 'next':
        q_info = q_info + 1
        sust.change_state(id, q, q_info)
        next_or_back(call.message.message_id, call.message.chat.id)

    if call.data in ('osn_q', 'osob_q', 'propos_q'):
        q = qu.get_guestion(call.data.replace('_q', ''))

        if len(q) != 0:
            keyboard = types.InlineKeyboardMarkup()
            lk_button = types.InlineKeyboardButton(text='Like', callback_data='lk')
            ds_button = types.InlineKeyboardButton(text='Dislike', callback_data='ds')
            del_button = types.InlineKeyboardButton(text='Delete', callback_data='del')
            if len(q) > 1:
                next_button = types.InlineKeyboardButton(text='Next', callback_data='next')
                keyboard.add(next_button)
            #keyboard.add(lk_button, ds_button)
            keyboard.add(del_button)
            bot.send_message(call.message.chat.id, q[0], reply_markup=keyboard)
            q_info = 0

            try:
                sust.set_user(id, q, q_info)
            except pw.IntegrityError:
                sust.delete_user(id)
                sust.set_user(id, q, q_info)
        else:
            bot.send_message(call.message.chat.id, 'No more new messages')

    if call.data in ('osn_q_list', 'osob_q_list', 'propos_q_list'):
        q = qu.get_guestion(call.data.replace('_q_list', ''))

        if len(q) != 0:
            if call.data.replace('_q_list', '') == 'osn':
                rubr = f'"{text_osn[1]}"'
            elif call.data.replace('_q_list', '') == 'osob':
                rubr = f'"{text_osob[1]}"'
            # elif call.data.replace('_q_list', '') == 'propos':
            #     rubr = '"Пропозиції"'
            message = 'Here is the list of all question of this section %s:' % rubr
            rah = 0
            for que in q:
                rah = rah + 1
                message = message + '\n' + str(rah) + '. ' + que
            bot.send_message(call.message.chat.id, message)
        else:
            bot.send_message(call.message.chat.id, 'No more new messages')


bot.infinity_polling()