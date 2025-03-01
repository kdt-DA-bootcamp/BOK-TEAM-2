import os
import csv
import fitz
from urllib.parse import urlparse, unquote

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    
    text_pages = []
    for page in doc:
        text_pages.append(page.get_text())
    doc.close()

    return "\n".join(text_pages)

def update_csv_with_extracted_text(input_csv, output_csv, pdf_folder):
    """
    1) input_csv를 읽어서 각 행의 'pdf_url' 열에서 PDF 파일명을 파싱
    2) pdf_folder에서 해당 PDF를 찾아 텍스트 추출
    3) 추출 텍스트를 row['pdf_url']에 덮어씀
    4) 수정된 데이터를 output_csv로 저장
    """

    # 원본 csv 읽기
    with open(input_csv, 'r', encoding='utf-8', newline='') as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames

        # 결과 csv 쓰기
        with open(output_csv, 'w', encoding='utf-8', newline='') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                    pdf_url = row.get('pdf_url', '').strip()
                    
                    if pdf_url:
                        parsed = urlparse(pdf_url)
                        pdf_filename = os.path.basename(parsed.path)
                        pdf_filename = unquote(pdf_filename)

                        pdf_path = os.path.join(pdf_folder, pdf_filename)

                        if os.path.isfile(pdf_path):
                            
                            try:
                                extracted_text = extract_text_from_pdf(pdf_path)
                                extracted_text = " ".join(extracted_text.split())
                                row['pdf_url'] = extracted_text
                            
                            except Exception as e:
                                print(f"PDF 텍스트 추출 실패: {pdf_path}\n에러: {e}")

                        else:
                            print(f"PDF 파일 없음: {pdf_path}")

                    writer.writerow(row)

    print(f"CSV 갱신 완료 -> {output_csv}")


if __name__ == "__main__":
    # (A) pdf_url에서 파일명 파싱
    input_csv  = r"C:/Users/USER/Desktop/bootcamp/BOK-TEAM-2/yedam/myproject/debenture_lists_raw.csv"
    output_csv = r"C:/Users/USER/Desktop/bootcamp/BOK-TEAM-2/yedam/myproject/debenture_results.csv"
    pdf_folder = r"C:/Users/USER/Desktop/bootcamp/BOK-TEAM-2/yedam/myproject/debenture_pdf_folder"
    
    update_csv_with_extracted_text(input_csv, output_csv, pdf_folder)