from aiogram.utils import executor
from temp import dp
from dotenv import load_dotenv


load_dotenv()

from handlers import client, admin, other

client.register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True)
