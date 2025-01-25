# Ivy Wallet to Cashew CSV Converter

I have been a dedicated user of ([Ivy Wallet](https://ivywallet.app/)), an open-source money manager app for Android. However, as of November 5th, 2024, Ivy Wallet is ([no longer maintained](https://github.com/Ivy-Apps/ivy-wallet)) by the original developers.

In search of a reliable alternative, I discovered [Cashew](https://cashewapp.web.app).

To facilitate the transition, I developed this script to convert Ivy Wallet's CSV export into a format compatible with Cashew.

## Usage

1. **Export Data from Ivy Wallet**:
   - Open Ivy Wallet.
   - Navigate to **Settings** > **Export to CSV**.
   - Save the CSV file to a known location.

2. **Run the Conversion Script**:
   - Ensure you have Python installed on your system.
   - Download the conversion script from this repository.
   - Open a terminal or command prompt.
   - Navigate to the directory containing the script.
   - Execute the script with the following command:

     ```bash
     python3 converter.py path_to_ivy_wallet_csv path_to_output_cashew_csv
     ```

     Replace `path_to_ivy_wallet_csv` with the path to your exported Ivy Wallet CSV file, and `path_to_output_cashew_csv` with the desired path for the output Cashew CSV file.

3. **Import Data into Cashew**:
   - Open Cashew.
   - Navigate to **Settings & Customization** > **Import CSV file**.
   - Select the converted CSV file generated by the script.
   - Follow the on-screen instructions to complete the import process.

## Requirements

- Python 3.x
- `chardet` library for encoding detection. Install it using pip:

  ```bash
  pip install chardet
