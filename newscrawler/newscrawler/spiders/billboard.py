import scrapy
from scrapy import Request
from .. import items
class BillboardSpider(scrapy.Spider):
    name = "billboard"
    allowed_domains = ["www.billboard.com/charts/billboard-200"]
    start_urls = ['https://www.billboard.com/charts/billboard-200']

    def parse(self, response):
        for i in range(0,200):
            album = response.css("span.chart-element__information")[i].css("span.chart-element__information__song.text--truncate.color--primary::text").extract_first()
            artist = response.css("span.chart-element__information")[i].css("span.chart-element__information__artist.text--truncate.color--secondary::text").extract_first()
            rank = response.css("span.chart-element__rank.flex--column.flex--xy-center.flex--no-shrink")[i].css("span.chart-element__rank__number::text").extract_first()
            peak = response.css(".chart-element__metas.display--flex.flex--y-center")[i].css(".chart-element__meta.text--center.color--secondary.text--peak::text").extract_first()
            duration = response.css(".chart-element__metas.display--flex.flex--y-center")[i].css(".chart-element__meta.text--center.color--secondary.text--week::text").extract_first()
            last_week = response.css(".chart-element__metas.display--flex.flex--y-center")[i].css(".chart-element__meta.text--center.color--secondary.text--last::text").extract_first()
            yield items.ArticleItem(
              album=album,
              artist=artist,
              rank=rank,
              peak=peak,
              duration=duration,
              last_week=last_week
            )

