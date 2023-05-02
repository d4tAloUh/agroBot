import os
import xml.etree.ElementTree as ET

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')
django.setup()
from django.db import transaction

from sales.models import Region, SubRegion, City
mytree = ET.parse('geo.xml')
myroot = mytree.getroot()

data = {}

region_strip_words = [" р-н", 'р.']
subregion_strip_words = []
city_strip_words = []
city_stop_words = ["Не визначений"]


def should_skip_city(city):
    for city_stop_word in city_stop_words:
        if city_stop_word in city:
            return True
    return False


def transform_name(geo_word: str, strip_words):
    for strip_word in strip_words:
        geo_word = geo_word.replace(strip_word, "")
    return geo_word


def process_file():
    for record in myroot:
        region = record.find('OBL_NAME')
        subregion = record.find('REGION_NAME')
        city = record.find('CITY_NAME')
        if region.text not in data:
            data[region.text] = {}
        if subregion.text not in data[region.text]:
            data[region.text][subregion.text] = set()
        if city.text is None:
            continue

        data[region.text][subregion.text].add(city.text)

    final_data = {}

    for region in data:
        if len(data[region]) == 0:
            continue
        region_clear_name = transform_name(region, region_strip_words)
        if region_clear_name not in final_data:
            final_data[region_clear_name] = {"cities": set(), "subregions": {}}
        for subregion in data[region]:
            subregion_clear_name = None
            if subregion is not None:
                subregion_clear_name = transform_name(subregion, subregion_strip_words)
                if subregion_clear_name not in final_data[region_clear_name]:
                    final_data[region_clear_name]["subregions"][subregion_clear_name] = set()

            for city in data[region][subregion]:
                if should_skip_city(city):
                    continue
                city_clear_name = transform_name(city, city_strip_words)
                if subregion is not None:
                    final_data[region_clear_name]["subregions"][subregion_clear_name].add(city_clear_name)
                else:
                    final_data[region_clear_name]["cities"].add(city_clear_name)
            if subregion_clear_name and len(final_data[region_clear_name]["subregions"][subregion_clear_name]) == 0:
                del final_data[region_clear_name]["subregions"][subregion_clear_name]
    # for region in final_data:
    #     print("region:", region)
    #     print("cities without subregion:", final_data[region]['cities'])
    #     for subregion in final_data[region]["subregions"]:
    #         print(subregion, " cities ----:", final_data[region]["subregions"][subregion])
    #     print("\n=================================================\n\n")
    return final_data


result = process_file()
with transaction.atomic():
    for region in result:
        region_obj = Region(
            name=region
        )
        region_obj.save()
        for city in result[region]["cities"]:
            city_obj = City(
                name=city,
                region_id=region_obj.pk
            )
            city_obj.save()
        for subregion in result[region]["subregions"]:
            subregion_obj = SubRegion(
                name=subregion,
                region_id=region_obj.pk
            )
            subregion_obj.save()
            for city in result[region]["subregions"][subregion]:
                city_obj = City(
                    name=city,
                    region_id=region_obj.pk,
                    subregion_id=subregion_obj.pk
                )
                city_obj.save()