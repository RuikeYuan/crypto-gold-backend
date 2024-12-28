# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import requests
from decimal import Decimal
from .models import User, Crypto, Metal, Transaction, Post, Reply, CryptoHistory
from .serializers import (
    UserSerializer, CryptoSerializer, MetalSerializer,
    TransactionSerializer, PostSerializer, ReplySerializer,
    CryptoHistorySerializer
)

from django.shortcuts import render
from .models import *
from .price import *
from datetime import *

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import UntypedToken
import logging
import requests
from decimal import Decimal
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Crypto
from .serializers import CryptoSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
import logging
from decimal import Decimal
from .models import Crypto
from .serializers import CryptoSerializer

class UserRegistrationView(APIView):
    # 允许未经过身份验证的用户访问
    # permission_classes = []
    authentication_classes = [] 

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True  # Ensure the user is active
            user.save()
            # 为新用户生成令牌
            refresh = RefreshToken.for_user(user)
            print(refresh) 
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = [JWTAuthentication]

    @action(detail=True, methods=['get'])
    def portfolio(self, request, pk=None):
        user = self.get_object()
        assets = {}
        
        for transaction in user.transactions.filter(status='completed'):
            asset_id = transaction.asset.id
            if asset_id not in assets:
                assets[asset_id] = {
                    'quantity': 0,
                    'total_cost': Decimal('0.00')
                }
            
            if transaction.action == 'buy':
                assets[asset_id]['quantity'] += transaction.quantity
                assets[asset_id]['total_cost'] += transaction.quantity * transaction.price
            else:
                assets[asset_id]['quantity'] -= transaction.quantity
                assets[asset_id]['total_cost'] -= transaction.quantity * transaction.price
        
        return Response(assets)



# Configure logging
logger = logging.getLogger(__name__)



# Logger for debugging
logger = logging.getLogger(__name__)

# class CryptoViewSet(models.Model):
#     queryset = Crypto.objects.all()
#     serializer_class = CryptoSerializer
#     permission_classes = []  # Optional: you can add permission classes if needed
#     authentication_classes = []  # No authentication for now

#     @action(detail=False, methods=['get'])
#     def fetch_all(self, request):
#         """
#         Fetch crypto data from CoinCap API and update the database.
#         """
#         try:
#             # Log the attempt to fetch data
#             logger.debug("Fetching crypto data from CoinCap API")
            
#             # Make a GET request to the CoinCap API
#             response = requests.get('https://api.coincap.io/v2/assets', timeout=10)
#             response.raise_for_status()  # Raise an exception for HTTP errors
            
#             # Get the 'data' field from the response JSON
#             data = response.json().get('data', [])
            
#             if not data:
#                 # If no data is found, return an error response
#                 logger.error("No data received from CoinCap API")
#                 return Response({'error': 'No data received from CoinCap API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # Log the received data for debugging
#             logger.debug(f"Received data: {data}")
            
#             # Loop through the data and update or create Crypto records
#             for crypto_data in data:
#                 Crypto.objects.update_or_create(
#                     defaults={
#                         'rank': crypto_data['rank'],
#                         'name': crypto_data['name'],
#                         'symbol': crypto_data['symbol'],
#                         'current_price': Decimal(crypto_data['priceUsd'])  # Ensure price is a Decimal
#                     }
#                 )
            
#             # Return a success response once data is updated
#             return Response({'message': 'Crypto data updated successfully'}, status=status.HTTP_200_OK)
        
#         except requests.exceptions.RequestException as e:
#             # Handle request exceptions like network issues or invalid responses
#             logger.error(f"Error fetching crypto data: {e}")
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#         except Exception as e:
#             # Handle other unexpected errors
#             logger.error(f"Unexpected error: {e}")
#             return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MetalViewSet(viewsets.ModelViewSet):
    queryset = Metal.objects.all()
    serializer_class = MetalSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def fetch_all(self, request):
        # Implement metal price fetching logic here
        # You would typically use a metals price API
        pass

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        transaction = serializer.save()
        user = transaction.user
        
        if transaction.action == 'buy':
            total_cost = transaction.quantity * transaction.price
            user.balance -= total_cost
        else:
            total_gain = transaction.quantity * transaction.price
            user.balance += total_gain
        
        user.save()
        transaction.status = 'completed'
        transaction.save()

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add_reply(self, request, pk=None):
        post = self.get_object()
        serializer = ReplySerializer(data={
            **request.data,
            'post': post.pk,
            'author': request.user.pk
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CryptoHistoryViewSet(viewsets.ModelViewSet):
#     queryset = CryptoHistory.objects.all()
#     serializer_class = CryptoHistorySerializer
#     permission_classes = [IsAuthenticated]

#     @action(detail=True, methods=['get'])
#     def fetch_history(self, request, pk=None):
#         asset = get_object_or_404(Crypto, pk=pk)
#         interval = request.query_params.get('interval', 'd1')
        
#         try:
#             response = requests.get(
#                 f'https://api.coincap.io/v2/assets/{asset.id}/history',
#                 params={'interval': interval}
#             )
            
#             if response.status_code == 200:
#                 data = response.json()['data']
#                 for price_data in data:
#                     CryptoHistory.objects.update_or_create(
#                         asset=asset,
#                         time=price_data['time'],
#                         defaults={
#                             'price_usd': Decimal(price_data['priceUsd']),
#                             'date': price_data['date'],
#                             'circulating_supply': Decimal(price_data.get('circulatingSupply', 0))
#                         }
#                     )
#                 return Response({'message': 'Price history updated successfully'})
#             return Response({'error': 'Failed to fetch history'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


def crypto_view(request, symbol):
    update_price()
    fetch_crypto_history()

    crypto_models = {
        "BTC": Btc,
        "ETH": Eth,
        "DOGE": Doge,
        "SOL": Sol,
    }

    history_models = {
        "BTC": BtcHistory,
        "ETH": EthHistory,
        "DOGE": DogeHistory,
        "SOL": SolHistory,
    }

    model = crypto_models[symbol]

    today_data = model.objects.order_by('timestamp')

    trend_data = {
        "timestamps": [record.timestamp.strftime('%H:%M:%S') for record in today_data],
        "prices": [record.current_price for record in today_data],
        "changes": [record.change_percent_24h for record in today_data],
        "volumes": [record.volume_24h for record in today_data],
    }

    latest_data = today_data.last()

    history_model = history_models[symbol]
    historical_records = history_model.objects.order_by('timestamp')  # Oldest to newest
    history_data = {
        "timestamps": [record.timestamp.strftime('%Y-%m-%d') for record in historical_records],
        "prices": [record.price for record in historical_records],
    }

    context = {
        "symbol": symbol,
        "latest_record": latest_data,
        "trend_data": trend_data,
        "history_data": history_data,
    }
    print(today_data)

    return render(request, 'market_view_crypto.html', context)
       