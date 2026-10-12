import requests
import time

BOT_TOKEN = "8604343862:AAGDm4NGZo5IWFU44RMYgOxHA5NLMylDSvI"
CHAT_ID = "1721379903"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def main():
    send_telegram("✅ Bot Started!\nBinance Futures 5m - 3% scanner ON hai")
    last_prices = {}
    while True:
        try:
            r = requests.get("https://fapi.binance.com/fapi/v1/ticker/24hr", timeout=10).json()
            for d in r:
                sym = d['symbol']
                if not sym.endswith('USDT'): continue
                if any(x in sym for x in ['USDC','BUSD','FDUSD','TUSD']): continue

                price = float(d['lastPrice'])
                vol = float(d['quoteVolume'])

                if sym in last_prices:
                    old = last_prices[sym]
                    change = ((price - old) / old) * 100
                    if abs(change) >= 3:
                        emoji = "🚀 PUMP" if change > 0 else "📉 DUMP"
                        msg = f"{emoji} {sym}\n5m Change: {change:.2f}%\nPrice: {price}\n24h Vol: ${vol:,.0f}"
                        send_telegram(msg)

                last_prices[sym] = price
            time.sleep(300) # 5 minute
        except Exception as e:
            print(e)
            time.sleep(10)

if __name__ == "__main__":
    main()
