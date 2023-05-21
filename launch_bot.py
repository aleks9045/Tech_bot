from aiogram.utils import executor

from bot import dp
from handlers import main, admin, log_in_out, shedule, other

import logging
logging.basicConfig(level=logging.INFO)

main.register_handlers_main(dp)
admin.register_handlers_admin(dp)
log_in_out.register_handlers_log_in_out(dp)
shedule.register_handlers_shedule(dp)
other.register_handlers_shedule(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
