from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery
import config, json, keyboards
from Model import *


class User:
    def __init__(self):
        self.state = 0
        self.dictionary: Dictionary | None = None
        self.lesson: Lesson | None = None


bot = AsyncTeleBot(config.token)
users: dict[int, User] = {}
with open(config.replicas_filename, 'r', encoding='utf-8') as f:
    replicas = json.load(f)

with open(config.help_filename, 'r', encoding='utf-8') as f:
    help_text = f.read()


def with_state(state):
    def _check(message: Message):
        user = users.get(message.from_user.id)
        if user:
            return user.state == state
        return False
    return _check


def func_and(func1, func2):
    def _check(message: Message):
        return func1(message) and func2(message)
    return _check


def with_texts(*texts):
    _texts = tuple(texts)
    def _check(message: Message):
        return message.text in texts
    return _check


def with_queries(*texts):
    _texts = tuple(texts)
    def _check(query: CallbackQuery):
        return query.data in _texts
    return _check


@bot.message_handler(commands=['start'])
async def start(message: Message):
    user_id = message.from_user.id
    new_user = User()
    users[user_id] = new_user
    await bot.send_message(user_id, replicas['hello'], reply_markup=keyboards.start)


@bot.message_handler(commands=['help'])
async def start(message: Message):
    await bot.send_message(message.from_user.id,
                           help_text.replace("<", "\\<").replace(">", "\\>").replace("-", "—").replace(".", "\\."),
                           parse_mode="MarkdownV2")

@bot.message_handler(commands='load_dict')
async def load_dict(message: Message):
    user_id = message.from_user.id
    new_user = User()
    users[user_id] = new_user
    await to_wait_dict(message)


@bot.message_handler(func=with_texts("Отправить словарь"))
async def to_wait_dict(message: Message):
    user = users[message.from_user.id]
    user.state = "wait_dict"
    await bot.send_message(message.from_user.id, replicas["wait_dict"])


@bot.message_handler(func=with_state("wait_dict"))
async def get_dict(message: Message):
    user = users[message.from_user.id]
    try:
        dictionary = DictionaryParser.parse_from_string(message.text.strip())
        user.dictionary = dictionary
        user.state = "wait_mode"
        await bot.send_message(message.from_user.id, replicas["choose_mode"], reply_markup=keyboards.choose)
    except Exception as e:
        print(e)
        await bot.send_message(message.from_user.id, replicas["wrong_format"])


@bot.callback_query_handler(func=with_queries('dir', 'rev'))
async def get_mode(query: CallbackQuery):
    await bot.answer_callback_query(query.id)
    user_id = query.from_user.id
    if user_id not in users:
        return
    user = users[user_id]
    if user.state == "wait_mode":
        match query.data:
            case 'dir':
                user.lesson = Lesson(user.dictionary.direct)
            case 'rev':
                user.lesson = Lesson(user.dictionary.reverse)
            case _:
                await bot.answer_callback_query(query.id, "Error")
                return
        user.state = "wait_answer"
        message = query.message
        await bot.edit_message_text(message.text, message.chat.id, message.id, reply_markup=None)
        await bot.send_message(user_id, user.lesson.current_question)



@bot.message_handler(func=with_state("wait_answer"))
async def check_answer(message: Message):
    user_id = message.from_user.id
    user = users[user_id]
    lesson = user.lesson
    if lesson.check_answer(message.text.strip().lower()):
        lesson.right_answers += 1
        if lesson.is_question_completed():
            lesson.complete_question()
            if not lesson.is_empty():
                t1 = bot.send_message(user_id, replicas["Yes"])
                t2 = bot.send_message(user_id, lesson.current_question)
                await t1
                await t2
            else:
                user.state = 0
                await bot.send_message(user_id, replicas["thats_all"])
        else:
            await bot.send_message(user_id, replicas["and"] % (lesson.answers_count - lesson.right_answers))
    else:
        translation =  lesson.try_get_translation(message.text)
        if translation is None:
            await bot.send_message(user_id, replicas["No"])
        else:
            await bot.send_message(user_id, replicas["it_is_differ"] % translation)





import asyncio
print("Bot started")
asyncio.run(bot.infinity_polling())
