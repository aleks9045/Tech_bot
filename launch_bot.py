from aiogram.utils import executor

from start_bot import dp
from handlers import main, admin, log_in_out, old_mode_ifs, ml

import logging
logging.basicConfig(level=logging.INFO)

main.register_handlers_main(dp)
admin.register_handlers_admin(dp)
log_in_out.register_handlers_log_in_out(dp)
old_mode_ifs.register_handlers_ifs(dp)
ml.register_handlers_ml(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
