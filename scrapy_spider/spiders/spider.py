# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin

import scrapy
from scrapy_spider.items import ProductItem


def clean_str(string):
    return re.sub(r"\s+", ' ', string.replace("\n", '').replace("\t", '')).strip()


class Spider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['shop.countdown.co.nz']
    start_urls = ['https://shop.countdown.co.nz/']

    def parse(self, response):
        category_links = response.xpath("//div[@class='row-fluid mrow-fluid']")[0].xpath(".//a/@href").extract()
        for category_link in category_links[:]:
            yield scrapy.Request(urljoin(response.url, category_link), callback=self.parse_category)

        # category_link = "https://shop.countdown.co.nz/shop/browse/bakery?page=8"
        # yield scrapy.Request(urljoin(response.url, category_link), callback=self.parse_category)

    def parse_category(self, response):
        product_details = response.xpath("//div[@class='gridProductStamp-details']")
        for product_detail in product_details:
            url = product_detail.xpath("./a/@href").extract()[0]
            title = clean_str(''.join(product_detail.xpath(".//h3[@class='gridProductStamp-name']//text()").extract()))
            if re.search("\d", title.split()[-1]):
                weight = title.split()[-1]
            else:
                weight = ''

            price_string = clean_str(''.join(product_detail.xpath(
                "./div[@class='gridProductStamp-priceContainer']//*[contains(@class, 'gridProductStamp-price')]//text()").extract()))

            try:
                price = re.search('\d+\.?\d*', price_string.split()[0]).group(0)
            except IndexError:
                price = ''
            try:
                unit = price_string.split()[1]
            except IndexError:
                unit = ''

            item = ProductItem()

            item['url'] = urljoin(response.url, url)
            item['title'] = title
            item['size_weight'] = weight
            item['price'] = price
            item['unit'] = unit

            yield item

        next_page = response.xpath("//li[contains(@class, 'next')]/a/@href").extract()
        if len(next_page):
            yield scrapy.Request(urljoin(response.url, next_page[0]), callback=self.parse_category)

