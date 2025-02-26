import os
import csv
import requests
from urllib.parse import urlparse

def download_pdfs_from_csv(csv_file, folder='debenture_pdf_folder'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pdf_url = row.get('pdf_url')
            if pdf_url and pdf_url.lower().endswith('.pdf'):
                try:
                    response = requests.get(pdf_url)
                    response.raise_for_status()
                except Exception as e:
                    print(f"PDF 다운로드 실패: {pdf_url}, 에러: {e}")
                    continue

                filename = os.path.basename(urlparse(pdf_url).path)
                filepath = os.path.join(folder, filename)
                with open(filepath, 'wb') as f_out:
                    f_out.write(response.content)
                print(f"다운로드 완료: {filepath}")

if __name__ == '__main__':
    csv_file_path = "C:/Users/USER/Desktop/bootcamp/BOK-TEAM-2/yedam/myproject/debenture_lists_raw.csv"
    download_pdfs_from_csv(csv_file_path)
