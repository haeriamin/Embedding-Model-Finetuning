# scrapy runspider ./src/scraper.py

import os
import scrapy
from scrapy.http import Request


class PDFScraper(scrapy.Spider):
    name = "pdf_scraper"

    allowed_domains = ["www.federalresrve.com"]
    start_urls = ["http://www.federalresrve.com/us/en/tax-services/publications/research-and-insights.html"]

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            yield Request(
                url=response.urljoin(href),
                callback=self.parse_article
            )

    def parse_article(self, response):
        for href in response.css('[href$=".pdf"]::attr(href)').extract():
            yield Request(
                url=response.urljoin(href),
                callback=self.save_pdf
            )

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        path = os.path.join('./data', path)
        with open(path, 'wb') as f:
            f.write(response.body)
