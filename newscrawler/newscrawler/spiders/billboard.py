import scrapy
from scrapy import Request
from .. import items
class BillboardSpider(scrapy.Spider):
    name = "billboard"
    allowed_domains = ["www.billboard.com/charts/billboard-200"]
    start_urls = ['https://www.billboard.com/charts/billboard-200']

    def parse(self, response):
        #client = MongoClient()
        #db_music = client.series
        #collection_billboard = db_music['billboard']
        for i in range(0,200):
            album = response.css("span.chart-element__information")[i].css("span.chart-element__information__song.text--truncate.color--primary::text").extract_first()
            artist = response.css("span.chart-element__information")[i].css("span.chart-element__information__artist.text--truncate.color--secondary::text").extract_first()
            rank = response.css("span.chart-element__rank.flex--column.flex--xy-center.flex--no-shrink")[i].css("span.chart-element__rank__number::text").extract_first()
        #all_links = {
         #   name:response.urljoin(url) for name, url in zip(
          #  response.css("#nav-markup .Nav__item")[3].css("a::text").extract(),
           # response.css("#nav-markup .Nav__item")[3].css("a::attr(href)").extract())
        #}
            #collection_billboard.insert_one({"album" :album,"artist":artist, "rank":rank})
            #yield {"album":album,"artist":artist,"rank":rank}
            yield items.ArticleItem(
              album=album,
              artist=artist,
              rank=rank
            )
            #print("la collection : ")
            #print(collection_billboard.find_one())
        #print("collection KIRK: " + str(collection_billboard.find_one({"album":"KIRK"})))
        #print("collection gospel: " + str(collection_billboard.find_one({"album":"Ghetto Gospel"})))
	#all_links = {
            #name:response.urljoin(url) for name, url in zip(
            #response.css("#nav-markup .Nav__item")[3].css("a::text").extract(),
            #response.css("#nav-markup .Nav__item")[3].css("a::attr(href)").extract())
        #}
        #for link in all_links.values():
         #   yield Request(link, callback=self.parse_category)

   # def parse_category(self, response):
        #for article in response.css(".river")[0].css(".teaser"):
         #   title = self.clean_spaces(article.css("h3 ::text").extract_first())
          #  image = article.css("img::attr(data-src)").extract_first()
           # description = article.css("p::text").extract_first()

           # yield ArticleItem(
            #    title=title,
             #   image=image,
              #  description=description
            #)

    #def clean_spaces(self, string):
    #    if string is not None:
    #        return " ".join(string.split())
