import asyncio
import os
from aiogram import Bot, Dispatcher
from app.bot.handlers import router

async def main():
    """
    Main entry point for the HR Telegram Bot service.
    """
    # Hardcoded token (User choice)
    token = "8302463815:AAEtgldpuQm0QW0jv3xJCSbmNExmuJ4yb1M"
    if not token:
        print("ERROR: TELEGRAM_BOT_TOKEN not found in environment.")
        return

    bot = Bot(token=token)
    dp = Dispatcher()
    
    # Register handlers
    dp.include_router(router)
    
    print("HR Telegram Bot started. Polling...")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    asyncio.run(main())
