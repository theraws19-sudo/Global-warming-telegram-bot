import telebot
from telebot import types
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import os
from config import TOKEN, ADMIN_CHAT_ID, DATA_FILE, NEWSAPI_KEY
import random
from datetime import datetime, timedelta
import json
import requests

BASE_TEMP = 14.0  
bot = telebot.TeleBot(TOKEN)


def load_data():
    df = pd.read_csv(DATA_FILE, skiprows=1)
    df = df[['Year', 'Jul', 'Dec']]
    df.columns = ['year', 'jul_temp', 'dec_temp']
    df = df.dropna()
    

    df['jul_temp'] = pd.to_numeric(df['jul_temp'], errors='coerce')
    df['dec_temp'] = pd.to_numeric(df['dec_temp'], errors='coerce')
    

    df['jul_abs'] = df['jul_temp'] + BASE_TEMP
    df['dec_abs'] = df['dec_temp'] + BASE_TEMP
    
    return df.dropna()

climate_facts = [
    "Уровень CO₂ в атмосфере - самый высокий за 2 миллиона лет.",
    "Последнее десятилетие стало самым теплым за всю историю наблюдений.",
    "Океаны поглощают около 30% CO₂, что приводит к их закислению.",
    "Гренландский ледяной щит теряет массу рекордными темпами.",
    "С 1993 года темпы таяния льда в Антарктиде утроились.",
    "Уровень моря поднимается из-за теплового расширения воды и таяния ледников.",
    "Волны жары стали более частыми и интенсивными из-за изменения климата.",
    "Животноводство ответственно за 14-18% всех парниковых газов.",
    "Метан в 80 раз мощнее CO₂ в первые 20 лет после выброса.",
    "Стоимость солнечной энергии снизилась на 85% за последнее десятилетие."
]

climate_tips = [
    "Замените лампы накаливания на светодиодные - они потребляют на 80% меньше энергии.",
    "Выключайте электронику из розетки, когда не используете её - даже в режиме ожидания приборы потребляют энергию.",
    "Снижайте потребление мяса - животноводство ответственно за значительную часть парниковых газов.",
    "Используйте многоразовые сумки вместо пластиковых пакетов при покупках.",
    "Пользуйтесь общественным транспортом, велосипедом или ходите пешком вместо поездок на автомобиле.",
    "Установите программируемый термостат для оптимизации отопления и охлаждения дома.",
    "Покупайте местные продукты - это сокращает выбросы от транспортировки товаров.",
    "Сортируйте отходы и сдавайте вторсырьё на переработку.",
    "Выбирайте продукты с минимальной упаковкой или без неё.",
    "Пользуйтесь многоразовой бутылкой для воды вместо покупки воды в пластиковых бутылках.",
    "Сушите белье на воздухе вместо использования сушильной машины.",
    "Посадите дерево - оно поглощает CO₂ в процессе фотосинтеза.",
    "Утеплите окна и двери в доме, чтобы уменьшить потери тепла зимой.",
    "Выбирайте энергоэффективные приборы с маркировкой А+++ при покупке.",
    "Сократите количество авиаперелётов - особенно на короткие расстояния."
]

climate_news = [
    {
        "title": "Уровень CO₂ в атмосфере достиг рекордного значения",
        "content": "Концентрация углекислого газа в атмосфере достигла 425 ppm, что является самым высоким показателем за последние 2 миллиона лет.",
        "source": "NASA",
        "date": (datetime.now() - timedelta(days=3)).strftime("%d.%m.%Y"),
        "url": "https://climate.nasa.gov/vital-signs/carbon-dioxide/"
    },
    {
        "title": "Таяние ледников Гренландии ускорилось",
        "content": "Новое исследование показывает, что ледниковый щит Гренландии теряет массу на 30% быстрее, чем предполагалось ранее.",
        "source": "Nature Journal",
        "date": (datetime.now() - timedelta(days=7)).strftime("%d.%m.%Y"),
        "url": "https://www.nature.com/articles/s41586-023-06817-8"
    },
    {
        "title": "ЕС утвердил новый план по климату",
        "content": "Европейский союз принял ambitious план по сокращению выбросов на 55% к 2030 году и достижению углеродной нейтральности к 2050 году.",
        "source": "European Commission",
        "date": (datetime.now() - timedelta(days=10)).strftime("%d.%m.%Y"),
        "url": "https://ec.europa.eu/clima/eu-action/european-green-deal_en"
    },
    {
        "title": "Климатический саммит ООН: новые обязательства",
        "content": "На климатическом саммите ООН страны представили обновленные обязательства по сокращению выбросов, но их все еще недостаточно для ограничения потепления 1,5°C.",
        "source": "UNFCCC",
        "date": (datetime.now() - timedelta(days=15)).strftime("%d.%m.%Y"),
        "url": "https://unfccc.int/process-and-meetings/the-paris-agreement/nationally-determined-contributions-ndcs"
    },
    {
        "title": "Возобновляемая энергия стала дешевле ископаемой",
        "content": "Согласно новому отчету, солнечная и ветровая энергия теперь дешевле, чем новые электростанции на ископаемом топливе в большинстве стран мира.",
        "source": "IRENA",
        "date": (datetime.now() - timedelta(days=20)).strftime("%d.%m.%Y"),
        "url": "https://www.irena.org/publications/2021/Jun/Renewable-Power-Costs-in-2020"
    },
    {
        "title": "Коралловые рифы продолжают гибнуть из-за потепления океана",
        "content": "Ученые сообщают о массовом обесцвечивании кораллов из-за рекордно высоких температур океана в тропических регионах.",
        "source": "NOAA",
        "date": (datetime.now() - timedelta(days=25)).strftime("%d.%m.%Y"),
        "url": "https://coralreefwatch.noaa.gov/satellite/index.php"
    }
]

def get_climate_news_from_api():
    """Получение новостей о климате из NewsAPI"""
    api_key = "NEWSAPI_KEY"
    url = f"https://newsapi.org/v2/everything?q=climate+change&language=ru&sortBy=publishedAt&apiKey={NEWSAPI_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'ok':
            articles = data['articles']
            formatted_news = []
            
            for article in articles[:10]: 
                formatted_news.append({
                    "title": article['title'],
                    "content": article['description'] or "Описание недоступно",
                    "source": article['source']['name'],
                    "date": article['publishedAt'][:10],
                    "url": article['url']
                })
            
            return formatted_news
        else:
            return climate_news 
    except:
        return climate_news 

# Генерация графика
def generate_plot(df, years=50):
    current_year = pd.Timestamp.now().year
    start_year = current_year - years
    recent_data = df[(df['year'] >= start_year) & (df['year'] <= current_year)]
    
    plt.figure(figsize=(12, 6))
    plt.plot(recent_data['year'], recent_data['jul_abs'], 'o-', color='red', label='Июль')
    plt.plot(recent_data['year'], recent_data['dec_abs'], 'o-', color='blue', label='Декабрь')
    plt.axhline(y=BASE_TEMP, color='black', linestyle='--', alpha=0.5, label=f'Базовая температура ({BASE_TEMP}°C)')
    plt.title(f"Абсолютные температуры ({start_year}-{current_year})", fontsize=14)
    plt.xlabel("Год", fontsize=12)
    plt.ylabel("Температура (°C)", fontsize=12)
    plt.grid(True)
    plt.legend()
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        "🌍 Привет! Я бот анализа глобального потепления.\n"
        "Используй /help для списка команд"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def send_help(message):
    text = (
        'Привет! Я бот-помощник в теме глобального потепления. Я могу:\n' 
        '🌍 Рассказать факты и развеять мифы (/facts, /myths - ⛔В разработке⛔)\n'
        '🧮 Помочь измерить твой углеродный след (/footprint) - ⛔В разработке⛔\n'
        '💡 Давать полезные советы каждый день (/tip)\n'
        '📊 Показать актуальные данные о климате (/news)\n'
        '🎯 Предложить викторину (/quiz) - ⛔В разработке⛔\n'
        '🌡️ Отправить температурные данные за последние 50 лет (/last50)\n'
        '📆 Сравнить изменения температуры в прошлом веке (/compare)\n'
        '📈 Получить график температур за последнее время (/graph)\n'
        'Выбери, что тебя интересует!\n'
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['news', 'новости'])
def send_news(message):
    actual_news = get_climate_news_from_api()
    news_item = random.choice(actual_news)
    response = f"📰 *{news_item['title']}*\n\n" \
               f"{news_item['content']}\n\n" \
               f"📅 *Дата:* {news_item['date']}\n" \
               f"📚 *Источник:* {news_item['source']}\n" \
               f"🔗 [Читать подробнее]({news_item['url']})"

    bot.send_message(message.chat.id, response, parse_mode='Markdown')

@bot.message_handler(commands=['facts'])
def send_random_fact(message):
    random_fact = random.choice(climate_facts)

    response = f"🌍 Факт о глобальном потеплении:\n\n{random_fact}"
    
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['tip', 'advice', 'совет'])
def send_random_tip(message):
    random_tip = random.choice(climate_tips)
    response = f"💡 Экосовет:\n\n{random_tip}"
    markup = types.InlineKeyboardMarkup()
    new_tip_button = types.InlineKeyboardButton("Ещё совет", callback_data='new_tip')
    markup.add(new_tip_button)

    bot.send_message(message.chat.id, response, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'new_tip')
def handle_new_tip(call):
    random_tip = random.choice(climate_tips)
    response = f"💡 Ещё один совет:\n\n{random_tip}"
    bot.edit_message_text(response, call.message.chat.id, call.message.message_id, reply_markup=call.message.reply_markup)


@bot.message_handler(commands=['last50'])
def send_last_50(message):
    df = load_data()
    current_year = pd.Timestamp.now().year
    last_50 = df[df['year'] >= (current_year - 50)]
    
    if last_50.empty:
        bot.reply_to(message, "Данные не найдены.")
        return
    
    response = "📊 Абсолютные температуры (°C):\n"
    for _, row in last_50.iterrows():
        response += f"{int(row['year'])}: Июль={row['jul_abs']:.2f} | Декабрь={row['dec_abs']:.2f}\n"
    
    bot.reply_to(message, response)

@bot.message_handler(commands=['compare'])
def send_comparison(message):
    df = load_data()
    current_year = pd.Timestamp.now().year

    period1 = df[(df['year'] >= 1924) & (df['year'] <= 1973)]
    period2 = df[(df['year'] >= current_year - 49) & (df['year'] <= current_year)]

    avg_jul_past = period1['jul_abs'].mean()
    avg_jul_recent = period2['jul_abs'].mean()
    diff_jul = avg_jul_recent - avg_jul_past
    
    avg_dec_past = period1['dec_abs'].mean()
    avg_dec_recent = period2['dec_abs'].mean()
    diff_dec = avg_dec_recent - avg_dec_past
    
    response = (
        "🔍 Сравнение периодов (абсолютные температуры):\n"
        "Июль:\n"
        f"• 1924-1973: {avg_jul_past:.2f}°C\n"
        f"• {current_year-49}-{current_year}: {avg_jul_recent:.2f}°C\n"
        f"➡️ Изменение: {diff_jul:+.2f}°C\n\n"
        "Декабрь:\n"
        f"• 1924-1973: {avg_dec_past:.2f}°C\n"
        f"• {current_year-49}-{current_year}: {avg_dec_recent:.2f}°C\n"
        f"➡️ Изменение: {diff_dec:+.2f}°C"
    )
    bot.reply_to(message, response)

@bot.message_handler(commands=['graph'])
def send_plot(message):
    df = load_data()
    plot_buffer = generate_plot(df, 50)
    bot.send_photo(message.chat.id, plot_buffer, caption="🌡️ Абсолютные температуры в июле и декабре")

if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        bot.send_message(ADMIN_CHAT_ID, "⚠️ Файл данных не найден!")
    else:
        bot.infinity_polling()