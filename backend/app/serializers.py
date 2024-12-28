# serializers.py
from rest_framework import serializers
from .models import User, Crypto, Metal, Transaction, Post, Reply, CryptoHistory
from django.db import models


# filepath: /Users/ruikeyuan/Desktop/endpoints/backend/app/serializers.py
from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'balance')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = ('id', 'rank', 'name', 'symbol', 'current_price')

class MetalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metal
        fields = ('id', 'name', 'current_price')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('trans_id', 'user', 'asset', 'action', 'quantity', 'price', 'time', 'status')

    def validate(self, data):
        user = data['user']
        action = data['action']
        quantity = data['quantity']
        price = data['price']
        
        if action == 'buy':
            total_cost = quantity * price
            if user.balance < total_cost:
                raise serializers.ValidationError("Insufficient funds")
        elif action == 'sell':
            # Check if user has enough assets to sell
            asset_balance = Transaction.objects.filter(
                user=user,
                asset=data['asset'],
                status='completed'
            ).aggregate(
                balance=models.Sum(
                    models.Case(
                        models.When(action='buy', then='quantity'),
                        models.When(action='sell', then=-models.F('quantity')),
                        default=0,
                        output_field=models.DecimalField()
                    )
                )
            )['balance'] or 0
            
            if asset_balance < quantity:
                raise serializers.ValidationError("Insufficient assets")
        
        return data

class CryptoHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoHistory
        fields = ('asset', 'price_usd', 'time', 'circulating_supply', 'date')

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('reply_id', 'post', 'author', 'content', 'time')

class PostSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('post_id', 'author', 'content', 'time', 'replies')