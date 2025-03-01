import scrapy
import re
from datetime import datetime

class DebentureSpider(scrapy.Spider):
    name = "debenture"
    allowed_domains = ["finance.naver.com", "stock.pstatic.net"]

    start_urls = [
        'https://finance.naver.com/research/economy_list.naver?keyword=&brokerCode=&searchType=writeDate&writeFromDate=2014-01-01&writeToDate=2024-11-30&x=29&y=33&page=1'
    ]

    def parse(self, response):
        rows = response.xpath('//table[@class="type_1"]/tr')
        
        date_pattern = re.compile(r'^\s*\d{2}\.\d{2}\.\d{2}\s*$')
        
        for row in rows:
            # 제목
            title = row.xpath('.//td[1]/a/text()').get()
            if not title:
                continue
            
            # PDF 링크
            pdf_url = row.xpath('.//td[@class="file"]/a/@href').get()
            
            # 날짜 (예: '24.11.29')
            date_str = row.xpath('.//td[4]/text()').get()
            if not date_str or not date_pattern.match(date_str.strip()):
                continue
            
            # 날짜 형식 변환
            try:
                date_obj = datetime.strptime(date_str.strip(), '%y.%m.%d')
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except Exception:
                formatted_date = date_str.strip()
            
            yield {
                'title': title.strip(),
                'pdf_url': pdf_url,
                'date': formatted_date,
            }
        
        # 페이지네이션 처리
        current_page = int(response.url.split("page=")[-1])
        if current_page < 217:
            next_page = current_page + 1
            next_url = response.url.replace(f"page={current_page}", f"page={next_page}")
            yield scrapy.Request(next_url, callback=self.parse)