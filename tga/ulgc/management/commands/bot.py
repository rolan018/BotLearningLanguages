import re
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from asgiref.sync import sync_to_async
from aiogram.utils import executor
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from ulgc.management.app import dp
from ulgc.management.actions import ACTION_LIST
from ulgc.management.standard_widgets import get_standard_markup, get_first_markup, get_mark_markup
from ulgc.models import Profile
from ulgc.models import ActionWord
from ulgc.models import ActionLesson
from ulgc.models import ActionMaterial


class Command(BaseCommand):
    help = "Телеграм-Бот"

    def handle(self, *args, **options):

        # Обработчики
        class FSMAdmin(StatesGroup):
            name = State()
            number = State()
            post = State()
            general_question = State()
            action = State()
            word_un = State()
            word_ru = State()
            lesson_date = State()
            lesson_topic = State()
            lesson_mark = State()
            material_name = State()
            material_url = State()
            material_mark = State()

        @dp.message_handler(commands=["start"])
        async def start_command(message: types.Message):
            # Добавляем две кнопки
            markup = get_first_markup()
            await message.reply(text='Привет, это учебный проект бота для изучения иностранных языков',
                                reply_markup=markup)

        '''************************ Остановка **************************'''

        # Хэндлер на текстовое сообщение с текстом "Нет, спасибо"
        @dp.message_handler(lambda message: message.text == "Нет, спасибо")
        async def action_cancel(message: types.Message):
            remove_keyboard = types.ReplyKeyboardRemove()
            await message.answer("Ок, хорошего дня \U0001F602", reply_markup=remove_keyboard)

        @dp.message_handler(lambda message: message.text not in ["Начинаем изучать!"])
        async def get_weather(message: types.Message):
            await message.answer("Если хочешь начать, воспользуйся кнопками. Они находятся над клавиатурой, " +
                                 "слева от значка 🎤\n")

        '''************************ Анкета **************************'''

        @dp.message_handler(lambda message: message.text == "Начинаем изучать!")
        async def cm_start(message: types.Message):
            await FSMAdmin.name.set()
            remove_keyboard = types.ReplyKeyboardRemove()
            await message.answer('Супер! Сначала давай познакомимся ✌️\nНапиши своё имя', reply_markup=remove_keyboard)

        # Ловим первый ответ от пользователя
        @dp.message_handler(state=FSMAdmin.name)
        async def get_name(message: types.Message, state: FSMContext):
            if len(message.text.split()) == 1:
                async with state.proxy() as data:
                    data['name'] = message.text
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Отправить контакт", request_contact=True)
                markup.add(item1)
                await message.answer(
                    "Приятно познакомиться!\nОтправь контакт или напиши номер телефона в формате: +7xxxxxxxxxx",
                    reply_markup=markup)
                await FSMAdmin.next()
            else:
                await message.answer(text="Пожалуйста, укажи только имя (без пробелов)")

        # Ловим шестой ответ
        @dp.message_handler(content_types=['contact', 'text'], state=FSMAdmin.number)
        async def get_un_name(message: types.Message, state: FSMContext):
            if message.contact is not None:
                async with state.proxy() as data:
                    data['number'] = message.contact.phone_number
                    data['id'] = message.contact.user_id
                await FSMAdmin.next()
                remove_keyboard = types.ReplyKeyboardRemove()
                await message.answer(text='и ещё email pls 😁', reply_markup=remove_keyboard)
            elif re.fullmatch(r"\+7\d*", message.text) and len(message.text) == 12:
                async with state.proxy() as data:
                    data['number'] = message.text
                    data['id'] = message.from_id
                await FSMAdmin.next()
                remove_keyboard = types.ReplyKeyboardRemove()
                await message.answer(text='и ещё email pls 😁', reply_markup=remove_keyboard)
            else:
                await message.answer(
                    text="Вы ввели неверный номер телефона.\nПожалуйста введите номер телефона в формате +7xxxxxxxxxx."+
                         "\nИли воспользуйтесь кнопкой: Отправить контакт")

        @dp.message_handler(state=FSMAdmin.post)
        async def get_un_name(message: types.Message, state: FSMContext):
            if re.search(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$", message.text):
                async with state.proxy() as data:
                    data['post'] = message.text
                    # Производим запись в базу
                    try:
                        await sync_to_async(Profile(telegram_id=data['id'],
                                                    name=data['name'],
                                                    telephone=data['number'],
                                                    email=data['post']).save)()
                    except IntegrityError:
                        await message.reply("Вы уже регистрировались, но ничего страшного " +
                                            "продолжайте использовать наш бот")
                    data['telegram_id'] = await sync_to_async(Profile.objects.get)(telegram_id=data['id'])
                # Добавляем одну кнопку старта
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Супер, начинаем!")
                markup.add(item1)
                await message.answer(text='Отлично, давай приступим к обучению', reply_markup=markup)
                await FSMAdmin.next()
            else:
                await message.answer(text="Вы ввели неверно вашу почту.\nУкажите почту в формате: example@gmail.com")

        '''*********************** Начало ****************************'''

        # Вступление
        @dp.message_handler(state=FSMAdmin.general_question)
        async def handle_text(message: types.Message):
            if message.text == "Супер, начинаем!":
                # варианты ответа
                markup = get_standard_markup()
                await FSMAdmin.action.set()
                await message.answer(text='Выбирите, что хотите сделать', reply_markup=markup)
            else:
                await message.reply(text="Для начала необходимо пользоваться кнопками\n" +
                                         "Кнопки находятся над клавиатурой, слева от значка 🎤")

        # Отлавливание отсутствующих сообщений
        @dp.message_handler(lambda message: message.text not in ACTION_LIST, state=FSMAdmin.action)
        async def get_w(message: types.Message):
            await message.answer("Для взаимодействия с ботом используй кнопки.\nОни находятся над клавиатурой, " +
                                 "слева от значка 🎤\n")

        # Заполнение слова
        @dp.message_handler(lambda message: message.text == "Новое слово", state=FSMAdmin.action)
        async def handle_text(message: types.Message):
            # варианты ответа
            remove_keyboard = types.ReplyKeyboardRemove()
            await FSMAdmin.word_un.set()
            await message.answer(text='Введите слово на иностранном языке',
                                 reply_markup=remove_keyboard)

        @dp.message_handler(state=FSMAdmin.word_un)
        async def handle_text(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['word_un'] = message.text
            await FSMAdmin.word_ru.set()
            await message.answer(text='Отлично, теперь перевод')

        @dp.message_handler(state=FSMAdmin.word_ru)
        async def handle_text(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['word_ru'] = message.text
                text = f"{data['word_un']}-{data['word_ru']}"
                print(data['telegram_id'])
                await sync_to_async(ActionWord(telegram_id=data['telegram_id'],
                                               text=text).save)()
            markup = get_standard_markup()
            await FSMAdmin.action.set()
            await message.answer(text='Отлично, слово записано.\nВыбирите, что ещё хотите сделать', reply_markup=markup)

        # Заполнение урока
        @dp.message_handler(lambda message: message.text == "Новый урок", state=FSMAdmin.action)
        async def handle_text(message: types.Message):
            # варианты ответа
            remove_keyboard = types.ReplyKeyboardRemove()
            await FSMAdmin.lesson_date.set()
            await message.answer(text='Введите дату урока',
                                 reply_markup=remove_keyboard)

        @dp.message_handler(state=FSMAdmin.lesson_date)
        async def handle_text(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['lesson_date'] = message.text
            await FSMAdmin.lesson_topic.set()
            await message.answer(text='Отлично, теперь тему урока')

        @dp.message_handler(state=FSMAdmin.lesson_topic)
        async def handle_text(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['lesson_topic'] = message.text
            markup = get_mark_markup()
            await FSMAdmin.lesson_mark.set()
            await message.answer(text='Отлично, теперь оценка урока по 5-ти бальной шкале',
                                 reply_markup=markup)

        @dp.message_handler(state=FSMAdmin.lesson_mark)
        async def handle_text(message: types.Message, state: FSMContext):
            if message.text in ["1", "2", "3", "4", "5"]:
                async with state.proxy() as data:
                    data['lesson_mark'] = message.text
                    await sync_to_async(ActionLesson(telegram_id=data['telegram_id'],
                                                     date=data['lesson_date'],
                                                     topic=data['lesson_topic'],
                                                     mark=int(data['lesson_mark'])).save)()
                markup = get_standard_markup()
                await FSMAdmin.action.set()
                await message.answer(text='Урок записан.\nВыбирите, что ещё хотите сделать', reply_markup=markup)
            else:
                await message.reply(
                    text="Сорри, воспользуйся кнопкой пожалуйста.\nКнопки находятся над клавиатурой, слева от значка 🎤")

        # Заполнение материала
        @dp.message_handler(lambda message: message.text == "Новый материал", state=FSMAdmin.action)
        async def handle_text(message: types.Message):
            # варианты ответа
            remove_keyboard = types.ReplyKeyboardRemove()
            await FSMAdmin.material_name.set()
            await message.answer(text='Введите название материала',
                                 reply_markup=remove_keyboard)

        @dp.message_handler(state=FSMAdmin.material_name)
        async def handle_text(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['material_name'] = message.text
            await FSMAdmin.material_url.set()
            await message.answer(text='Отлично, теперь ссылку')

        @dp.message_handler(state=FSMAdmin.material_url)
        async def handle_text(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['material_url'] = message.text
            markup = get_mark_markup()
            await FSMAdmin.material_mark.set()
            await message.answer(text='Отлично, теперь оценка материала по 5-ти бальной шкале',
                                 reply_markup=markup)

        @dp.message_handler(state=FSMAdmin.material_mark)
        async def handle_text(message: types.Message, state: FSMContext):
            if message.text in ["1", "2", "3", "4", "5"]:
                async with state.proxy() as data:
                    data['material_mark'] = message.text
                    await sync_to_async(ActionMaterial(telegram_id=data['telegram_id'],
                                                       topic=data['material_name'],
                                                       url=data['material_url'],
                                                       mark=int(data['material_mark'])).save)()
                markup = get_standard_markup()
                await FSMAdmin.action.set()
                await message.answer(text='Материал записан.\nВыбирите, что ещё хотите сделать', reply_markup=markup)
            else:
                await message.reply(
                    text="Сорри, воспользуйся кнопкой пожалуйста.\nКнопки находятся над клавиатурой, слева от значка 🎤")

        # Вывод Слов
        @dp.message_handler(lambda message: message.text == "Посмотреть все слова", state=FSMAdmin.action)
        async def handle_text(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                async for Words in ActionWord.objects.filter(telegram_id=data['telegram_id']):
                    word_text = Words.text
                    await message.answer(f'{word_text}')
            # варианты ответа
            markup = get_standard_markup()
            await FSMAdmin.action.set()
            await message.answer(text='Выбирите, что ещё хотите сделать',
                                 reply_markup=markup)

        # Вывод материала
        @dp.message_handler(lambda message: message.text == "Посмотреть все материалы", state=FSMAdmin.action)
        async def handle_text(message: types.Message, state: FSMContext):
            item = 0
            async with state.proxy() as data:
                async for Materials in ActionMaterial.objects.filter(telegram_id=data['telegram_id']):
                    item += 1
                    material_topic = Materials.topic
                    material_url = Materials.url
                    material_mark = Materials.mark
                    await message.answer(f'{item}){material_topic}.\nURL:{material_url}\nОЦЕНКА:{material_mark}')
            # варианты ответа
            markup = get_standard_markup()
            await FSMAdmin.action.set()
            await message.answer(text='Выбирите, что ещё хотите сделать',
                                 reply_markup=markup)

        # Вывод уроков
        @dp.message_handler(lambda message: message.text == "Посмотреть все уроки", state=FSMAdmin.action)
        async def handle_text(message: types.Message, state: FSMContext):
            item = 0
            async with state.proxy() as data:
                async for Lessons in ActionLesson.objects.filter(telegram_id=data['telegram_id']):
                    item += 1
                    lesson_topic = Lessons.topic
                    lesson_date = Lessons.date
                    lesson_mark = Lessons.mark
                    await message.answer(f'{item}){lesson_topic}.\nДАТА УРОКА:{lesson_date}\nОЦЕНКА:{lesson_mark}')
            # варианты ответа
            markup = get_standard_markup()
            await FSMAdmin.action.set()
            await message.answer(text='Выбирите, что ещё хотите сделать',
                                 reply_markup=markup)

        # Вывод сколько всего слов записано
        @dp.message_handler(lambda message: message.text == "Сколько слов записано", state=FSMAdmin.action)
        async def handle_text(message: types.Message, state: FSMContext):
            # варианты ответа
            async with state.proxy() as data:
                res = await sync_to_async(ActionWord.objects.filter(telegram_id=data['telegram_id']).count)()
            markup = get_standard_markup()
            await message.answer(f'Всего слов: {res}')
            await FSMAdmin.action.set()
            await message.answer(text='Выбирите, что ещё хотите сделать',
                                 reply_markup=markup)
        # Запуск пуллера
        executor.start_polling(dp, skip_updates=True)
