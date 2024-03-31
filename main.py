from telegram import Update
from telegram.ext import Application

from core.logging.helpers import create_logger
from core.settings import config
from core.database import init_models
from app import bot_handlers


async def init_application(application: Application) -> None:
    create_logger("telegram")
    await init_models()
    
    ...

if __name__ == "__main__":
    builder = Application.builder()
    builder.token(config.TG_TOKEN).post_init(init_application)
    
    application = builder.build()
    application.add_handlers(bot_handlers)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)
