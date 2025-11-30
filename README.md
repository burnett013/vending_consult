# Vending Machine Tracker

A simple Streamlit app to track vending machine refills and inventory.

## Features
- Track Date, Location, Product, SKU, Starting Qty, Ending Qty.
- Locations: FCA Snack Machine, CFC Micro Market, CFL Micro Market.
- Reset all data.
- Email CSV report.
- Download CSV.

## Setup

### Local Development
1. Clone the repo.
2. Install requirements: `pip install -r requirements.txt`.
3. Run the app: `streamlit run app.py`.

### Email Configuration
To use the email feature, you must configure secrets.

#### On Streamlit Cloud
1. Go to your app dashboard.
2. Click the three dots next to your app -> **Settings**.
3. Click on **Secrets**.
4. Paste the contents of `secrets.toml.example` and replace the values with your actual credentials.
   - `sender_email`: Your Gmail address.
   - `sender_password`: Your Gmail App Password (not your login password).

#### Locally
Create a file `.streamlit/secrets.toml` in the project root and add the same configuration.
