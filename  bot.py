import logging
import os
from telegram.ext import Updater, CommandHandler, ConversationHandler
from database import init_db
from handlers.registration import (
    start,
    register_email,
    register_password,
    REGISTER_EMAIL,
    REGISTER_PASSWORD
)

# تهيئة التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    # تهيئة قاعدة البيانات
    init_db()
    
    # تهيئة البوت
    updater = Updater(os.getenv('TELEGRAM_TOKEN'))
    dp = updater.dispatcher
    
    # إضافة المعالجات
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REGISTER_EMAIL: [MessageHandler(Filters.text & ~Filters.command, register_email)],
            REGISTER_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, register_password)]
        },
        fallbacks=[]
    )
    
    dp.add_handler(conv_handler)
    
    # تشغيل البوت
    if 'DYNO' in os.environ:
        PORT = int(os.environ.get('PORT', 5000))
        updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=os.getenv('TELEGRAM_TOKEN'),
            webhook_url=f"https://your-app.herokuapp.com/{os.getenv('TELEGRAM_TOKEN')}"
        )
    else:
        updater.start_polling()
    
    updater.idle()

if __name__ == '__main__':
    main()