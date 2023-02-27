from django.db import models
import json


class StocksPricePredictions(models.Model):
    symbol = models.CharField(max_length=20)
    last_refreshed = models.CharField(max_length=20)
    timezone = models.CharField(max_length=20)
    data_size = models.IntegerField()
    predicted_data = models.JSONField()
    best_model = models.CharField(max_length=20)
    models_accuracy = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50)

    def set_predicted_data(self, predicted_data):
        self.predicted_data = json.dumps(predicted_data)

    def get_predicted_data(self):
        return json.loads(self.predicted_data)

    def __str__(self):
        return f'{self.symbol}-{self.best_model}-{json.loads(self.predicted_data)}'
