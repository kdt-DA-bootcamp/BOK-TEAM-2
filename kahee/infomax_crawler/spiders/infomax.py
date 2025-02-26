# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


import scrapy
from datetime import datetime


class InfomaxSpider(scrapy.Spider):
    name = 'infomax_spider'
    allowed_domains = ["news.einfomax.co.kr"]

    def start_requests(self):
        # 페이지 수 조정: 'nextpage' 설정하면 자꾸 안 넘어가서 그냥 range 설정했습니다다
        for page in range(107, 9655):
            url = f"https://news.einfomax.co.kr/news/articleList.html?view_type=sm&sc_word=금리&page={page}"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # 기사 목록 크롤링
        articles = response.xpath('//*[@id="section-list"]/ul/li')
        for article in articles:
            title = article.xpath('.//h4/a/text()').get(default='').strip()
            link = response.urljoin(article.xpath('.//h4/a/@href').get(default=''))
            date_text = article.xpath('.//span/em[last()]/text()').get(default='').strip()
            category = article.xpath('.//span/em[1]/text()').get(default='').strip() #카테고리 필터링 위해 카테고리도 추출(csv파일 출력은 X)

            # 카테고리 필터링
            if category in ["채권/외환", "정책/금융"]:
                yield scrapy.Request(
                    url=link,
                    callback=self.parse_article,
                    meta={
                        "title": title,
                        "date": date_text
                    }
                )

    def parse_article(self, response):
        # 기사 본문 추출(기사 목록에서 바로 가져올 수 없어 해당 링크로 이동, 따로 추출해야 함)
        title = response.meta["title"]
        date = response.meta["date"]
        content = " ".join(response.xpath('//*[@id="article-view-content-div"]//text()').getall()).strip()

        if content:
            yield {
                "title": title,
                "date": date,
                "content": content
            }
