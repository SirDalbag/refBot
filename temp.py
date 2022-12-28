from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

storage = MemoryStorage()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)

https://www.canva.com/design/DAFVvppqQJc/rGmO5ywXmgr991ITjbrCKg/view?utm_content=DAFVvppqQJc&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
