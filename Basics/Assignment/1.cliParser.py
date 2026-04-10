# run this cmd == python 1.cliParser.py --file data.csv --column city --value Pune  

import argparse
import csv

def parse_csv(file_path, column, value):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row[column] == value:
                print(row)

def main():
    parser = argparse.ArgumentParser(description="Simple CSV Parser CLI Tool")
    
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--column", required=True, help="Column name to filter")
    parser.add_argument("--value", required=True, help="Value to match")
    
    args = parser.parse_args()
    
    parse_csv(args.file, args.column, args.value)

if __name__ == "__main__":
    main()