from ast import parse
import scrapy

class PostsSpider(scrapy.Spider):

    name= "posts"
    start_urls = [
        "https://www.cimri.com/tencere-tava-setleri"
    ]

    def parse(self, response):
        for products in response.css("div.z7ntrt-0.cLlfW.s1a29zcm-11.ggOMjb"):
            yield {
            "name": products.css("a.link-detail::attr(title)").get(),
            "link": products.css("a.link-detail").attrib["href"],
            "source": products.css("div.tag::text").get()
       }
        next_page = response.xpath(
        '//a[contains(@class,"ctiKSh")]/following-sibling::a/@href'
        ).get()
        
        if next_page is not None:
            next_page_link=response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback= self.parse)

    