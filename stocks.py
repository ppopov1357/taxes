import csv

import exchange_rates

CURRENCY_RATES = {
    "USD": 1.73098,
    "CHF": 1.87484,
    "EUR": 1.95583,
    "GBP": 2.28477
}


def get_date(date_string: str) -> tuple[str, str, str]:
    return str(date_string[0:4]), str(date_string[5:7]), str(date_string[8:10])


def csv_to_list(csv_path: str) -> list[dict]:
    with open(csv_path, newline='') as csv_file:
        return list(csv.DictReader(csv_file, delimiter=',', quotechar='|'))


def csv_with_bgn_exchange_rate(csv_path: str):
    market_orders: list[dict] = csv_to_list(csv_path)

    for order in market_orders:
        currency = order['Currency (Price / share)']
        if currency == 'GBX':
            currency = 'GBP'
        date = get_date(order['Time'])

        order['Exchange rate'] = exchange_rates.get_currency_exchange_rate(currency, *date)['rate']

    return market_orders


def csv_to_dict(csv_path: str) -> dict:
    orders = csv_with_bgn_exchange_rate(csv_path)

    csv_dict = {}

    for order in orders:
        if order['Name'] not in csv_dict:
            csv_dict[order['Name']] = []

        csv_dict[order['Name']].append(order)

    return csv_dict


def main():
    market_orders = csv_to_dict('market_orders.csv')

    with open('market_orders_aggregated.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['Name', 'Total Quantity', 'Absolute quantity', 'Total Cost', 'Total Cost BGN', 'Average Price', 'Currency', 'Date',
             'Average currency rate']
        )
        for stock, market_actions in market_orders.items():

            total_orders = len(market_actions)
            currency_total = 0
            total_cost = 0
            total_quantity = 0
            absolute_quantity = 0
            currency = market_actions[0]['Currency (Price / share)']
            date = market_actions[-1]['Time']
            for action in market_actions:
                is_buy = action['Action'] == 'Market buy'
                quantity = float(action['No. of shares'])
                quantity = quantity if is_buy else -quantity
                price = float(action['Price / share'])
                total_cost += quantity * price
                total_quantity += quantity
                absolute_quantity += abs(quantity)
                currency_total += float(action['Exchange rate'])

            try:
                average_price = total_cost / absolute_quantity
            except ZeroDivisionError:
                print("here")
            if currency == 'GBX':
                total_cost = total_cost / 100
                average_price = average_price / 100

            average_price = round(average_price, 2)
            average_currency_rate = round(currency_total / total_orders, 4)
            total_cost = round(total_cost, 2)
            total_cost_bgn = round(total_cost * average_currency_rate, 2)
            total_quantity = round(total_quantity, 3)

            writer.writerow(
                [stock.replace('"', ''), total_quantity, absolute_quantity, total_cost, total_cost_bgn, average_price, currency, date,
                 average_currency_rate]
            )


if __name__ == '__main__':
    main()
