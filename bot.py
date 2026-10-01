import telebot
from telebot import types
import os
import json
import threading
from flask import Flask
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
CHANNEL = os.getenv('CHANNEL_USERNAME')

bot = telebot.TeleBot(TOKEN)
STATS_FILE = 'stats.json'

# --- ФЕЙКОВЫЙ ВЕБ-СЕРВЕР ДЛЯ RENDER ---
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Бот работает! Сервер активен.</h1><p>Добавь эту ссылку в UptimeRobot.</p>"

# --- БАЗА ПЕРСОНАЖЕЙ ---
brawlers = {
    "shelly": {"name": "Шелли 🔫", "photo": "https://static.wikia.nocookie.net/brawlstars/images/0/08/Shelly_Skin-Default.png"},
    "colt": {"name": "Кольт 🎯", "photo": "https://static.wikia.nocookie.net/brawlstars/images/7/7b/Colt_Skin-Default.png"},
    "el_primo": {"name": "Эль Примо 🥊", "photo": "https://static.wikia.nocookie.net/brawlstars/images/3/30/El_Primo_Skin-Default.png"},
    "poco": {"name": "Поко 🎸", "photo": "https://static.wikia.nocookie.net/brawlstars/images/a/a2/Poco_Skin-Default.png"},
    "mortis": {"name": "Мортис 🦇", "photo": "https://static.wikia.nocookie.net/brawlstars/images/e/ea/Mortis_Skin-Default.png"},
    "edgar": {"name": "Эдгар 🧣", "photo": "https://static.wikia.nocookie.net/brawlstars/images/3/36/Edgar_Skin-Default.png"},
    "leon": {"name": "Леон 🦎", "photo": "https://static.wikia.nocookie.net/brawlstars/images/7/73/Leon_Skin-Default.png"},
    "spike": {"name": "Спайк 🌵", "photo": "https://static.wikia.nocookie.net/brawlstars/images/7/7c/Spike_Skin-Default.png"},
    "crow": {"name": "Ворон 🐦‍⬛", "photo": "https://static.wikia.nocookie.net/brawlstars/images/7/7b/Crow_Skin-Default.png"},
    "dynamike": {"name": "Динамайк 🧨", "photo": "https://static.wikia.nocookie.net/brawlstars/images/8/87/Dynamike_Skin-Default.png"},
    "piper": {"name": "Пайпер ☂️", "photo": "https://static.wikia.nocookie.net/brawlstars/images/7/71/Piper_Skin-Default.png"},
    "frank": {"name": "Фрэнк 🧟‍♂️", "photo": "https://static.wikia.nocookie.net/brawlstars/images/f/f7/Frank_Skin-Default.png"},
    "tara": {"name": "Тара 👁️", "photo": "https://static.wikia.nocookie.net/brawlstars/images/0/07/Tara_Skin-Default.png"},
    "gene": {"name": "Джин 🧞‍♂️", "photo": "https://static.wikia.nocookie.net/brawlstars/images/5/52/Gene_Skin-Default.png"},
    "max": {"name": "Макс ⚡", "photo": "https://static.wikia.nocookie.net/brawlstars/images/c/c5/Max_Skin-Default.png"},
    "surge": {"name": "Вольт 🤖", "photo": "https://static.wikia.nocookie.net/brawlstars/images/e/e9/Surge_Skin-Default.png"},
    "buzz": {"name": "Базз 🦖", "photo": "https://static.wikia.nocookie.net/brawlstars/images/3/30/Buzz_Skin-Default.png"},
    "fang": {"name": "Фэнг 👟", "photo": "https://static.wikia.nocookie.net/brawlstars/images/3/33/Fang_Skin-Default.png"},
    "cordelius": {"name": "Корделиус 🍄", "photo": "https://static.wikia.nocookie.net/brawlstars/images/0/00/Cordelius_Skin-Default.png"},
    "chester": {"name": "Честер 🃏", "photo": "https://static.wikia.nocookie.net/brawlstars/images/8/86/Chester_Skin-Default.png"},
    "mandy": {"name": "Мэнди 🍬", "photo": "https://static.wikia.nocookie.net/brawlstars/images/8/82/Mandy_Skin-Default.png"},
    "rt": {"name": "R-T 🖥️", "photo": "https://static.wikia.nocookie.net/brawlstars/images/0/06/RT_Skin-Default.png"},
    "willow": {"name": "Виллоу 🐸", "photo": "https://static.wikia.nocookie.net/brawlstars/images/8/83/Willow_Skin-Default.png"},
    "amber": {"name": "Амбер 🔥", "photo": "https://static.wikia.nocookie.net/brawlstars/images/8/85/Amber_Skin-Default.png"},
    "gale": {"name": "Гэйл ❄️", "photo": "https://static.wikia.nocookie.net/brawlstars/images/2/23/Gale_Skin-Default.png"}
}

# --- 20 ВОПРОСОВ ---
questions = [
    {"text": "Какой у тебя стиль игры?", "answers": [
        {"text": "Прыгаю на врага и уничтожаю", "brawler": ["edgar", "el_primo", "fang"]},
        {"text": "Держусь вдалеке, снайперю", "brawler": ["piper", "mandy", "colt"]},
        {"text": "Бегаю из кустов, бью в спину", "brawler": ["leon", "cordelius", "buzz"]},
        {"text": "Помогаю команде, контроля карту", "brawler": ["poco", "gene", "gale"]}]},
    {"text": "Выбери свой тип урона:", "answers": [
        {"text": "Огромный урон вблизи", "brawler": ["shelly", "bull", "chester"]},
        {"text": "Метание через стены", "brawler": ["dynamike", "willow", "sprout"]},
        {"text": "Быстрые тычки издалека", "brawler": ["crow", "spike", "rt"]},
        {"text": "Огонь по площади", "brawler": ["amber", "emz", "sandy"]}]},
    {"text": "Твоя реакция, если союзник слил катку?", "answers": [
        {"text": "Злюсь и иду в соло-режим", "brawler": ["edgar", "mortis", "crow"]},
        {"text": "Пофиг, начинаю заново", "brawler": ["spike", "poco", "chester"]},
        {"text": "Анализирую ошибки", "brawler": ["rt", "max", "tara"]},
        {"text": "Ломаю телефон", "brawler": ["surge", "frank", "dynamike"]}]},
    {"text": "Твой любимый режим?", "answers": [
        {"text": "Столкновение (ШД)", "brawler": ["leon", "edgar", "buzz"]},
        {"text": "Броулбол", "brawler": ["mortis", "el_primo", "fang"]},
        {"text": "Захват кристаллов", "brawler": ["gene", "tara", "poco"]},
        {"text": "Нокаут", "brawler": ["piper", "mandy", "crow"]}]},
    {"text": "Какая суперспособность тебе ближе?", "answers": [
        {"text": "Стать невидимым", "brawler": ["leon", "sandy", "cordelius"]},
        {"text": "Стянуть всех врагов в точку", "brawler": ["tara", "gene", "jacky"]},
        {"text": "Резкий рывок/прыжок", "brawler": ["edgar", "mortis", "crow"]},
        {"text": "Прокачать себя", "brawler": ["surge", "max", "8bit"]}]},
    {"text": "Выбери скорость передвижения:", "answers": [
        {"text": "Я должен быть самым быстрым!", "brawler": ["max", "mortis", "crow"]},
        {"text": "Средняя, баланс наше все", "brawler": ["shelly", "colt", "spike"]},
        {"text": "Медленный, но очень жирный", "brawler": ["frank", "8bit", "pam"]},
        {"text": "Зависит от ульты", "brawler": ["surge", "ash", "meg"]}]},
    {"text": "Сколько у тебя должно быть здоровья (ХП)?", "answers": [
        {"text": "Очень много (Танк)", "brawler": ["frank", "el_primo", "buster"]},
        {"text": "Мало, но я уворотливый", "brawler": ["crow", "piper", "spike"]},
        {"text": "Средне, могу выжить", "brawler": ["shelly", "tara", "gene"]},
        {"text": "Лечусь во время атаки!", "brawler": ["edgar", "mortis", "pam"]}]},
    {"text": "Какой гаджет ты предпочтешь?", "answers": [
        {"text": "Щит, чтобы не убили", "brawler": ["edgar", "crow", "tick"]},
        {"text": "Телепорт или рывок", "brawler": ["surge", "max", "shelly"]},
        {"text": "Дополнительный урон", "brawler": ["colt", "piper", "spike"]},
        {"text": "Оглушение врага", "brawler": ["dynamike", "fang", "buzz"]}]},
    {"text": "Твой характер в жизни:", "answers": [
        {"text": "Тихий и скрытный", "brawler": ["leon", "spike", "crow"]},
        {"text": "Энергичный и шумный", "brawler": ["max", "surge", "el_primo"]},
        {"text": "Токсичный (люблю дизлайки)", "brawler": ["edgar", "mortis", "dynamike"]},
        {"text": "Веселый и дружелюбный", "brawler": ["poco", "chester", "lou"]}]},
    {"text": "Какая редкость круче?", "answers": [
        {"text": "Легендарная", "brawler": ["leon", "crow", "spike"]},
        {"text": "Мифическая", "brawler": ["mortis", "tara", "max"]},
        {"text": "Эпическая/Хроматическая", "brawler": ["edgar", "surge", "fang"]},
        {"text": "Редкая/Начальная", "brawler": ["shelly", "colt", "el_primo"]}]},
    {"text": "Что ты делаешь в кустах?", "answers": [
        {"text": "Кемплю всю игру", "brawler": ["shelly", "bull", "buzz"]},
        {"text": "Прячусь, чтобы захилиться", "brawler": ["crow", "piper", "max"]},
        {"text": "Жду момента для ульты", "brawler": ["tara", "frank", "dynamike"]},
        {"text": "У меня пассивка на кусты", "brawler": ["rosa", "piper", "sprout"]}]},
    {"text": "Выбери эстетику персонажа:", "answers": [
        {"text": "Мрачная / Хэллоуин", "brawler": ["mortis", "frank", "willow"]},
        {"text": "Милая / Природа", "brawler": ["spike", "sprout", "bea"]},
        {"text": "Технологии / Роботы", "brawler": ["surge", "rt", "8bit"]},
        {"text": "Огонь и магия", "brawler": ["amber", "gene", "tara"]}]},
    {"text": "Твое отношение к автоатаке?", "answers": [
        {"text": "Спамлю кнопку нон-стоп!", "brawler": ["edgar", "el_primo", "amber"]},
        {"text": "Только целюсь ручками", "brawler": ["piper", "dynamike", "colt"]},
        {"text": "Вблизи авто, вдали ручками", "brawler": ["shelly", "leon", "crow"]},
        {"text": "Атака сама наводится (ульта)", "brawler": ["gene", "tara", "sandy"]}]},
    {"text": "Как ты добиваешь врага с 1 ХП?", "answers": [
        {"text": "Яд сделает свое дело", "brawler": ["crow", "willow", "byron"]},
        {"text": "Догоняю на скорости", "brawler": ["max", "mortis", "leon"]},
        {"text": "Перекидываю бомбу через стену", "brawler": ["dynamike", "grom", "tick"]},
        {"text": "Пуля снайпера", "brawler": ["piper", "mandy", "bea"]}]},
    {"text": "Выбери питомца/сущность в помощь:", "answers": [
        {"text": "Медведь или тень", "brawler": ["nita", "tara", "penny"]},
        {"text": "Маленькие взрывные штуки", "brawler": ["tick", "mr_p", "spike"]},
        {"text": "Мне никто не нужен, я соло", "brawler": ["edgar", "colt", "fang"]},
        {"text": "Турель для команды", "brawler": ["pam", "8bit", "jessie"]}]},
    {"text": "Если на тебя идет танк?", "answers": [
        {"text": "Замедляю или отбрасываю", "brawler": ["gale", "emz", "gene"]},
        {"text": "Встречаю в лоб! Кто кого?", "brawler": ["shelly", "bull", "el_primo"]},
        {"text": "Убегаю сверкая пятками", "brawler": ["piper", "dynamike", "crow"]},
        {"text": "Перепрыгиваю его", "brawler": ["mortis", "edgar", "surge"]}]},
    {"text": "Какой значок (пин) ставишь после килла?", "answers": [
        {"text": "Красный дизлайк 👎", "brawler": ["edgar", "mortis", "buzz"]},
        {"text": "Крутые очки 😎", "brawler": ["surge", "colt", "buster"]},
        {"text": "Смеющийся смайлик 😂", "brawler": ["chester", "dynamike", "leon"]},
        {"text": "Сердечко ❤️", "brawler": ["poco", "spike", "piper"]}]},
    {"text": "Выбери роль в команде:", "answers": [
        {"text": "Агрессор (делаю киллы)", "brawler": ["fang", "edgar", "mortis"]},
        {"text": "Защитник (держу центр)", "brawler": ["pam", "frank", "8bit"]},
        {"text": "Саппорт (хил, бафы)", "brawler": ["poco", "max", "gene"]},
        {"text": "Контроль (не даю пройти)", "brawler": ["spike", "crow", "gale"]}]},
    {"text": "Твой любимый цвет?", "answers": [
        {"text": "Красный / Огненный", "brawler": ["amber", "dynamike", "el_primo"]},
        {"text": "Зеленый / Природный", "brawler": ["spike", "leon", "willow"]},
        {"text": "Фиолетовый / Темный", "brawler": ["tara", "mortis", "frank"]},
        {"text": "Яркий / Желтый", "brawler": ["max", "poco", "chester"]}]},
    {"text": "Какая фраза тебе ближе?", "answers": [
        {"text": "I am a creature of the night!", "brawler": ["mortis", "crow", "tara"]},
        {"text": "ЕЕЕЕЕЛЬ ПРИМО!", "brawler": ["el_primo", "edgar", "fang"]},
        {"text": "*Звуки молчания/радости*", "brawler": ["spike", "poco", "surge"]},
        {"text": "Let's go get 'em!", "brawler": ["shelly", "colt", "max"]}]}
]

# НОВАЯ СИСТЕМА СОХРАНЕНИЯ ДАННЫХ ПОЛЬЗОВАТЕЛЯ
user_sessions = {}

def load_stats():
    if not os.path.exists(STATS_FILE):
        initial_stats = {key: 0 for key in brawlers.keys()}
        initial_stats["total_plays"] = 0
        with open(STATS_FILE, 'w') as f:
            json.dump(initial_stats, f)
        return initial_stats
    with open(STATS_FILE, 'r') as f:
        return json.load(f)

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

def update_global_stats(brawler_id):
    stats = load_stats()
    stats[brawler_id] = stats.get(brawler_id, 0) + 1
    stats["total_plays"] += 1
    save_stats(stats)

def get_percentages():
    stats = load_stats()
    total = stats.get("total_plays", 0)
    if total == 0:
        return "Пока никто не прошел тест."
    brawler_counts = {k: v for k, v in stats.items() if k != "total_plays"}
    sorted_brawlers = sorted(brawler_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    msg = "*Глобальная статистика игроков:*\n\n"
    for b_id, count in sorted_brawlers:
        if count > 0:
            percent = (count / total) * 100
            name = brawlers[b_id]["name"]
            msg += f"• {name} — {percent:.1f}%\n"
    return msg

def check_sub(user_id):
    if not CHANNEL: return True
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

@bot.message_handler(commands=['start'])
def start_quiz(message):
    chat_id = message.chat.id
    if not check_sub(message.from_user.id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("👉 Подписаться", url=f"https://t.me/{CHANNEL.replace('@', '')}"),
            types.InlineKeyboardButton("✅ Я подписался", callback_data="check_sub")
        )
        bot.send_message(chat_id, f"✋ Привет! Чтобы пройти тест, подпишись на канал {CHANNEL}!", reply_markup=markup)
        return
    
    user_sessions[chat_id] = {'step': 0, 'answers': {}, 'msg_ids': {}}
    bot.send_message(chat_id, "🎮 Привет! Ответь на 20 вопросов и узнай, кто ты из Brawl Stars! Погнали!")
    send_or_edit_question(chat_id)

def send_or_edit_question(chat_id, edit_msg_id=None):
    step = user_sessions[chat_id]['step']
    if step >= len(questions):
        show_result(chat_id)
        return

    q_data = questions[step]
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for i, answer in enumerate(q_data["answers"]):
        button = types.InlineKeyboardButton(answer["text"], callback_data=f"ans_{i}")
        markup.add(button)
        
    if step > 0:
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))

    text = f"Вопрос {step + 1}/{len(questions)}\n\n*{q_data['text']}*"

    if edit_msg_id:
        bot.edit_message_text(chat_id=chat_id, message_id=edit_msg_id, text=text, reply_markup=markup, parse_mode="Markdown")
    else:
        msg = bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
        user_sessions[chat_id]['msg_ids'][step] = msg.message_id

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    
    if call.data == "check_sub":
        if check_sub(call.from_user.id):
            bot.delete_message(chat_id, call.message.message_id)
            user_sessions[chat_id] = {'step': 0, 'answers': {}, 'msg_ids': {}}
            bot.send_message(chat_id, "🎮 Погнали!")
            send_or_edit_question(chat_id)
        else:
            bot.answer_callback_query(call.id, "❌ Ты еще не подписался!", show_alert=True)
        return

    if chat_id not in user_sessions:
        bot.answer_callback_query(call.id, "Тест устарел, напиши /start", show_alert=True)
        return

    step = user_sessions[chat_id]['step']

    if call.message.message_id != user_sessions[chat_id]['msg_ids'].get(step):
        bot.answer_callback_query(call.id, "Используй активные кнопки ниже 👇")
        return

    if call.data == "back":
        bot.delete_message(chat_id, call.message.message_id)
        user_sessions[chat_id]['step'] -= 1
        new_step = user_sessions[chat_id]['step']
        if new_step in user_sessions[chat_id]['answers']:
            del user_sessions[chat_id]['answers'][new_step]
            
        prev_msg_id = user_sessions[chat_id]['msg_ids'][new_step]
        send_or_edit_question(chat_id, edit_msg_id=prev_msg_id)
        return

    if call.data.startswith("ans_"):
        ans_index = int(call.data.split("_")[1])
        user_sessions[chat_id]['answers'][step] = ans_index
        
        chosen_text = questions[step]["answers"][ans_index]["text"]
        original_text = questions[step]["text"]
        
        new_text = f"Вопрос {step + 1}/{len(questions)}\n\n*{original_text}*\n\n✅ Твой ответ: _{chosen_text}_"
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=new_text, parse_mode="Markdown", reply_markup=None)
        
        user_sessions[chat_id]['step'] += 1
        send_or_edit_question(chat_id)

def show_result(chat_id):
    scores = {key: 0 for key in brawlers.keys()}
    answers = user_sessions[chat_id]['answers']
    
    for q_idx, ans_idx in answers.items():
        target_brawlers = questions[q_idx]["answers"][ans_idx]["brawler"]
        for b_id in target_brawlers:
            if b_id in scores:
                scores[b_id] += 1
                
    result_brawler_id = max(scores, key=scores.get)
    result_data = brawlers[result_brawler_id]
    
    update_global_stats(result_brawler_id)
    stats_text = get_percentages()
    
    final_text = f"🎉 Твой результат подсчитан!\n\nТы — *{result_data['name']}*!\n\n{stats_text}\nНажми /start, чтобы пройти еще раз."
    bot.send_photo(chat_id, photo=result_data["photo"], caption=final_text, parse_mode="Markdown")

# --- ЗАПУСК БОТА И СЕРВЕРА ---
def run_bot():
    print("Бот запущен в фоновом потоке...")
    bot.polling(none_stop=True)

if __name__ == '__main__':
    # Запускаем телеграм-бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Запускаем Flask-сервер в основном потоке на порту, который выделит Render
    port = int(os.environ.get('PORT', 10000))
    print(f"Веб-сервер запущен на порту {port}...")
    app.run(host='0.0.0.0', port=port)