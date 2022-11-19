# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from ECS.main import get_arguments
args = get_arguments()


class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, product_data, spider):
        adapter = ItemAdapter(product_data)
        if adapter['product_href'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {product_data!r}")
        else:
            self.ids_seen.add(adapter['product_href'])
            return product_data


class IncludeKeywordPipeline:
    def process_item(self, product_data, spider):
        adapter = ItemAdapter(product_data)
        include_keywords = args.include
        if any(keyword in adapter['product_title'] for keyword in include_keywords):
            return product_data
        raise DropItem('Drop item')


class ExcludeKeywordPipeline:
    def process_item(self, product_data, spider):
        adapter = ItemAdapter(product_data)
        exclude_keywords = args.exclude
        if any(keyword in adapter['product_title'] for keyword in exclude_keywords):
            raise DropItem('Drop item')
        return product_data


class AuthorisedSellerPipeline:
    def process_item(self, product_data, spider):
        adapter = ItemAdapter(product_data)
        authorized_seller = args.auth
        if any(seller in adapter['product_seller'] for seller in authorized_seller):
            raise DropItem('Drop item')
        return product_data


class UnauthorisedSellerPipeline:
    def process_item(self, product_data, spider):
        adapter = ItemAdapter(product_data)
        unauthorized_seller = args.unth
        if any(seller in adapter['product_seller'] for seller in authorized_seller):
            return product_data
        raise DropItem('Drop item')

