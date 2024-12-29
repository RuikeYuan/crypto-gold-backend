# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from decimal import Decimal

class Asset(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

    class Meta:
        abstract = True  # Define this as an abstract base class

class Metal(Asset):
    metalName = models.CharField(max_length=50, choices=[('Gold', 'gold'), ('Silver', 'silver')],default="")

class Crypto(Asset):
    rank = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="")
    symbol = models.CharField(max_length=10, default="")
    current_price = models.FloatField(default=0.0)
    market_cap = models.FloatField(default=0.0)  # Market cap in USD
    volume_24h = models.FloatField(default=0.0)  # 24h volume in USD
    change_percent_24h = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

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

    # Use a Generic Foreign Key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    asset = GenericForeignKey('content_type', 'object_id')

    action = models.CharField(max_length=4, choices=ACTION_CHOICES)
    quantity = models.DecimalField(max_digits=15, decimal_places=8, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=15, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processing')

    def __str__(self):
        return f"Transaction {self.trans_id} - {self.action} {self.quantity} of {self.asset.name}"

    def get_asset_type(self):
        """Returns the type of asset: 'metal' or 'crypto'"""
        if isinstance(self.asset, Metal):
            return 'metal'
        elif isinstance(self.asset, Crypto):
            return 'crypto'
        return 'unknown'

    def __str__(self):
        return f"Transaction {self.trans_id} - {self.action} {self.quantity} of {self.asset.name}"

    def get_asset_type(self):
        """Returns the type of asset: 'metal' or 'crypto'"""
        if isinstance(self.asset, Metal):
            return 'metal'
        elif isinstance(self.asset, Crypto):
            return 'crypto'
        return 'unknown'

    def __str__(self):
        return f"Transaction {self.trans_id} - {self.action} {self.quantity} of {self.asset.name}"

    def get_asset_type(self):
        """Returns the type of asset: 'metal' or 'crypto'"""
        if isinstance(self.asset, Metal):
            return 'metal'
        elif isinstance(self.asset, Crypto):
            return 'crypto'
        return 'unknown'

class CryptoHistory(models.Model):
    symbol = models.CharField(max_length=10)
    time = models.BigIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    date = models.DateTimeField()
    circulatingSupply = models.DecimalField(max_digits=20, decimal_places=10, default=Decimal(0))
    interval = models.CharField(max_length=5, choices=[
        ('m1', '1 Minute'),
        ('m5', '5 Minutes'),
        ('m15', '15 Minutes'),
        ('m30', '30 Minutes'),
        ('h1', '1 Hour'),
        ('h2', '2 Hours'),
        ('h6', '6 Hours'),
        ('h12', '12 Hours'),
        ('d1', '1 Day'),
    ], default='d1')

    class Meta:
        unique_together = ('symbol', 'time', 'interval')