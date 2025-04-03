from django.db import models

from users.models import User

class Stock(models.Model):
    name = models.CharField(max_length=255)

class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="prices")
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    variation = models.DecimalField(max_digits=10, decimal_places=2)

# Create your models here.
class UserStock(models.Model):
    class TradeType(models.TextChoices):  # ✅ TextChoices 사용
        BUYING = "buying", "Buying"
        SELLING = "selling", "Selling"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stocks")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="trades")
    trade_type = models.CharField(max_length=10, choices=TradeType.choices)  # ✅ .choices 사용
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField()
    traded_at = models.DateTimeField(auto_now_add=True)