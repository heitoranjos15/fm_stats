import csv
from glob import glob
from os import path
from bs4 import BeautifulSoup

# Read HTML from file
html_files = glob(path.join(path.dirname(__file__), '*.html'))
html_files_data = []
for html_files in html_files:
    file_name = path.basename(html_files).replace('.html', '.csv')
    with open(html_files, encoding='utf-8') as f:
        print("Processing file:", file_name)
        soup = BeautifulSoup(f, 'html.parser')

        table = soup.find('table')

        headers = [th.get_text(strip=True) for th in table.find_all('th')]

        rows = []
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            print("TDs:", tds)
            if tds:
                row = list(td.get_text(strip=True) for td in tds)
                rows.append(row)
        html_files_data.append({"name": file_name, "headers": headers, "rows": rows})

for data in html_files_data:
    with open(data["name"], 'w', newline='', encoding='utf-8') as f:
        print(data)
        writer = csv.writer(f)
        writer.writerow(data["headers"])
        writer.writerows(data["rows"])
