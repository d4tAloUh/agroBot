from django.contrib import admin
from django.utils.safestring import mark_safe

from sales.models import CompanyAccount, Product, SubRegion, Region, City, SalesPlacement
from dtb.settings import TELEGRAM_BOT_USERNAME


@admin.register(CompanyAccount)
class CompanyAccountAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'tov', 'name', 'phone',
        'account_link_url', 'is_registered'
    ]
    search_fields = ('name', 'tov', 'phone')

    def account_link_url(self, obj: CompanyAccount):
        return mark_safe(
            f"<a href='https://t.me/{TELEGRAM_BOT_USERNAME}?start={obj.invite_code}'>Лінк</a>"
        )

    account_link_url.short_description = 'Invite link'

    def is_registered(self, obj: CompanyAccount):
        return obj.is_registered

    is_registered.short_description = 'Is registered'
    is_registered.boolean = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name',
    ]
    search_fields = ('name',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name',
    ]
    search_fields = ('name',)


@admin.register(SubRegion)
class SubRegionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'region_name'
    ]
    search_fields = ('name',)

    def region_name(self, obj: SubRegion):
        return obj.region.name


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name',
        'region_name',
        'subregion_name'
    ]
    search_fields = ('name',)

    def region_name(self, obj: City):
        return obj.region.name

    def subregion_name(self, obj: City):
        return obj.subregion.name


@admin.register(SalesPlacement)
class SalesPlacementAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company_tov',
        'product_name',
    ]
    search_fields = ('company__tov',
                     'company__name',
                     'basis',
                     'product__name', 'product__id')

    def company_tov(self, obj: SalesPlacement):
        return obj.company.tov

    company_tov.admin_order_field = 'company'
    company_tov.short_description = 'ТОВ'

    def product_name(self, obj: SalesPlacement):
        return obj.product.name

    product_name.admin_order_field = 'product'
    product_name.short_description = 'Товар'
