import requests
from django.utils import timezone
from datetime import *
from app.models import *

def fetch_crypto_metadata():
    url = 'https://api.coincap.io/v2/assets'
    headers = {
        "Accepts": "application/json",
        "Accepts-Encoding": "gzip",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def fetch_and_save_crypto_currency_historical_data(symbol, interval):
    """
    Fetch historical data from the external API and save it to the database.
    """

    try:
        # Call the external API to fetch historical data
        response = requests.get(
            f'https://api.coincap.io/v2/assets/{symbol}/history',
            params={'interval': interval}
        )

        # Check if the response is successful
        if response.status_code != 200:
            return None, "Failed to fetch historical data from external API."

        data = response.json().get('data', [])

        # If no data is returned, return an error
        if not data:
            print("failed")
            return None, "No historical data found for the given symbol."

        # Store or replace data in the database
        for price_data in data:
            print(price_data)
            CryptoHistory.objects.update_or_create(
                symbol=price_data.get('symbol', symbol),
                # Use 'symbol' from price_data or fallback to 'symbol' variable
                time=price_data.get('time', 0),
                # Use 'time' from price_data or fallback to a default value (e.g., 0 or None)
                interval=price_data.get('interval', interval),
                # Use 'interval' from price_data or fallback to default 'interval'
                defaults={
                    'price': Decimal(price_data.get('priceUsd', 0)),  # Use get() to ensure 'priceUsd' exists
                    'date': price_data.get('date', None),  # If 'date' is missing, assign None
                    'circulatingSupply': Decimal(price_data.get('circulatingSupply', 0))
                }
            )

        return True, "Historical data saved successfully."

    except requests.exceptions.RequestException as e:
        return None, f"Request error: {str(e)}"
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"



