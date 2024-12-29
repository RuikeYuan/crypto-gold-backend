from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from app.models import User, Metal, Crypto, Transaction
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal

class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Use the logged-in user (from JWT or session)
        user = request.user
        # Get transaction details from the request body
        asset_type = request.data.get('asset_type')  # 'metal' or 'crypto'
        asset_id = request.data.get('asset_id')
        action = request.data.get('action')  # 'buy' or 'sell'
        quantity = request.data.get('quantity')
        price = request.data.get('price')
        status = request.data.get('status', 'processing')

        # Ensure the logged-in user is executing the transaction
        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        # Try to find the asset based on the asset type
        try:
            if asset_type == 'metal':
                asset_instance = Metal.objects.get(id=asset_id)
                content_type = ContentType.objects.get_for_model(Metal)
            elif asset_type == 'crypto':
                asset_instance = Crypto.objects.get(id=asset_id)
                content_type = ContentType.objects.get_for_model(Crypto)
            else:
                return Response({'error': 'Invalid asset type'}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'error': 'Asset not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create the transaction for the logged-in user
        transaction = Transaction.objects.create(
            user=user,
            content_type=content_type,
            object_id=asset_instance.id,
            action=action,
            quantity=Decimal(quantity),
            price=Decimal(price),
            status=status
        )

        # Return a success response
        return Response({
            'transaction_id': transaction.trans_id,
            'message': 'Transaction created successfully'
        })

    def get(self, request, *args, **kwargs):
        # Get the transaction ID from the request
        transaction_id = request.GET.get('transaction_id')

        try:
            transaction = Transaction.objects.get(trans_id=transaction_id)
        except ObjectDoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get related asset data
        asset_data = {
            'name': transaction.asset.name,
            'symbol': transaction.asset.symbol,
        }

        # If the asset is a Metal, get metal-specific data
        if isinstance(transaction.asset, Metal):
            asset_data['metal_name'] = transaction.asset.metalName
        elif isinstance(transaction.asset, Crypto):
            # If the asset is Crypto, include crypto-specific data
            asset_data['current_price'] = transaction.asset.current_price
            asset_data['market_cap'] = transaction.asset.market_cap
            asset_data['volume_24h'] = transaction.asset.volume_24h

        # Prepare the response data
        response_data = {
            'transaction_id': transaction.trans_id,
            'user': transaction.user.username,
            'asset': asset_data,
            'action': transaction.action,
            'quantity': str(transaction.quantity),
            'price': str(transaction.price),
            'status': transaction.status,
            'timestamp': transaction.time.strftime('%Y-%m-%d %H:%M:%S')
        }
        return Response(response_data, status=status.HTTP_200_OK)
