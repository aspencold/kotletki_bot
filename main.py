import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from db import init_db, add_recipe, get_random_recipe

BOT_TOKEN = os.environ['BOT_TOKEN']
ADMIN_IDS = [int(x) for x in os.environ.get('ADMIN_IDS', '').split(',')]

init_db()

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Команды:\n/recipe — случайный рецепт\n/recipe мясо — по тегу/категории\n/add — добавить рецепт (только админы)")

async def recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args) if context.args else None
    r = get_random_recipe(query)
    if not r:
        await update.message.reply_text("Рецептов не найдено.")
        return
    title, time, category, tags, desc = r
    await update.message.reply_text(
        f"🍽 *{title}* ({time})\nКатегория: {category}\nТеги: {tags}\n\n{desc}",
        parse_mode='Markdown'
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
        await update.message.reply_text("Ты не админ.")
        return
    user_state[uid] = {'step': 0, 'data': {}}
    await update.message.reply_text("Название блюда?")

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_state:
        return
    text = update.message.text
    state = user_state[uid]

    if state['step'] == 0:
        state['data']['title'] = text
        state['step'] += 1
        await update.message.reply_text("Время приготовления?")
    elif state['step'] == 1:
        state['data']['time'] = text
        state['step'] += 1
        await update.message.reply_text("Категория? (завтрак, обед, ужин)")
    elif state['step'] == 2:
        state['data']['category'] = text.lower()
        state['step'] += 1
        await update.message.reply_text("Теги (через запятую):")
    elif state['step'] == 3:
        state['data']['tags'] = [t.strip() for t in text.lower().split(',')]
        state['step'] += 1
        await update.message.reply_text("Описание приготовления:")
    elif state['step'] == 4:
        state['data']['description'] = text
        add_recipe(state['data'])
        del user_state[uid]
        await update.message.reply_text("✅ Рецепт добавлен!")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("recipe", recipe))
app.add_handler(CommandHandler("add", add))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))
app.run_polling()
