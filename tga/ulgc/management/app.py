from django.conf import settings
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot,  storage=MemoryStorage())
