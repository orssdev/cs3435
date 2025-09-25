# Oscar Silva-Santiago
# https://docs.scrapy.org/en/latest/intro/tutorial.html and https://www.w3schools.com/cssref/css_selectors.php
# Scraped 2 websites with different times in each website

import scrapy


class HW3(scrapy.Spider):
    name = "hw3"

    async def start(self):
        start_year = 2015
        end_year = 2025
        pages = 1
        urls = [f'https://www.plotexplained.com/movie?sort=latest-release&fromYear={start_year}&toYear={end_year}&page={x}' for x in range(1, pages + 1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.plot_explained_parse)
        urls = [f'https://www.physicalmediavault.com/collections/4k-steelbooks?page={x}' for x in range(1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.physical_media_valut_parse)
        

    def plot_explained_parse(self, response):
        urls = set([f'https://www.plotexplained.com{x}' for x in response.css('a[href^="/movie/"]::attr(href)').getall()])

        for url in urls:
            yield scrapy.Request(url=url, callback=self.movie_parse)
    
    def physical_media_valut_parse(self, response):
        urls = set([f'https://www.physicalmediavault.com{x}' for x in response.css('a[href^="/products/"]::attr(href)').getall()])

        for url in urls:
            yield scrapy.Request(url=url, callback=self.product_parse)
    
    def movie_parse(self, response):
        title = response.css('h1::text').get()
        info = response.css('div.flex.pt-4.flex-row.font-semibold.text-base.sm\\:text-lg.xl\\:text-xl.font-source-pro.gap-x-8.md\\:gap-x-14.gap-y-2.sm\\:gap-y-3.md\\:gap-y-4.flex-wrap p::text').getall()
        capitalize = response.css('span.capitalize::text').getall()
        desc = response.css('p.text-base.lg\\:text-lg.text-foreground::text').get()
        title_image = response.css('img.h-full.w-auto.lg\\:w-full.lg\\:h-auto.rounded-lg.shadow-lg.max-h-80.sm\\:max-h-96::attr(src)').get()
        year = 'No year listed'
        runtime = 'No runtime listed'
        language = 'No language listed'
        director = 'No director(s) listed'
        budget = 'No budget listed'
        for item in info:
            if item != ' ':
                data = item.split()
                item = data[0]
                if item == 'Year:':
                    year = data[1]
                elif item == 'Runtime:':
                    runtime = ' '.join(data[1:])
                elif item == 'Language:':
                    language = capitalize[0].title()
                elif item == 'Director:':
                    director = ' '.join(data[1:])
                elif item == 'Directors:':
                    director = (' '.join(data[1:])).split(',')
                elif item == 'Budget:':
                    budget = data[1]
        yield {
            'url': response.url,
            'title': title,
            'year': year,
            'runtime': runtime,
            'language' : language,
            'director' : director,
            'budget' : budget,
            'genre': capitalize[1:],
            'description': desc,
            'title_image': title_image
        }

    def product_parse(self, response):
        title = response.css('h1::text').get()
        country_released = response.css('p.product__text.inline-richtext strong::text').getall()
        price = response.css('span.price-item.price-item--regular::text').get()
        product_details = response.css('div.product__description.rte.quick-add-hidden li strong::text').getall()
        product_details_items = [x for x in response.css('div.product__description.rte.quick-add-hidden li::text').getall() if x != '\n']
        director = 'No director listed'
        starting = 'No stars listed'
        genre = 'No genre listed'
        format = 'No format listed'
        language = 'No language listed'
        runtime = 'No runtime listed'
        for i in range(len(product_details)):
            if product_details[i] == 'Director:':
                director = product_details_items[i]
            elif product_details[i] == 'Starring:':
                starting = product_details_items[i]
            elif product_details[i] == 'Genre:':
                genre = product_details_items[i]
            elif product_details[i] == 'Format:':
                format = product_details_items[i]
            elif product_details[i] == 'Language:':
                language = product_details_items[i]
            elif product_details[i] == 'Runtime:':
                runtime = product_details_items[i]
            
        yield {
            'url': response.url,
            'title': title,
            'country released': "No Country Listed" if len(country_released) < 2 else country_released[1],
            'price': ' '.join(price.split()),
            'director': director,
            'starting': starting,
            'genre': genre,
            'format': format,
            'language': language,
            'runtime': runtime 
        }