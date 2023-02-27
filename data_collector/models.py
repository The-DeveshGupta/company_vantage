from django.db import models
import json


class Ticker(models.Model):
    symbol = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50)
    symbol_type = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    market_open = models.CharField(max_length=10)
    market_close = models.CharField(max_length=10)
    timezone = models.CharField(max_length=20)
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.symbol}-{self.company_name}'


class StocksPrice(models.Model):
    symbol = models.CharField(max_length=20)
    information = models.CharField(max_length=50)
    last_refreshed = models.CharField(max_length=20)
    timezone = models.CharField(max_length=20)
    data_size = models.IntegerField()
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50)

    def set_data(self, data):
        self.data = json.dumps(data)

    def get_data(self):
        return json.loads(self.data)

    def __str__(self):
        return f'{self.symbol}-{self.information}'
