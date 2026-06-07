#!/usr/bin/env python3
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

user_state = {}

# ========== КЛАВИАТУРЫ ==========
main_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📝 Заказать работу", callback_data='order')],
    [InlineKeyboardButton("⏰ Сроки", callback_data='terms')],
    [InlineKeyboardButton("💬 Консультация", callback_data='consult')],
    [InlineKeyboardButton("💰 Узнать цену", callback_data='price')]
])

terms_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("💰 Узнать цену", callback_data='price')],
    [InlineKeyboardButton("💬 Консультация", callback_data='consult')],
    [InlineKeyboardButton("📝 Заказать работу", callback_data='order')]
])

price_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📝 Заказать работу", callback_data='order')],
    [InlineKeyboardButton("⏰ Сроки", callback_data='terms')],
    [InlineKeyboardButton("💬 Предложить свою цену", callback_data='offer_price')],
    [InlineKeyboardButton("💬 Консультация", callback_data='consult')]
])

reply_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton("📝 Заказать работу")],
    [KeyboardButton("⏰ Сроки"), KeyboardButton("💬 Консультация")],
    [KeyboardButton("💰 Узнать цену")]
], resize_keyboard=True)

# ========== ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ==========
async def send_message(update: Update, text: str, parse_mode: str = 'Markdown', reply_markup=None):
    """Отправляет сообщение в ответ на callback или обычное сообщение"""
    if update.callback_query:
        await update.callback_query.message.reply_text(text, parse_mode=parse_mode, reply_markup=reply_markup)
        await update.callback_query.answer()
    else:
        await update.message.reply_text(text, parse_mode=parse_mode, reply_markup=reply_markup)

# ========== ОСНОВНЫЕ ФУНКЦИИ ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Уважаемый клиент!\n\n"
        "На связи Заместитель профессора.\n"
        "Принимаю заказы на курсовые, дипломные работы, отчёты по практике и другие академические задачи.\n\n"
        "📌 Регламент работы*\n"
        "① Вы направляете тему и желаемый срок\n"
        "② Я определяю стоимость и фиксирую дедлайн\n"
        "③ Вы получаете готовую работу\n\n"
        "Для оформления заказа нажмите кнопку снизу.",
        reply_markup=reply_keyboard,
        parse_mode='HTML'
    )

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Меню:", reply_markup=reply_keyboard)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Используйте /start или /menu для отображения клавиатуры.")

async def send_order_request(update: Update, user_id: int):
    user_state[user_id] = 'waiting_order'
    msg = (
        "📋 *Что мне нужно от вас:*\n\n"
        "① Тема работы\n"
        "② Методичка (если есть)\n"
        "③ Титульный лист (если есть — файлом)\n"
        "④ Срок выполнения\n"
        "⑤ Дополнительно: пожелания, условия, рекомендации\n\n"
        "Пришлите всё в одном сообщении.\n\n"
        "После получения я изучу тему, прикину сроки и свяжусь с вами."
    )
    await send_message(update, msg)

async def send_terms(update: Update):
    text = (
        "⏰ *Сроки выполнения*\n\n"
        "Курсовая — от 3 дней\n"
        "Диплом — от 20 дней\n"
        "Отчёт — от 2 дней\n"
        "Срочный заказ — от 1 дня (обсуждаемо)\n\n"
        "📌 Напишите тему и срок — я скажу точную дату."
    )
    await send_message(update, text, reply_markup=terms_keyboard)

async def send_consult(update: Update):
    text = (
        "💬 *Консультация*\n\n"
        "По всем вопросам пишите сюда. Я — автор студенческих работ и создатель сервиса. Отвечаю лично.\n\n"
        "📱 *Мои контакты:*\n"
        "• Telegram: @miumiy_mi\n"
        "Спасибо! Ваше обращение принято.\n"
        "Специалист свяжется с вами в ближайшее время. Обычно это занимает не более 15–20 минут.\n\n"
        "А пока можете посмотреть полезные материалы в нашем сообществе."
    )
    await send_message(update, text)

async def send_price(update: Update):
    text = (
        "💰 *Прайс-лист*\n\n"
        "📘 *Курсовые и дипломные*\n"
        "Курсовая работа — от 3 000 ₽\n"
        "Дипломная работа — от 25 000 ₽\n\n"
        "📝 *Рефераты и эссе*\n"
        "Реферат — от 1 300 ₽\n"
        "Эссе — от 1 000 ₽\n"
        "Доклад / статья — от 1 000 ₽\n"
        "НИР — от 2 000 ₽\n\n"
        "📊 *Отчёты и практика*\n"
        "Отчёт (учебная) — от 1 300 ₽\n"
        "Отчёт (производств.) — от 1 500 ₽\n"
        "Дневник практики — от 2 200 ₽\n\n"
        "🎨 *Творческие работы*\n"
        "Презентация — от 1 200 ₽\n"
        "Буклет / постер — от 1 200 ₽\n\n"
        "🔄 *Сопровождение и правки* — БЕСПЛАТНО\n\n"
        "Цены указаны как ориентир. Итоговая стоимость зависит от объёма, сложности, срочности.\n"
        "Для точного расчёта напишите тему и срок."
    )
    await send_message(update, text, reply_markup=price_keyboard)

async def send_offer_request(update: Update, user_id: int):
    user_state[user_id] = 'waiting_offer'
    text = (
        "💡 *Предложите свою цену — мы обсудим*\n\n"
        "У нас есть фиксированный прайс. Но каждая ситуация — индивидуальна.\n\n"
        "Напишите ваш бюджет — подберем вариант и обсудим.\n\n"
        "📌 *Инструкция*\n"
        "① Пришлите задание, методичку и вашу цену (одним сообщением)\n"
        "② С вами свяжется автор для обсуждения"
    )
    await send_message(update, text)

# ========== ОБРАБОТЧИКИ СООБЩЕНИЙ ==========
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    username = update.effective_user.username or update.effective_user.first_name

    if user_id in user_state:
        state = user_state[user_id]
        if state == 'waiting_order':
            await update.message.reply_text(
                "✅ Спасибо за доверие!\n\n"
                "Ваш заказ принят.\n"
                "Я изучу тему, прикину сроки и свяжусь с вами в ближайшее время.\n\n"
                "Если что-то срочно — пишите. Я на связи.",
                reply_markup=reply_keyboard
            )
            await context.bot.send_message(chat_id=5004116032, text=f"Новый заказ от @{username}:\n{text}")
            del user_state[user_id]
            return
        elif state == 'waiting_offer':
            await update.message.reply_text(
                "🎓 Спасибо, ваш заказ принят! 🎓\n\n"
                "Я передал информацию автору — он скоро напишет вам, чтобы обсудить все детали. Обычно мы отвечаем в течение часа (но чаще быстрее).\n\n"
                "✨ Добро пожаловать в сотрудничество с All-Student ✨",
                reply_markup=reply_keyboard
            )
            await context.bot.send_message(chat_id=5004116032, text=f"Предложение цены от @{username}:\n{text}")
            del user_state[user_id]
            return

    if text == "📝 Заказать работу":
        await send_order_request(update, user_id)
    elif text == "⏰ Сроки":
        await send_terms(update)
    elif text == "💬 Консультация":
        await send_consult(update)
    elif text == "💰 Узнать цену":
        await send_price(update)
    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки меню.", reply_markup=reply_keyboard)

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name

    if update.message.document:
        content = f"[Файл] {update.message.document.file_name}"
    elif update.message.photo:
        content = f"[Фото] (ID: {update.message.photo[-1].file_id})"
    elif update.message.video:
        content = f"[Видео] {update.message.video.file_name}"
    else:
        content = "[Вложение]"

    if user_id in user_state and user_state[user_id] == 'waiting_order':
        await update.message.reply_text(
            "✅ Спасибо за доверие!\n\n"
            "Ваш заказ принят.\n"
            "Я изучу тему, прикину сроки и свяжусь с вами в ближайшее время.\n\n"
            "Если что-то срочно — пишите. Я на связи.",
            reply_markup=reply_keyboard
        )
        await context.bot.send_message(chat_id=5004116032, text=f"Новый заказ от @{username}:\n{content}")
        del user_state[user_id]
    elif user_id in user_state and user_state[user_id] == 'waiting_offer':
        await update.message.reply_text(
            "🎓 Спасибо, ваш заказ принят! 🎓\n\n"
            "Я передал информацию автору — он скоро напишет вам, чтобы обсудить все детали. Обычно мы отвечаем в течение часа (но чаще быстрее).\n\n"
            "✨ Добро пожаловать в сотрудничество с All-Student ✨",
            reply_markup=reply_keyboard
        )
        await context.bot.send_message(chat_id=5004116032, text=f"Предложение цены от @{username}:\n{content}")
        del user_state[user_id]
    else:
        await update.message.reply_text("Пожалуйста, начните с /start и выберите действие.", reply_markup=reply_keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    if data == 'order':
        await send_order_request(update, user_id)
    elif data == 'terms':
        await send_terms(update)
    elif data == 'consult':
        await send_consult(update)
    elif data == 'price':
        await send_price(update)
    elif data == 'offer_price':
        await send_offer_request(update, user_id)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL | filters.VIDEO, handle_file))

    logger.info("Бот запущен и работает...")
    app.run_polling()

if __name__ == '__main__':
    main()