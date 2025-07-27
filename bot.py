import requests
import time
import telegram

BOT_TOKEN = '7966719638:AAGICSOyQFhzbjcBiOZLI36HTt6H2LR036c'
CHAT_ID = 259393372  # ← твой Telegram ID

# Список монет, которые отслеживаются
TRACKED = {
    'bitcoin': {'symbol': 'BTC', 'last': None},
    'ethereum': {'symbol': 'ETH', 'last': None},
    'solana': {'symbol': 'SOL', 'last': None},
    'ethereum-classic': {'symbol': 'ETC', 'last': None},
    'mask-network': {'symbol': 'MASK', 'last': None},
    'dia-data': {'symbol': 'DIA', 'last': None}
}

bot = telegram.Bot(token=BOT_TOKEN)

def get_price(coin_id):
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {'ids': coin_id, 'vs_currencies': 'usd'}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()[coin_id]['usd']

def check():
    for coin_id, data in TRACKED.items():
        try:
            current = get_price(coin_id)
            previous = data['last']
            data['last'] = current

            if previous:
                change = ((current - previous) / previous) * 100
                if abs(change) >= 5:
                    trend = "📈" if change > 0 else "📉"
                    message = (
                        f"{trend} {data['symbol']} изменился на {change:.2f}%\n"
                        f"Цена: ${current:.2f}"
                    )
                    bot.send_message(chat_id=CHAT_ID, text=message)

        except Exception as e:
            print(f"Ошибка при проверке {coin_id}: {e}")

if __name__ == '__main__':
    while True:
        check()
        time.sleep(900)  # каждые 15 минут