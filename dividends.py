import csv
import os
from datetime import datetime


DATA_DIR = 'dividends_data'


def csv_to_dict(csv_path: str) -> dict:
    with open(csv_path, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', quotechar='|')
        csv_dict = {}
        for row in reader:
            if row['Name'] not in csv_dict:
                csv_dict[row['Name']] = []

            csv_dict[row['Name']].append(row)
    return csv_dict


def backup_output(output_path: str, previous_dir: str):
    if os.path.exists(output_path):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        basename = os.path.basename(output_path)
        name, ext = os.path.splitext(basename)
        backup_name = f'{name}_{timestamp}{ext}'
        backup_path = os.path.join(previous_dir, backup_name)
        os.rename(output_path, backup_path)


def main():
    input_path = os.path.join(DATA_DIR, 'dividends.csv')
    output_path = os.path.join(DATA_DIR, 'calculated_dividends.csv')
    previous_dir = os.path.join(DATA_DIR, 'previous')

    backup_output(output_path, previous_dir)

    dividents = csv_to_dict(input_path)
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Total Dividend'])

        for stock, dividend_payed in dividents.items():
            total_dividend = 0
            for dividend in dividend_payed:
                total_dividend += float(dividend['Total'])
            writer.writerow([stock.replace('"', ""), round(total_dividend, 2)])


if __name__ == '__main__':
    main()