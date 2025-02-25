import requests
from bs4 import BeautifulSoup, Tag

BNB_URL: str = "https://www.bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm"

cache = {}


def get_currency_exchange_rate(currency_symbol: str, year, month, day):
    key = f"{year}-{month}-{day}"

    print(f"Getting exchange rate for currency: {currency_symbol} and date: {key}")

    if key in cache:
        print("Exchange rate found in cache")
        return cache[key][currency_symbol]

    print("Getting exchange rate from BNB")

    html = requests.get(
        BNB_URL, params={
            "group1": "first",
            "firstDays": day,
            "firstMonths": month,
            "firstYear": year
        }
    ).text
    soup = BeautifulSoup(html, 'html.parser')
    tags: list[Tag] = soup.select('table.table tbody tr:not(.last)')
    names = ['name', 'symbol', 'quantity', 'rate', 'reverse_rate']
    rates = []
    for rows in tags:
        row_data = []
        for data in rows.select("td"):
            row_data.append(data.text)
        rates.append(dict(zip(names, row_data)))

    rates = {rate['symbol']: rate for rate in rates}
    rates['EUR'] = dict(
        zip(
            names,
            ['Euro', 'EUR', '1', '1.95583', '0.5100']
        )
    )

    cache[key] = rates

    return rates.get(currency_symbol)
