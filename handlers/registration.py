from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from database.models import User, db_session
from services.email_service import send_confirmation_email
import bcrypt, secrets
from datetime import datetime, timedelta
from config import Config

# حالات المحادثة
REGISTER_EMAIL, REGISTER_PASSWORD = range(2)

def start(update: Update, context: CallbackContext):
    user = db_session.query(User).filter_by(chat_id=update.effective_chat.id).first()
    if user:
        update.message.reply_text("مرحبًا بك مجددًا!")
        return ConversationHandler.END
    update.message.reply_text("الرجاء إدخال بريدك الإلكتروني:")
    return REGISTER_EMAIL

def register_email(update: Update, context: CallbackContext):
    email = update.message.text
    # ... (التحقق من صحة البريد)
    context.user_data['email'] = email
    update.message.reply_text("الرجاء إدخال كلمة المرور:")
    return REGISTER_PASSWORD

def register_password(update: Update, context: CallbackContext):
    password = update.message.text
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    new_user = User(
        chat_id=update.effective_chat.id,
        email=context.user_data['email'],
        password_hash=hashed_pw,
        referral_code=f"REF-{secrets.token_hex(4)}"
    )
    
    db_session.add(new_user)
    db_session.commit()
    
    send_confirmation_email(new_user.email)
    update.message.reply_text("تم التسجيل! تحقق من بريدك للتأكيد.")
    return ConversationHandler.END