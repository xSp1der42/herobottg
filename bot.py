import telebot
from telebot import types
import os
import json
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
CHANNEL = os.getenv('CHANNEL_USERNAME')

bot = telebot.TeleBot(TOKEN)

# Файл для хранения глобальной статистики
STATS_FILE = 'stats.json'

# --- БАЗА ПЕРСОНАЖЕЙ (25 штук) ---
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
    # Вопросы 11-20
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

user_progress = {}
user_scores = {}

# --- ФУНКЦИИ СТАТИСТИКИ ---
def load_stats():
    if not os.path.exists(STATS_FILE):
        # Если файла нет, создаем с нулями
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
    
    # Сортируем топ-5 самых частых бравлеров
    brawler_counts = {k: v for k, v in stats.items() if k != "total_plays"}
    sorted_brawlers = sorted(brawler_counts.items(), key=lambda x: x[1], reverse=True)[:10] # Покажем Топ-10
    
    msg = "*Глобальная статистика игроков:*\n\n"
    for b_id, count in sorted_brawlers:
        if count > 0:
            percent = (count / total) * 100
            name = brawlers[b_id]["name"]
            msg += f"• {name} — {percent:.1f}% ({count} чел.)\n"
    return msg


# --- ПРОВЕРКА ПОДПИСКИ ---
def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        # Если бот не админ или канал указан неверно, пускаем дальше, чтобы бот не сломался
        return False

def require_sub_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_url = types.InlineKeyboardButton("👉 Подписаться на канал", url=f"https://t.me/{CHANNEL.replace('@', '')}")
    btn_check = types.InlineKeyboardButton("✅ Я подписался", callback_data="check_sub")
    markup.add(btn_url, btn_check)
    return markup


# --- ЛОГИКА БОТА ---
@bot.message_handler(commands=['start'])
def start_quiz(message):
    chat_id = message.chat.id
    
    if not check_sub(message.from_user.id):
        bot.send_message(
            chat_id, 
            f"✋ Привет! Чтобы пройти тест «Кто ты из Brawl Stars?», подпишись на наш канал {CHANNEL}!",
            reply_markup=require_sub_markup()
        )
        return

    init_test(chat_id)

def init_test(chat_id):
    user_progress[chat_id] = 0
    # Создаем словарь очков для текущего пользователя
    user_scores[chat_id] = {key: 0 for key in brawlers.keys()}
    
    bot.send_message(chat_id, "🎮 Привет! Ответь на 20 вопросов и узнай, кто ты из Brawl Stars! Погнали!")
    send_question(chat_id)

def send_question(chat_id):
    q_index = user_progress[chat_id]
    
    if q_index >= len(questions):
        show_result(chat_id)
        return

    q_data = questions[q_index]
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Чтобы уместить передачу данных в callback_data (лимит 64 байта), 
    # передаем просто индекс ответа от 0 до 3
    for i, answer in enumerate(q_data["answers"]):
        button = types.InlineKeyboardButton(answer["text"], callback_data=f"ans_{i}")
        markup.add(button)

    bot.send_message(
        chat_id, 
        f"Вопрос {q_index + 1}/{len(questions)}\n\n*{" + q_data['text'] + "}*", 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    
    # Обработка кнопки "Проверить подписку"
    if call.data == "check_sub":
        if check_sub(call.from_user.id):
            bot.delete_message(chat_id, call.message.message_id)
            init_test(chat_id)
        else:
            bot.answer_callback_query(call.id, "❌ Ты еще не подписался!", show_alert=True)
        return

    # Обработка ответов на вопросы
    if call.data.startswith("ans_"):
        if chat_id not in user_progress:
            bot.send_message(chat_id, "Тест устарел, напиши /start.")
            return

        q_index = user_progress[chat_id]
        ans_index = int(call.data.split("_")[1])
        
        # Получаем список бравлеров, которым нужно начислить балл за этот ответ
        target_brawlers = questions[q_index]["answers"][ans_index]["brawler"]
        
        for b_id in target_brawlers:
            if b_id in user_scores[chat_id]:
                user_scores[chat_id][b_id] += 1
        
        user_progress[chat_id] += 1
        
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
        send_question(chat_id)

def show_result(chat_id):
    scores = user_scores[chat_id]
    
    # Находим победителя
    result_brawler_id = max(scores, key=scores.get)
    result_data = brawlers[result_brawler_id]
    
    # Обновляем глобальную статистику
    update_global_stats(result_brawler_id)
    
    # Получаем текст со статистикой (в процентах)
    stats_text = get_percentages()
    
    final_text = f"🎉 Твой результат подсчитан!\n\nТы — *{result_data['name']}*!\n\n"
    final_text += stats_text
    final_text += "\nНажми /start, чтобы пройти еще раз."
    
    bot.send_photo(
        chat_id, 
        photo=result_data["photo"], 
        caption=final_text,
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    print("Бот запущен! Ожидание сообщений...")
    bot.polling(none_stop=True)