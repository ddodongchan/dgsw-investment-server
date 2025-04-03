from django.db import models

from users.models import User


# Create your models here.
class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news")
    img = models.TextField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="reports")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    reported_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()