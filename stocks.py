import csv

CURRENCY_RATES = {
    "USD": 1.73098,
    "CHF": 1.87484,
    "EUR": 1.95583,
    "GBP": 2.28477
}


def csv_to_dict(csv_path: str) -> dict:
    with open(csv_path, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', quotechar='|')
        csv_dict = {}
        for row in reader:
            if row['Name'] not in csv_dict:
                csv_dict[row['Name']] = []

            csv_dict[row['Name']].append(row)
    return csv_dict


def main():
    market_orders = csv_to_dict('market_orders.csv')

    with open('market_orders_aggregated.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Total Quantity', 'Total Cost', 'Total Cost BGN', 'Average Price', 'Currency', 'Date'])
        for stock, market_actions in market_orders.items():

            total_cost = 0
            total_quantity = 0
            currency = market_actions[0]['Currency (Price / share)']
            date = market_actions[-1]['Time']
            for action in market_actions:
                quantity_bought = float(action['No. of shares'])
                price = float(action['Price / share'])
                total_cost += quantity_bought * price
                total_quantity += quantity_bought

            average_price = total_cost / total_quantity
            if currency == 'GBX':
                total_cost = total_cost / 100
                average_price = average_price / 100
                currency = 'GBP'

            average_price = round(average_price, 2)
            total_cost = round(total_cost, 2)
            total_cost_bgn = round(total_cost * CURRENCY_RATES[currency], 2)
            total_quantity = round(total_quantity, 3)

            writer.writerow([stock.replace('"', ''), total_quantity, total_cost, total_cost_bgn, average_price, currency, date])


if __name__ == '__main__':
    main()
