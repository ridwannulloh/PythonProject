import scrapy


class RwidSpider(scrapy.Spider):
    name = 'rwid'
    allowed_domains = ['127.0.0.1']
    start_urls = ['http://127.0.0.1:5000/']

    def parse(self, response):
        data = {
            'username': 'user',
            'password': 'user12345'
        }

        return scrapy.FormRequest(
            url='http://127.0.0.1:5000/login',
            formdata=data,
            callback=self.after_login
        )

    def after_login(self, response):

        ''''
        There are 2 tasks here:
        1. Scrape all items data in this page > directing to parsing detail
        2. Scrape all link next > back to after login
        '''

        # get detail product
        detail_products = response.css('.card .card-title a')
        for detail in detail_products:
            href = detail.attrib.get('href')
            yield response.follow(href, callback=self.parse_detail)

        paginations = response.css('.pagination a.page-link')
        for pagination in paginations:
            href = pagination.attrib.get('href')
            yield response.follow(href, callback=self.after_login)

    def parse_detail(self, response):
        image = response.css('.card-img-top').attrib.get('src')
        title = response.css('.card-title::text').get()
        stock = response.css('.card-stock::text').get()
        category = response.css('.card-category::text').get()
        description = response.css('.card-text::text').get()

        return {
            'image': image,
            'title': title,
            'stock': stock,
            'category': category,
            'description': description
        }
