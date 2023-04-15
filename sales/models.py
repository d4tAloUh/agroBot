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
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
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
        F1 = 'f1', 'Ф1'
        F2 = 'f2', 'Ф2'

    class VATChoice(models.TextChoices):
        WITH = 'with', 'З ПДВ'
        WITHOUT = 'without', 'БЕЗ ПДВ'

    class CurrencyChoice(models.TextChoices):
        UAH = 'uah', 'ГРН'
        USD = 'usd', 'USD'

    class StatusChoice(models.TextChoices):
        DRAFT = 'draft', 'DRAFT'
        POSTED = 'posted', 'POSTED'
        DELETED = 'deleted', 'DELETED'

    USER_DATA_SALE_FIELDS = [
        'product_id', 'region_id', 'subregion_id',
        'city_id', 'basis', 'weight', 'price',
        'currency', 'price_type'
    ]

    company = models.ForeignKey(CompanyAccount,
                                on_delete=models.CASCADE,
                                related_name="sales", **nb)
    product = models.ForeignKey(Product,
                                on_delete=models.PROTECT,
                                related_name="sales", **nb)
    weight = models.IntegerField(**nb)
    basis = models.CharField(max_length=1024, **nb)
    price_type = models.CharField(choices=PriceTypeChoice.choices, max_length=2, **nb)
    vat = models.CharField(choices=VATChoice.choices, max_length=7, **nb)
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
    
    def get_context_for_sale(self):
        return {
            "sale": self
        }
    
    def generate_sale_text(self):
        template = get_template('sale.html')
        context = self.get_context_for_sale()
        return template.render(context)

    def generate_sale_preview_text(self):
        template = get_template('sale_preview.html')
        context = self.get_context_for_sale()
        return template.render(context)
    
    @staticmethod
    def create_unsaved_sale_from_user_data(chat_id, user_data):
        company_account = CompanyAccount.objects.filter(
            tg_user_id=chat_id
        ).first()
        product_id = user_data.get("product_id")
        region_id = user_data.get("region_id")
        subregion_id = user_data.get("subregion_id")
        city_id = user_data.get("city_id")
        basis = user_data.get("basis")
        weight = user_data.get("weight")
        price = user_data.get("price")
        currency = user_data.get("currency")
        price_type = user_data.get("price_type")
        vat = user_data.get("vat")

        sale = SalesPlacement(
            company=company_account,
            product_id=product_id,
            weight=weight,
            basis=basis,
            price_type=price_type,
            currency=currency,
            price=price,
            region_id=region_id,
            subregion_id=subregion_id,
            city_id=city_id,
            vat=vat,
            status=SalesPlacement.StatusChoice.POSTED.value
        )
        return sale
