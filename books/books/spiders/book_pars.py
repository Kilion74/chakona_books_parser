import scrapy


class ExampleSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["chaconne.ru"]
    start_urls = [f"https://chaconne.ru/category/5941/?p={page}" for page in range(1, 28)]

    def parse(self, response):
        books = response.xpath('//div[@class="col-xs-6 col-sm-6 col-md-4 col-lg-3 grid"]')
        for book in books:
            # Извлечение ссылки на карточку товара
            product_url = book.xpath('.//div[@class="product "]/a/@href').get()
            if product_url:
                # Отправка запроса на карточку товара
                yield response.follow(product_url, self.parse_product)

    def parse_product(self, response):
        # Сбор полной информации о товаре
        data = {
            'name': response.xpath('//h1/text()').get(),
            'price': response.xpath('//div[@class="price"]/strong/span/text()').get(),
            # 'author': response.xpath('//a[@class="author"]/text()').get(),
            'photo': response.xpath('.//a[@class="img-container"]/img/@src').get(),
            "params": []
        }
        rows = response.xpath('//div[@class="product_text"]/table/tbody/tr')

        for row in rows:
            key = row.xpath('./td[1]/text()').get()
            value = row.xpath('./td[2]//text()').getall()
            value = " ".join(value).strip()
            all_params = key + ': ' + value
            # if key:
            #     data[key] = value
            if all_params:
                data["params"].append(all_params.strip())
        yield data
