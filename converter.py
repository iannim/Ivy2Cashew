import csv
import chardet  # Library to detect encoding
from datetime import datetime
import argparse  # For handling command-line arguments

# Function to detect file encoding
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

# Function to convert Ivy's date format to Cashew's (handles both with and without milliseconds)
def convert_date_format(ivy_date):
    # Try parsing with milliseconds first
    try:
        ivy_dt = datetime.strptime(ivy_date, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        # If milliseconds are missing, parse without them
        ivy_dt = datetime.strptime(ivy_date, "%Y-%m-%dT%H:%M:%S")
    
    # Convert to Cashew's format
    return ivy_dt.strftime("%Y-%m-%d %H:%M:%S.%f")

# Function to clean and convert amount based on transaction type (INCOME/EXPENSE)
def convert_amount(amount, trans_type):
    # Clean amount by removing commas and handling string amounts like "2,046.06"
    if isinstance(amount, str):
        amount = amount.replace(",", "")  # Remove commas from string amounts

    # Now convert to a float
    amount = float(amount)

    # Adjust the sign based on transaction type
    if trans_type == "EXPENSE":
        return -abs(amount)  # Ensure it's negative for expenses
    elif trans_type == "INCOME":
        return abs(amount)  # Ensure it's positive for income
    return amount  # Default case, should not normally happen

# Read Ivy CSV and convert to Cashew CSV
def convert_ivy_to_cashew(ivy_csv_file, cashew_csv_file):
    # Detect encoding of the input CSV file
    encoding = detect_encoding(ivy_csv_file)
    print(f"Detected encoding: {encoding}")

    with open(ivy_csv_file, mode='r', encoding=encoding) as ivy_file:
        csv_reader = csv.DictReader(ivy_file)
        # Define the fieldnames for Cashew's CSV format
        fieldnames = ['Date', 'Amount', 'Category', 'Title', 'Note', 'Account']
        
        # Open the new CSV for Cashew and write transformed data
        with open(cashew_csv_file, mode='w', newline='', encoding='utf-8') as cashew_file:
            csv_writer = csv.DictWriter(cashew_file, fieldnames=fieldnames)
            csv_writer.writeheader()  # Write the header for Cashew CSV

            for row in csv_reader:
                # Skip rows that don't have essential data like Amount or Date
                if not row['Amount'] or not row['Date']:
                    continue

                if row['Type'] == 'TRANSFER':
                    # Handle transfer: create two rows, one expense and one income
                    # Expense from the source account
                    expense_row = {
                        'Date': convert_date_format(row['Date']),
                        'Amount': -abs(float(row['Transfer Amount'].replace(",", ""))),  # Make it negative
                        'Category': 'Transfer',  # Can be a custom category
                        'Title': f"Transfer to {row['To Account']}",
                        'Note': row['Title'],  # Use original title as note
                        'Account': row['Account'],
                    }
                    # Income to the destination account
                    income_row = {
                        'Date': convert_date_format(row['Date']),
                        'Amount': abs(float(row['Receive Amount'].replace(",", ""))),  # Make it positive
                        'Category': 'Transfer',  # Can be a custom category
                        'Title': f"Transfer from {row['Account']}",
                        'Note': row['Title'],  # Use original title as note
                        'Account': row['To Account'],
                    }
                    # Write both rows into Cashew CSV
                    csv_writer.writerow(expense_row)
                    csv_writer.writerow(income_row)

                else:
                    # Prepare the new row for Cashew format
                    cashew_row = {
                        'Date': convert_date_format(row['Date']),
                        'Amount': convert_amount(row['Amount'], row['Type']),
                        'Category': row['Category'],
                        'Title': row['Title'],
                        'Note': row['Description'],  # Use description from Ivy as note in Cashew
                        'Account': row['Account'],
                    }

                    # Write the converted row into the Cashew CSV
                    csv_writer.writerow(cashew_row)

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Convert Ivy Wallet CSV to Cashew CSV format.")
    parser.add_argument('input', help="Path to the Ivy Wallet CSV file")
    parser.add_argument('output', help="Path to save the converted Cashew CSV file")

    # Parse the arguments
    args = parser.parse_args()

    # Call the conversion function with provided input and output paths
    convert_ivy_to_cashew(args.input, args.output)

if __name__ == '__main__':
    main()
