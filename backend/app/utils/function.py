import requests
from datetime import datetime
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from app.models import Crypto

def update_crypto():
    # Define the CoinCap API URL for fetching all assets (cryptocurrencies)
    url = "https://api.coincap.io/v2/assets"

    try:
        # Fetch data from CoinCap API
        response = requests.get(url)

        # Check if the response is successful
        if response.status_code != 200:
            print(f"Error fetching data from CoinCap API. Status code: {response.status_code}")
            return

        # Parse the JSON response
        data = response.json().get('data', [])

        # Check if the data exists
        if not data:
            print("No data received from CoinCap API")
            return

        # Start a database transaction to avoid multiple commits
        with transaction.atomic():
            for crypto_data in data:
                # Check if the cryptocurrency already exists in the database
                symbol = crypto_data['symbol']
                name = crypto_data['name']
                price_usd = Decimal(crypto_data['priceUsd'])  # Ensure price is a Decimal
                rank = crypto_data['rank']
                market_cap = float(crypto_data["marketCapUsd"])
                volume_24h = float(crypto_data["volumeUsd24Hr"])
                change_percent_24h = float(crypto_data["changePercent24Hr"])

                model = Crypto
                timestamp_naive = datetime.now()  # This is naive
                timestamp_aware = timezone.make_aware(timestamp_naive)
                model.objects.update_or_create(
                    symbol=symbol,
                    defaults={
                        'name': name,
                        'current_price': price_usd,
                        'rank': rank,
                        'market_cap': market_cap,
                        'volume_24h': volume_24h,
                        'change_percent_24h': change_percent_24h,
                        'timestamp': timestamp_aware,  # Explicitly set the timestamp
                    }
                )

        print("Cryptocurrency data updated successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching crypto data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")