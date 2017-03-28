from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    nickname = models.CharField(max_length=200)
    year = models.IntegerField()

    def average_economy(self):
        fills = self.fillups.all()
        economy_list = [fill.economy() for fill in fills]
        return float(sum(economy_list)) / max(len(economy_list), 1)

    def last_economy(self):
        fill = self.fillups.first()
        if fill:
            return fill.economy()

    def last_updated(self):
        dates = list()
        fills = self.fillups.all()
        dates.extend([fill.datetime for fill in fills])
        if len(dates):
            return max(dates)
        else:
            return None

    def __str__(self):
        return self.nickname


class FillUp(models.Model):
    car = models.ForeignKey(Car, related_name='fillups', on_delete=models.CASCADE)
    odometer = models.DecimalField(max_digits=7, decimal_places=1)
    distance = models.DecimalField(max_digits=4, decimal_places=1)
    price = models.DecimalField(max_digits=4, decimal_places=3)
    quantity = models.DecimalField(max_digits=6, decimal_places=3)
    datetime = models.DateTimeField()

    def economy(self):
        return self.distance/self.quantity

    class Meta:
        ordering = ('-datetime',)
