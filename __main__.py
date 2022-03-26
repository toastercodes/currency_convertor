from currency_convertor.config import API_KEY, BASE_URL
from pprint import PrettyPrinter
from requests import get

printer = PrettyPrinter()

def get_currencies():
    endpoint = f'api/v7/currencies?apiKey={API_KEY}'
    url = BASE_URL + endpoint
    data = get(url).json()['results']

    data = list(data.items())
    data.sort()

    return data

def print_currencies(currencies):
    for _id, currency in currencies:
        name = currency['currencyName']

        symbol = currency.get('currencySymbol', '')
        print(f'{_id} - {name} - {symbol}')

def exchange_rate(currency1, currency2):
    endpoint = f'api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}'
    url = BASE_URL + endpoint
    data = get(url).json()
    
    if len(data) == 0:
        print('Invalid currencies.')
        return

    rate = list(data.values())[0]
    print(f'{currency1} -> {currency2} = {rate}')

    return rate

def convert(currency1, currency2, amt):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return

    try:
        amt = float(amt)
    except:
        print('Invalid amount.')

    conv_amt = rate * amt
    print(f'{currency1} {amt} = {currency2} {conv_amt}')

    return conv_amt

def main():
    currencies = get_currencies()

    print('Currency converter started!')
    print('Available commands - Convert, List, Rate')
    print()

    while True:
        command = input('Enter a command(q to quit): ').lower()

        if command == 'q':
            break
        elif command == 'list':
            print_currencies(currencies)
        elif command == 'convert':
            cur1 = input('Enter a base currency id: ').upper()
            amt = input(f'Enter an amount in {cur1}: ')
            cur2 = input('Enter a currency id to convert to: ').upper()
            convert(cur1, cur2, amt)
        elif command == 'rate':
            cur1 = input('Enter a base currency id: ').upper()
            cur2 = input('Enter a currency id to convert to: ').upper()
            exchange_rate(cur1, cur2)
        else:
            print('Unrecognized command!')
    
    print('Exiting!')

main()
