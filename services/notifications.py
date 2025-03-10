# services/notifications.py
from telegram import Bot
from config import Config

class Notifier:
    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_TOKEN)
    
    def send_admin_alert(self, message: str):
        self.bot.send_message(
            chat_id=Config.ADMIN_CHAT_ID,
            text=f"🚨 تنبيه إداري: {message}"
        )
    
    def notify_user(self, user_id: int, message: str):
        try:
            self.bot.send_message(
                chat_id=user_id,
                text=message
            )
        except Exception as e:
            logger.error(f"Notification Error: {str(e)}")