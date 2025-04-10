from django.db import models

class Quantity(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} {self.time} - {self.quantity}"
