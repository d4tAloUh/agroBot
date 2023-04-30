import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')
django.setup()

from sales.models import Region, SubRegion

region_strip_words = [" обл.", 'р.']
subregion_strip_words = [" р-н", 'р.']

regions = Region.objects.all()
subregions = SubRegion.objects.all()

def transform_text(text, strip_words):
    for strip_word in strip_words:
        text = text.replace(strip_word, "")
    return text

per_page = 100
all_pages = regions.count()
for page in range(all_pages):
    # for region in regions[page*per_page:(page+1)*per_page]:
    #     print("Name: ", region.name)
    #     region.name = transform_text(region.name, region_strip_words)
    #     print("New Name: ", region.name, "\n\n")
    #
    #     region.save()
    for subregion in subregions[page*per_page:(page+1)*per_page]:
        print("Name: ", subregion.name)
        subregion.name = transform_text(subregion.name, subregion_strip_words)
        print("New Name: ", subregion.name, "\n\n")

        subregion.save()