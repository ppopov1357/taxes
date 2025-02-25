import csv
import os
from decimal import Decimal

import exchange_rates


def get_date(date_string: str) -> tuple[str, str, str]:
    return str(date_string[0:4]), str(date_string[5:7]), str(date_string[8:10])


def csv_to_list(csv_path: str) -> list[dict]:
    with open(csv_path, newline='') as csv_file:
        return list(csv.DictReader(csv_file, delimiter=',', quotechar='|'))


def merge_reports(report_paths: list[str]):
    merged_report = []
    for report in report_paths:
        print(f"merging report: {report}")
        merged_report.extend(csv_to_list(report))

    return merged_report


def csv_with_bgn_exchange_rate(csv_reports: list[str]):
    market_orders: list[dict] = merge_reports(csv_reports)

    print("Calculating exchange rates...")
    for order in market_orders:
        currency = order['Currency (Price / share)']
        if currency == 'GBX':
            currency = 'GBP'
        date = get_date(order['Time'])

        order['Exchange rate'] = exchange_rates.get_currency_exchange_rate(currency, *date)['rate']

    return market_orders


def csv_to_dict(csv_reports: list[str]) -> dict:
    orders = csv_with_bgn_exchange_rate(csv_reports)

    csv_dict = {}

    for order in orders:
        key = f"{order['Ticker']}-{order['Name']}"

        if key not in csv_dict:
            csv_dict[key] = []

        csv_dict[key].append(order)

    return csv_dict


def main():
    csv_reports_path = 'market_orders'

    csv_reports = [os.path.join(csv_reports_path, report) for report in os.listdir(csv_reports_path)]
    print(csv_reports)

    market_orders = csv_to_dict(csv_reports)

    with open('market_orders_aggregated.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['Name', 'Total Quantity', 'Total Cost', 'Total Cost BGN', 'Average Price', 'Currency',
             'Date',
             'Average currency rate']
        )
        for stock, market_actions in market_orders.items():
            print(f"Processing: {stock}")

            total_orders = len(market_actions)
            currency_total = Decimal(0)
            total_cost = Decimal(0)
            total_quantity = Decimal(0)
            currency = market_actions[0]['Currency (Price / share)']
            date = market_actions[-1]['Time']
            for action in market_actions:
                is_buy = action['Action'] == 'Market buy'
                quantity = Decimal(action['No. of shares'])
                quantity = quantity if is_buy else -quantity
                price = Decimal(action['Price / share'])
                total_cost += quantity * price
                total_quantity += quantity
                currency_total += Decimal(action['Exchange rate'])
            if total_quantity <= 0:
                continue

            average_price = total_cost / total_quantity

            if currency == 'GBX':
                total_cost = total_cost / 100
                average_price = average_price / 100

            average_price = round(average_price, 2)
            average_currency_rate = round(currency_total / total_orders, 4)
            total_cost = round(total_cost, 2)
            total_cost_bgn = round(total_cost * average_currency_rate, 2)
            total_quantity = round(total_quantity, 3)
            writer.writerow(
                [stock.replace('"', ''), total_quantity, total_cost, total_cost_bgn, average_price,
                 currency, date,
                 average_currency_rate]
            )


if __name__ == '__main__':
    main()
