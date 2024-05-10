import docx
import csv
import re

def extract_text_and_hyperlinks_from_docx(docx_file):
    doc = docx.Document(docx_file)
    data = []
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        hyperlinks = re.findall(r'(?<=\()https?://[^\)]+', text)
        if text and hyperlinks:
            data.append((text, hyperlinks[0]))
    return data

def save_data_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)

input_docx = r'aws\Data_Creation.docx'
output_csv = r'aws\output2.csv'

data = extract_text_and_hyperlinks_from_docx(input_docx)
save_data_to_csv(data, output_csv)
