from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from database.models import User, db_session
from config import Config

def show_profile(update: Update, context: CallbackContext):
    user = db_session.query(User).filter_by(chat_id=update.effective_chat.id).first()
    
    profile_text = (
        "👤 الملف الشخصي\n\n"
        f"📧 البريد: {user.email}\n"
        f"💰 الرصيد: {user.balance:.2f}$\n"
        f"🎖️ نقاط الولاء: {user.loyalty_points}\n"
        f"👥 المستخدمين المُحالين: {get_referred_count(user.id)}\n"
        f"🔗 رابط الإحالة: https://t.me/{context.bot.username}?start={user.referral_code}"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔄 تحديث الرصيد", callback_data="refresh_balance")],
        [InlineKeyboardButton("📤 مشاركة الرابط", callback_data="share_ref")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
    ]
    
    update.message.reply_text(
        profile_text,
        reply_markup=InlineKeyboardMarkup(keyboard))
    

def get_referred_count(user_id: int) -> int:
    return db_session.query(User).filter_by(referred_by=user_id).count()