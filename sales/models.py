from django.db import models
from django.template.loader import get_template
from django.utils.crypto import get_random_string
from users.models import TelegramUser
from utils.models import CreateUpdateTracker, nb


def get_default_invite_code():
    return get_random_string(length=32)


class CompanyAccount(CreateUpdateTracker):
    id = models.CharField(verbose_name="код ЄДРПОУ", primary_key=True, max_length=64)
    tov = models.CharField(verbose_name="ТОВ", max_length=1024)
    name = models.CharField(max_length=512)
    phone = models.CharField(max_length=15)
    invite_code = models.CharField(max_length=32, **nb)
    tg_user = models.OneToOneField(TelegramUser,
                                   on_delete=models.SET_NULL,
                                   related_name="company_account",
                                   **nb)

    class Meta:
        verbose_name = 'CompanyAccount'
        verbose_name_plural = 'Company accounts'

    def __str__(self):
        return self.tov

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = get_default_invite_code()

        super().save(*args, **kwargs)


class Product(CreateUpdateTracker):
    name = models.CharField(max_length=512)

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class Region(CreateUpdateTracker):
    name = models.CharField(max_length=512)

    class Meta:
        ordering = ['name']
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.name


class SubRegion(CreateUpdateTracker):
    name = models.CharField(max_length=512)
    region = models.ForeignKey(Region,
                               on_delete=models.CASCADE,
                               related_name="subregions")

    class Meta:
        ordering = ['name']
        verbose_name = 'SubRegion'
        verbose_name_plural = 'SubRegions'

    def __str__(self):
        return self.name


class City(CreateUpdateTracker):
    name = models.CharField(max_length=512)
    region = models.ForeignKey(Region,
                               on_delete=models.CASCADE,
                               related_name="cities")
    subregion = models.ForeignKey(SubRegion,
                                  on_delete=models.CASCADE,
                                  related_name="cities")

    class Meta:
        ordering = ['name']
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class SalesPlacement(CreateUpdateTracker):
    class PriceTypeChoice(models.TextChoices):
        F1 = 'f1', 'З ПДВ'
        F2 = 'f2', 'Без ПДВ'

    class CurrencyChoice(models.TextChoices):
        UAH = 'uah', 'ГРН'
        USD = 'usd', 'USD'

    class StatusChoice(models.TextChoices):
        DRAFT = 'draft', 'DRAFT'
        POSTED = 'posted', 'POSTED'
        DELETED = 'deleted', 'DELETED'

    company = models.ForeignKey(CompanyAccount,
                                on_delete=models.CASCADE,
                                related_name="sales", **nb)
    product = models.ForeignKey(Product,
                                on_delete=models.PROTECT,
                                related_name="sales", **nb)
    weight = models.IntegerField(**nb)
    basis = models.CharField(max_length=1024, **nb)
    price_type = models.CharField(choices=PriceTypeChoice.choices, max_length=2, **nb)
    currency = models.CharField(choices=CurrencyChoice.choices, max_length=3, **nb)
    price = models.CharField(**nb)

    region = models.ForeignKey(Region,
                               on_delete=models.PROTECT,
                               related_name="sales", **nb)
    subregion = models.ForeignKey(SubRegion,
                                  on_delete=models.PROTECT,
                                  related_name="sales", **nb)
    city = models.ForeignKey(City,
                             on_delete=models.PROTECT,
                             related_name="sales", **nb)

    status = models.CharField(choices=StatusChoice.choices,
                              default=StatusChoice.DRAFT,
                              max_length=32)

    class Meta:
        verbose_name = 'Sale placement'
        verbose_name_plural = 'Sale Placements'

    def __str__(self):
        return f"{self.product} | {self.company}"

    @staticmethod
    def generate_sale_preview(chat_id, user_data):
        template = get_template('sale_preview.html')

        print("user_data:", user_data)
        print("chat_id:", chat_id)
        company_account = CompanyAccount.objects.filter(
            tg_user_id=chat_id
        ).first()
        product_name = None
        region_name = None
        subregion_name = None
        city_name = None

        product_id = user_data.get("product_id")
        if product_id:
            product_name = Product.objects.filter(id=product_id).first().name

        region_id = user_data.get("region_id")
        if region_id:
            region_name = Region.objects.filter(id=region_id).first().name

        subregion_id = user_data.get("subregion_id")
        if region_id:
            subregion_name = SubRegion.objects.filter(id=subregion_id).first().name

        city_id = user_data.get("city_id")
        if city_id:
            city_name = City.objects.filter(id=city_id).first().name

        basis = user_data.get("basis")
        weight = user_data.get("weight")
        price = user_data.get("price")
        try:
            currency = user_data.get("currency")
            currency = SalesPlacement.CurrencyChoice[currency.upper()].label
            price_type = user_data.get("price_type")
            price_type = SalesPlacement.PriceTypeChoice[price_type.upper()].label
        except KeyError as e:
            print(e)
            currency = None
            price_type = None
        context = {
            "company_account": company_account,
            "product_name": product_name,
            "weight": weight,
            "region_name": region_name,
            "subregion_name": subregion_name,
            "city_name": city_name,
            "basis": basis,
            "price": price,
            "currency": currency,
            "price_type": price_type,
        }
        return template.render(context)
