import scrapy


class AldiSpider(scrapy.Spider):
    name = 'aldi2'
    allowed_domains = [ 'aldi.nl' ]
    start_urls = ['https://www.aldi.nl/producten.html']

    def parse_categories(self, response):
        for category_url in response.css('div.mod-content-tile__content a::attr(href)').getall():
            yield response.follow('https://www.aldi.nl' + category_url, callback=self.parse_category)
        pass

    def parse_cateogry(self, response):
        category_level_1 = response.css('div.mod-content-tile__content div')
        for n in category_level_1:
            yield {
            'name' : n.css('h4::text').get(),
            'link' : n.css('a::attr(href)').getall()
            }
            
            
        pass 
    
    def parse_page(self,response):
        category_level_2 = response.css('div.mod-content-tile__content div')
        for n in category_level_2:
            yield {
            'name' : n.css('h4::text').get(),
            'link' : n.css('a::attr(href)').get()
            }
        pass