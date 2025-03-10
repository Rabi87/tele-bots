from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler
from database.models import Product, Transaction, db_session
from services.payment_gateway import CoinExPayment
from utils.validators import validate_payment
import logging

logger = logging.getLogger(__name__)

def show_categories(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🛡️ بروكسي خاص", callback_data="cat_proxy")],
        [InlineKeyboardButton("📞 أرقام وهمية", callback_data="cat_phone")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
    ]
    update.message.reply_text(
        "🏪 متجر الخدمات:\nاختر الفئة المطلوبة:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def list_products(update: Update, context: CallbackContext):
    query = update.callback_query
    category = query.data.split('_')[1]
    
    products = db_session.query(Product).filter(
        Product.category == category,
        Product.is_active == True,
        Product.stock > 0
    ).all()
    
    buttons = []
    for product in products:
        btn_text = f"{product.name} - {product.price:.2f}$"
        buttons.append([InlineKeyboardButton(btn_text, callback_data=f"prod_{product.id}")])
    
    buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data="shop_menu")])
    
    query.edit_message_text(
        text=f"📦 المنتجات المتاحة ({category}):",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

def product_details(update: Update, context: CallbackContext):
    query = update.callback_query
    product_id = int(query.data.split('_')[1])
    
    product = db_session.query(Product).get(product_id)
    
    if not product:
        query.answer("⚠️ المنتج غير متوفر حالياً!")
        return
    
    text = (
        f"📦 {product.name}\n\n"
        f"💵 السعر: {product.price:.2f}$\n"
        f"📝 الوصف: {product.description}\n"
        f"🛒 الكمية المتاحة: {product.stock}"
    )
    
    keyboard = [
        [InlineKeyboardButton("🛒 شراء الآن", callback_data=f"buy_{product.id}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=f"cat_{product.category}")]
    ]
    
    query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def initiate_purchase(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    product_id = int(query.data.split('_')[1])
    
    user = db_session.query(User).filter_by(chat_id=user_id).first()
    product = db_session.query(Product).get(product_id)
    
    if not product or product.stock < 1:
        query.answer("⚠️ المنتج غير متوفر حالياً!")
        return
    
    if user.balance < product.price:
        query.answer("⚠️ رصيدك غير كافي! يرجى شحن الرصيد.")
        return show_topup_options(update, context)
    
    try:
        # خصم المبلغ
        user.balance -= product.price
        product.stock -= 1
        
        # تسجيل العملية
        transaction = Transaction(
            user_id=user.id,
            amount=product.price,
            type='purchase',
            status='completed'
        )
        db_session.add(transaction)
        
        # إضافة نقاط الولاء
        user.loyalty_points += int(product.price * Config.LOYALTY_RATE)
        
        db_session.commit()
        
        # إرسال التفاصيل للمستخدم
        context.bot.send_message(
            chat_id=user_id,
            text=f"✅ تمت العملية بنجاح!\n\n{product.delivery_details}"
        )
        
    except Exception as e:
        logger.error(f"Purchase Error: {str(e)}")
        db_session.rollback()
        query.answer("❌ حدث خطأ أثناء العملية! يرجى المحاولة لاحقاً.")