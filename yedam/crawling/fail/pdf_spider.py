import scrapy
import pdfplumber
import io
import csv
import os

class PdfSpider(scrapy.Spider):
    name = "pdf_spider"
    csv_fname = 'debenture_lists.csv'

    def start_requests(self):

        csv_file = os.path.join(os.path.dirname(__file__), self.csv_fname)

        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pdf_url = row.get('pdf_url')
                if not pdf_url:
                    continue

                yield scrapy.Request(
                    url=pdf_url,
                    callback=self.parse_pdf,
                    meta={'row': row}
                )


    def parse_pdf(self, response):
        row = response.meta['row']

        pdf_text = ""
        try:
            with pdfplumber.open(io.BytesIO(response.body)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pdf_text += page_text + "\n"
        except Exception as e:
            self.logger.error(f"PDF 파싱 오류: {e}")

        pdf_text = pdf_text.replace("\n", " ").replace("\r", " ")
        pdf_text = " ".join(pdf_text.split())

        row.pop('pdf_url', None)
        row['contents'] = pdf_text.strip() if pdf_text else "No text extracted"

        yield row