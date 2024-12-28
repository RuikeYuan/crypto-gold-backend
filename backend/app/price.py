import requests
from django.utils import timezone
from datetime import *
from .models import *

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

def update_price():
    data = fetch_crypto_metadata()
    if not data:
        return

    selected_symbols = {"BTC", "ETH", "DOGE", "SOL"}
    crypto_name = {
        "BTC": Btc,
        "ETH": Eth,
        "DOGE": Doge,
        "SOL": Sol,
    }

    today = date.today()
    for model in crypto_name.values():
        model.objects.exclude(timestamp__date=today).delete()

    for crypto in data["data"]:
        if crypto["symbol"] in selected_symbols:
            symbol = crypto["symbol"]
            name = crypto["name"]
            price = float(crypto["priceUsd"])
            market_cap = float(crypto["marketCapUsd"])
            volume_24h = float(crypto["volumeUsd24Hr"])
            change_percent_24h = float(crypto["changePercent24Hr"])

            model = crypto_name[symbol]
            model.objects.create(
                name=name,
                symbol=symbol,
                current_price=price,
                market_cap=market_cap,
                volume_24h=volume_24h,
                change_percent_24h=change_percent_24h,
            )

    latest_data = {}
    for symbol, model in crypto_name.items():
        latest_record = model.objects.filter(timestamp__date=today).order_by('-timestamp').first()
        latest_data[symbol] = latest_record

    return latest_data




def fetch_crypto_history():
    crypto_history_api = {
        "bitcoin": {"url": "https://api.coincap.io/v2/assets/bitcoin/history", "model": BtcHistory},
        "ethereum": {"url": "https://api.coincap.io/v2/assets/ethereum/history", "model": EthHistory},
        "dogecoin": {"url": "https://api.coincap.io/v2/assets/dogecoin/history", "model": DogeHistory},
        "solana": {"url": "https://api.coincap.io/v2/assets/solana/history", "model": SolHistory},
    }

    params = {
        "interval": "d1"
    }

    headers = {
        "Accepts": "application/json",
        "Accept-Encoding": "gzip",
    }
    for crypto, model in crypto_history_api.items():
        url = model["url"]
        model = model["model"]


        try:

            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            for record in data["data"]:
                price = float(record["priceUsd"])
                time = datetime.utcfromtimestamp(record["time"] / 1000)

                if not model.objects.filter(timestamp=time).exists():
                    model.objects.create(price=price, timestamp=time)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching : {e}")
            return None




