from binance.client import Client
import time

client = Client(tld='com')

listTiks = []

def fetchTicks():
    ticks = []

    while True:
        try:
            list_of_tickers = client.futures_symbol_ticker()
        except Exception as e:
            print(e)
            with open("log.txt", "a") as file:
                message = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()) + ' ERROR: ' + str(e) + "\n"
                file.write(message)
            time.sleep(2)
        else:
            break

    for tick in list_of_tickers:
        if tick['symbol'][-4:] != 'USDT':
            continue
        ticks.append(tick['symbol'])
    return ticks

def analyzeCurrency(tick, interval):
    while True:
        try:
            klines = client.futures_klines(symbol=tick, interval=interval, limit=1)
        except Exception as e:
            print(e)
            with open("log.txt", "a") as file:
                message = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()) + ' ERROR: ' + str(e) + "\n"
                file.write(message)
            time.sleep(2)
        else:
            break

    nKlines = len(klines) - 1
    oldClose = float(klines[0][1])
    newClose = float(klines[nKlines][4])
    percentage = round((newClose - oldClose) / oldClose * 100, 2)

    listTiks.append((tick, oldClose, newClose, percentage))

def showResults():
    sorted_list = sorted(listTiks, key=lambda result: result[3])
    for r in sorted_list:
        print("TICK: " + r[0] + " OLD: " + str(r[1]) + " NEW: " + str(r[2]) + " PERCENTAGE: " + str(r[3]) + "%")

def selectTimeframe():
    while True:
        print("Select the timeframe to analyze the candles:")
        print("1. 1m")
        print("2. 5m")
        print("3. 15m")
        print("4. 1h")
        print("5. 4h")
        print("6. 1d")
        option = input("Enter the number of the desired option: ")

        if option == '1':
            return Client.KLINE_INTERVAL_1MINUTE
        elif option == '2':
            return Client.KLINE_INTERVAL_5MINUTE
        elif option == '3':
            return Client.KLINE_INTERVAL_15MINUTE
        elif option == '4':
            return Client.KLINE_INTERVAL_1HOUR
        elif option == '5':
            return Client.KLINE_INTERVAL_4HOUR
        elif option == '6':
            return Client.KLINE_INTERVAL_1DAY
        else:
            print("Invalid option. Please enter a valid number.")
