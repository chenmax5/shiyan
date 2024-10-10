import scrapy
from src_sjtu.items import SrcSjtuItem


def parse_author(response):
    item = response.meta['item']

    author_rank_text = response.xpath('/html/body/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[1]/text()').get(default='').strip()
    if author_rank_text:
        item['authorRank'] = ''.join(filter(str.isdigit, author_rank_text))  # 提取数字
    else:
        item['authorRank'] = '0'
    item['grade'] = response.xpath('/html/body/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/span/text()').get(default='').strip()
    tnum_text = response.xpath('/html/body/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[3]/text()').get(default='').strip()
    if tnum_text:
        item['tnum'] = ''.join(filter(str.isdigit, tnum_text))
    else:
        item['tnum'] = '0'
    bnum_text = response.xpath('/html/body/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[4]/text()').get(default='').strip()
    if bnum_text:
        item['bnum'] = ''.join(filter(str.isdigit, bnum_text))
    else:
        item['bnum'] = '0'
    item['team'] = response.xpath('/html/body/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[5]/a/text()').get(default='').strip()

    yield item


class SjtuSpider(scrapy.Spider):
    name = "sjtu"
    allowed_domains = ["src.sjtu.edu.cn"]
    start_urls = ["https://src.sjtu.edu.cn/list"]


    def parse(self, response):
        for content in response.xpath('//table//tr[@class="row"]'):
            item = SrcSjtuItem()
            item['date'] = content.xpath('./td[1]/text()').get(default='').strip()
            item['title'] = content.xpath('./td[2]/a/text()').get(default='').strip()
            item['rank'] = content.xpath('./td[3]/span/text()').get(default='').strip()
            item['author'] = content.xpath('./td[4]/a/text()').get(default='').strip()

            author_link = content.xpath('./td[4]/a/@href').get()
            if author_link:
                author_url = response.urljoin(author_link)
                request = scrapy.Request(url=author_url, callback=parse_author)
                request.meta['item'] = item
                yield request

            next_page = response.xpath('/html/body/div/div/div[1]/div/div/ul/li/a[contains(text(), "»")]/@href').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(next_page_url, callback=self.parse)

