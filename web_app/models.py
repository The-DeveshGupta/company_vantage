from django.db import models
from django.contrib.auth.models import User


class UserHistory(models.Model):
    date = models.DateField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.symbol}-{self.username}'
