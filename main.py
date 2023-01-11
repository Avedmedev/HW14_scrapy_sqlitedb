import time

import scrapy
from scrapy.crawler import CrawlerProcess
from pipeline import SpiderPipeLine


class QuoteItem(scrapy.Item):
    author = scrapy.Field()
    quote = scrapy.Field()
    tags = scrapy.Field()


class AuthorItem(scrapy.Item):
    fullname = scrapy.Field()
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    bio = scrapy.Field()


class Spider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        "ITEM_PIPELINES": {
            SpiderPipeLine: 300,
        },
    }

    def parse(self, response):

        for quote in response.xpath("/html//div[@class='quote']"):
            yield response.follow(url=self.start_urls[0] + quote.xpath('span/a/@href').get(),
                                  callback=self.parse_author)

        for quote in response.xpath("/html//div[@class='quote']"):
            author = quote.xpath("span/small/text()").get()
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            quote = quote.xpath("span[@class='text']/text()").get().strip("“”").replace('\n', "")
            yield QuoteItem(author=author, quote=quote, tags=tags)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    @staticmethod
    def parse_author(response):
        content = response.xpath("/html//div[@class='author-details']")

        fullname = content.xpath("h3/text()").get().strip()
        born_date = content.xpath("p/span[@class='author-born-date']/text()").get().strip()
        born_location = content.xpath("p/span[@class='author-born-location']/text()").get().strip()
        bio = content.xpath("div[@class='author-description']/text()").get().strip()

        yield AuthorItem(fullname=fullname, born_date=born_date, born_location=born_location, bio=bio)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Spider)
    process.start()
