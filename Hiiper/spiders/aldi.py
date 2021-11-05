import scrapy


class AldiSpider(scrapy.Spider):
    name = 'aldi'
    allowed_domains = [ 'aldi.nl' ]
    start_urls = ['https://www.aldi.nl/producten.html']

    def parse(self, response):
        category_level_1 = response.css('div.tiles-grid div')
        for n in category_level_1:
            yield {
            'name' : n.css('h4.mod-content-tile__title::text').get(),
            'link' : n.css('div.mod-content-tile__meta  a::attr(href)').get()
            }
        next_page = response.css('div.mod-content-tile__meta  a::attr(href)').get()
        if next_page is not None :
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)
        pass
