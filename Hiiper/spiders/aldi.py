import scrapy


class AldiSpider(scrapy.Spider):
    name = 'aldi'
    allowed_domains = [ 'aldi.nl' ]
    start_urls = ['https://www.aldi.nl/producten.html']

    def __init__(self, *a, **kw):
        super(AldiSpider, self).__init__(*a, **kw)
        self.categories = []
    
    def parse(self, response):
        category_level_1 = response.css('div.mod-content-tile__content div')
        for n in category_level_1:
            yield {
            'name' : n.css('h4::text').get(),
            'link' : n.css('a::attr(href)').getall()
            }
        for category_url in response.css('div.mod-content-tile__content a::attr(href)').getall():
            yield response.follow('https://www.aldi.nl' + category_url, callback=self.parse_page)

        pass
    
    def parse_page(self,response):
        category_level_2 = response.css('div.mod-content-tile__content div')
        for n in category_level_2:
            yield {
            'name' : n.css('h4::text').get(),
            'link' : n.css('a::attr(href)').get()
            }
        for subcategory_url in response.css('div.mod-content-tile__content a::attr(href)').getall():
            yield response.follow('https://www.aldi.nl' + subcategory_url, callback=self.parse_product)

        pass

    def parse_product(self,response):
        product = response.css('div.tiles-grid')
        for p in product:
            yield {
                'shop' : 'aldi.nl',
                'product_name' : p.css('span.mod-article-tile__title::text').get().strip(),
                'product_id' : p.css('.mod-article-tile__action::attr(data-attr-prodid)').get(),
                'category_level_1' : '',
                'category_level_2' : '',
                'url' : p.css('a::attr(href)').get(),
                'description' : p.css('div.rte p::text').getall(),
                'images' : '',
                'quantity' :'' ,
                'amount' : p.css('span.price__wrapper::text').get().strip(),
                'date' : '',
                'time' : '',
                'price' : p.css('span.price__unit::text').get().strip(),
            }
        pass
