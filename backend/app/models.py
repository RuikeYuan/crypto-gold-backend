# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator
from decimal import Decimal

class Asset(models.Model):
    currentPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def updateCurrentPrice(self):
        return

    def getPriceHistory(self):
        return

    def getCurrentPrice(self):
        return

class Metal(Asset):
    metalName = models.CharField(max_length=50, choices=[('Gold', 'gold'), ('Silver', 'silver')])

class Crypto(Asset):  # Inherit from Asset without defining a conflicting field
    rank = models.IntegerField()
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    current_price = models.FloatField()
    market_cap = models.FloatField()
    volume_24h = models.FloatField()
    change_percent_24h = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Btc(Crypto):
    pass

class Eth(Crypto):
    pass

class Sol(Crypto):
    pass

class Doge(Crypto):
    pass

class User(AbstractUser):
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    groups = models.ManyToManyField(Group, related_name='app_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='app_user_permissions')

    def calculate_profit_loss_for_asset(self, asset_id):
        transactions = self.transactions.filter(asset_id=asset_id)
        total_profit_loss = Decimal('0.00')
        for transaction in transactions:
            if transaction.action == 'buy':
                total_profit_loss -= Decimal(transaction.price) * transaction.quantity
            else:
                total_profit_loss += Decimal(transaction.price) * transaction.quantity
        return total_profit_loss

    def calculate_total_loss(self):
        transactions = self.transactions.all()
        total_loss = Decimal('0.00')
        for transaction in transactions:
            if transaction.action == 'buy':
                total_loss -= Decimal(transaction.price) * transaction.quantity
            else:
                total_loss += Decimal(transaction.price) * transaction.quantity
        return total_loss

class Transaction(models.Model):
    ACTION_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('processing', 'Processing'),
    ]

    trans_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    action = models.CharField(max_length=4, choices=ACTION_CHOICES)
    quantity = models.DecimalField(max_digits=15, decimal_places=8, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=15, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processing')

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

class Forum(models.Model):
    name = models.CharField(max_length=100)
    posts = models.ManyToManyField(Post, related_name='forums')

class CryptoHistory(models.Model):
    price = models.FloatField()
    timestamp = models.DateTimeField()

    class Meta:
        abstract = True

class BtcHistory(CryptoHistory):
    pass

class EthHistory(CryptoHistory):
    pass

class SolHistory(CryptoHistory):
    pass

class DogeHistory(CryptoHistory):
    pass
