import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["chaconne.ru"]
    start_urls = [f"https://chaconne.ru/category/5941/?p={page}" for page in range(1, 28)]

    def parse(self, response):
        books = response.xpath('//div[@class="col-xs-6 col-sm-6 col-md-4 col-lg-3 grid"]')
        for book in books:
            yield {
                'name': book.xpath('.//a[@class="title text-center"]/text()').get(),
                'price': book.xpath('.//div[@class="price"]/strong/span/text()').get(),
                'autor': book.xpath('.//a[@class="author"]/text()').get(),
                'photo': book.css('a.img-container::attr(data-image-src)').get()
            }

