import csv


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
    dividents = csv_to_dict('dividends.csv')
    with open('calculated_dividends.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Total Dividend'])

        for stock, dividend_payed in dividents.items():
            total_dividend = 0
            for dividend in dividend_payed:
                total_dividend += float(dividend['Total (EUR)'])
            writer.writerow([stock.replace('"', ""), round(total_dividend, 2)])


if __name__ == '__main__':
    main()
