import scrapy

class MiSpider(scrapy.Spider):
    name = "titles"
    # Recibimos la URL por argumentos
    def __init__(self, url=None, *args, **kwargs):
        super(MiSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        yield {
            "url": response.url,
            "title": response.css('title::text').get(),
            "status": "success"
        }
