from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler
from database.models import Transaction, db_session
from services.payment_gateway import CoinExPayment
import uuid

def show_topup_options(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💳 دفع مباشر", callback_data="topup_direct")],
        [InlineKeyboardButton("🪙 Coinex", callback_data="topup_coinex")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
    ]
    
    if update.callback_query:
        update.callback_query.edit_message_text(
            text="💸 اختر طريقة الشحن:",
            reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        update.message.reply_text(
            "💸 اختر طريقة الشحن:",
            reply_markup=InlineKeyboardMarkup(keyboard))