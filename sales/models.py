from django.db import models

from utils.models import CreateUpdateTracker, nb


class CompanyAccount(CreateUpdateTracker):
    id = models.IntegerField(verbose_name="код ЄДРПОУ", primary_key=True)
    tov = models.CharField(verbose_name="ТОВ", max_length=1024)
    name = models.CharField(max_length=512)
    phone = models.CharField(max_length=15)
    invite_code = models.CharField(max_length=32, **nb)

    def __str__(self):
        return self.tov

class Product(CreateUpdateTracker):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name

class Region(CreateUpdateTracker):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name

class SubRegion(CreateUpdateTracker):
    name = models.CharField(max_length=512)
    region = models.ForeignKey(Region,
                               on_delete=models.CASCADE,
                               related_name="subregions",
                               related_query_name="subregion", **nb)

    def __str__(self):
        return self.name

class City(CreateUpdateTracker):
    name = models.CharField(max_length=512)
    region = models.ForeignKey(Region,
                               on_delete=models.CASCADE,
                               related_name="cities",
                               related_query_name="city", **nb)
    subregion = models.ForeignKey(SubRegion,
                                  on_delete=models.CASCADE,
                                  related_name="cities",
                                  related_query_name="city", **nb)

    def __str__(self):
        return self.name

class SalesPlacement(CreateUpdateTracker):
    class PriceTypeChoice(models.TextChoices):
        F1 = 'f1', 'З ПДВ'
        F2 = 'f2', 'Без ПДВ'

    class CurrencyChoice(models.TextChoices):
        UAH = 'uah', 'UAH ₴'
        USD = 'usd', 'USD $'

    company = models.ForeignKey(CompanyAccount,
                                on_delete=models.CASCADE,
                                related_name="sales",
                                related_query_name="sale", **nb)
    product = models.ForeignKey(Product,
                                on_delete=models.PROTECT,
                                related_name="sales",
                                related_query_name="sale", **nb)
    weight = models.IntegerField(**nb)
    basis = models.CharField(max_length=1024, **nb)
    price_type = models.CharField(choices=PriceTypeChoice.choices, max_length=2, **nb)
    currency = models.CharField(choices=CurrencyChoice.choices, max_length=3, **nb)
    price = models.CharField(**nb)

    region = models.ForeignKey(Region,
                               on_delete=models.PROTECT,
                               related_name="sales",
                               related_query_name="sale", **nb)
    subregion = models.ForeignKey(SubRegion,
                                  on_delete=models.PROTECT,
                                  related_name="sales",
                                  related_query_name="sale", **nb)
    city = models.ForeignKey(City,
                             on_delete=models.PROTECT,
                             related_name="sales",
                             related_query_name="sale", **nb)

    def __str__(self):
        return f"{self.product} | {self.company}"