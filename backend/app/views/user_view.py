from decimal import Decimal

from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, request
from app.models import User
from app.serializers import UserRegistrationSerializer, UserSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Transaction  # Adjust the import according to your project structure
from decimal import Decimal

class UserTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the 'status' parameter from the URL (e.g., 'processing' or 'completed')
        status_filter = kwargs.get('status', 'processing')  # Default to 'processing' if not provided

        if status_filter not in ['processing', 'completed']:
            return Response({'error': 'Invalid status provided'}, status=status.HTTP_400_BAD_REQUEST)

        return self.getUserTransactionsByStatus(request, status_filter)

    def getUserTransactionsByStatus(self, request, status_filter):
        user = request.user
        assets = {}

        # Filter transactions by the status ('processing' or 'completed')
        transactions = user.transactions.filter(user=user, status=status_filter)

        for transaction in transactions:
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

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):  # Keep the HTTP method as POST
        # return self.getUserByNameAndEmail(request)
        return self.getUserById(request)

    def getUserByNameAndEmail(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')

        # If neither username nor email is provided, return an error
        if not username and not email:
            return Response({'error': 'Username or email is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter based on username or email
        try:
            # If both username and email are provided, filter by both
            if username and email:
                user = User.objects.get(username=username, email=email)
            # If only username is provided, filter by username
            elif username:
                user = User.objects.get(username=username)
            # If only email is provided, filter by email
            elif email:
                user = User.objects.get(email=email)

            # Return the user data in response
            return Response({
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def getUserById(self, request):
        user = request.user

        # If neither username nor email is provided, return an error
        if not user:
            return Response({'error': 'User is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter based on username or email
        try:
            if user.id:
                user = User.objects.get(id=user.id)

            # Return the user data in response
            return Response({
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UserRegistrationView(APIView):
    # permission_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True  # Ensure the user is active
            user.save()

            refresh = RefreshToken.for_user(user)
            print(refresh)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the password
        if check_password(password, user.password):
            # User authenticated successfully, generate tokens
            from rest_framework_simplejwt.tokens import RefreshToken

            refresh = RefreshToken.for_user(user)
            refresh.payload['user_id'] = user.id
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
