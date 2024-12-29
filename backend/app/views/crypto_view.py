from app.utils.function import update_crypto
from app.utils.price import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Crypto
from rest_framework.permissions import IsAuthenticated, AllowAny


class CryptoHistoryView(APIView):
    """
    Handles POST requests to fetch and store historical data for a given cryptocurrency symbol and interval,
    or GET requests to retrieve historical data from the database.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        # Get symbol
        symbol = request.data.get("symbol", "")
        interval = request.data.get("interval", "d1")

        # Validate the interval
        allowed_intervals = ['m1', 'm5', 'm15', 'm30', 'h1', 'h2', 'h6', 'h12', 'd1']
        if interval not in allowed_intervals:
            return Response({
                "error": f"Invalid interval. Please use one of the following valid values: {', '.join(allowed_intervals)}"
            }, status=status.HTTP_400_BAD_REQUEST)

        success, message = fetch_and_save_crypto_currency_historical_data(symbol.lower(), interval)
        # If data storage fails, return an error message
        if not success:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        # Query the database for historical data
        historical_records = CryptoHistory.objects.filter(symbol=symbol, interval=interval).order_by('time')

        # If no data is found, return a 404 error
        if not historical_records.exists():
            return Response({"error": "No historical data found."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare the response data with historical data
        history_data = {
            "symbol": symbol,
            "interval": interval,
            "timestamps": [record.time for record in historical_records],
            "prices": [record.price for record in historical_records],
        }

        return Response(history_data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        # Handle GET logic for retrieving historical data
        symbol = request.query_params.get("symbol", "")
        interval = request.query_params.get("interval", "d1")

        # Add your logic to fetch historical data from the database
        historical_records = CryptoHistory.objects.filter(symbol=symbol, interval=interval).order_by('time')

        if not historical_records.exists():
            return Response({"error": "No historical data got."}, status=status.HTTP_404_NOT_FOUND)

        history_data = {
            "symbol": symbol,
            "interval": interval,
            "timestamps": [record.time for record in historical_records],
            "prices": [record.price for record in historical_records],
        }

        return Response(history_data, status=status.HTTP_200_OK)

    def fetch_from_api(self, request, *args, **kwargs):
        """
        Handles POST requests to submit and store historical data after validating the interval and fetching data from an external API.
        """
        symbol = request.data.get("symbol", "")
        interval = request.data.get("interval", "d1")

        # Validate the interval
        allowed_intervals = ['m1', 'm5', 'm15', 'm30', 'h1', 'h2', 'h6', 'h12', 'd1']
        if interval not in allowed_intervals:
            return Response({
                "error": f"Invalid interval. Please use one of the following valid values: {', '.join(allowed_intervals)}"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Call the external API to fetch and store historical data
        success, message = fetch_and_save_crypto_currency_historical_data(symbol, interval)

        # If data storage fails, return an error message
        if not success:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        # Return success message
        return Response({"message": message}, status=status.HTTP_200_OK)


class UpdateDeleteGetCryptoViewSet(APIView):
    """
    Handles GET, POST, PATCH, and DELETE requests for cryptocurrencies.
    """

    def get(request, *args, **kwargs):
        """
        Fetch and return the latest cryptocurrency data.
        """
        print("Starting fetch_and_return_cryptos view")

        try:
            # Fetch and save the latest crypto data (you can adjust this logic as needed)
            update_crypto()
            print("Crypto data fetched and saved")

            # Filter and fetch cryptocurrency data
            cryptos = {
                "BTC": Crypto.objects.filter(symbol="BTC"),
                "ETH": Crypto.objects.filter(symbol="ETH"),
                "DOGE": Crypto.objects.filter(symbol="DOGE"),
                "SOL": Crypto.objects.filter(symbol="SOL"),
            }

            # Prepare the data to return
            response_data = {}
            for symbol, model in cryptos.items():
                print(f"Processing {symbol} data")
                response_data[symbol] = [
                    {
                        "name": crypto.name,
                        "symbol": crypto.symbol,
                        "current_price": str(crypto.current_price),  # Convert Decimal to string for JSON serialization
                        "rank": crypto.rank,
                        "market_cap": str(crypto.market_cap),  # Adding more fields if needed
                        "volume_24h": str(crypto.volume_24h),
                        "change_percent_24h": str(crypto.change_percent_24h),
                    }
                    for crypto in model
                ]

            # Return the fetched and saved data
            print(f"Returning data: {response_data}")
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in get method: {e}")
            return Response({"error": "Failed to fetch cryptocurrency data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def delete(request, *args, **kwargs):
        """
        Delete all crypto records from the database.
        """
        print("Starting delete_all_cryptos method")

        try:
            # Ensure this is a deliberate action (you can add additional checks here if needed)
            confirm_delete = request.data.get('confirm_delete', False)
            if not confirm_delete:
                return Response({"error": "Please confirm delete by setting 'confirm_delete' to true."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Delete all crypto records from the database
            deleted_count, _ = Crypto.objects.all().delete()
            print(f"{deleted_count} crypto records deleted.")

            return Response({"message": f"{deleted_count} crypto records deleted successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in delete method: {e}")
            return Response({"error": "Failed to delete cryptocurrency data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
