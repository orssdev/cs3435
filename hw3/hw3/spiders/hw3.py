import scrapy


class HW3(scrapy.Spider):
    name = "hw3"

    async def start(self):
        start_year = 2015
        end_year = 2025
        pages = 5
        urls = [f'https://www.plotexplained.com/movie?sort=latest-release&fromYear={start_year}&toYear={end_year}&page={x}' for x in range(1, pages + 1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

        

    def parse(self, response):
        urls = [f'https://www.plotexplained.com{x}' for x in response.css('a[href^="/movie/"]::attr(href)').getall()]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.movie_parse)
    
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
        echo_score = 'No echo score listed'
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
    
