from rest_framework import serializers
from .models import Ticker, StocksPrice


class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = '__all__'


class StocksPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StocksPrice
        fields = '__all__'
