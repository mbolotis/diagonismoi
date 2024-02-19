from bs4 import BeautifulSoup
import requests
import json
import os
import pickle
import branca
import lxml
from urllib.parse import quote
from datetime import date
import textract

'''
decoded_string = 'λαμπες'
encoded_string = quote(decoded_string)
start_date = date.today()
suffix = 'T00:00:00'
print(str(start_date)+suffix)
'''
'''
start_date = '2024-01-21T00:00:00'
end_date = '2024-02-19T23:59:59'
keyword = 'λαμπες'
#url = 'https://diavgeia.gov.gr/search?advanced&query=q:%22%CE%BB%CE%B1%CE%BC%CF%80%CE%B5%CF%82%22&page=0&fq=decisionType:%22%CE%A0%CE%95%CE%A1%CE%99%CE%9B%CE%97%CE%A8%CE%97%20%CE%94%CE%99%CE%91%CE%9A%CE%97%CE%A1%CE%A5%CE%9E%CE%97%CE%A3%22&fq=issueDate:%5BDT(2024-01-21T00:00:00)%20TO%20DT(2024-02-19T23:59:59)%5D'
#response = requests.get(url)
file_url = 'https://diavgeia.gov.gr/doc/ΨΟ854690ΒΠ-ΟΨ8'
response = requests.get(file_url)
print(response)

if response.status_code == 200:
    with open("test_1.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)
    print("File downloaded successfully.")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")

# html_text = requests.get(url).text
'''

json_url = 'https://diavgeia.gov.gr/luminapi/api/search/export?q=q:[%22%CE%BB%CE%B1%CE%BC%CF%80%CE%B5%CF%82%22]&fq=decisionType:%22%CE%A0%CE%95%CE%A1%CE%99%CE%9B%CE%97%CE%A8%CE%97%20%CE%94%CE%99%CE%91%CE%9A%CE%97%CE%A1%CE%A5%CE%9E%CE%97%CE%A3%22&fq=issueDate:[DT(2024-01-21T00:00:00)%20TO%20DT(2024-02-19T23:59:59)]&sort=recent&wt=json'

file_path = requests.get(json_url).text
response = requests.get(json_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Load the JSON content into a list of dictionaries
    data_list = [json.loads(line) for line in response.text.strip().split('\n')]

    # Extract multiple fields from each record in data_list
    field_values = [
        {
            'ada': result.get('ada', 'N/A'),
            'protocolNumber': result.get('protocolNumber', 'N/A'),
            'issueDate': result.get('issueDate', 'N/A'),
            'submissionTimestamp': result.get('submissionTimestamp', 'N/A'),
            'documentUrl': result.get('documentUrl', 'N/A'),
            'subject': result.get('subject', 'N/A'),
            'decisionTypeUid': result.get('decisionTypeUid', 'N/A'),
            'decisionTypeLabel': result.get('decisionTypeLabel', 'N/A'),
            'organizationUid': result.get('organizationUid', 'N/A'),
            'organizationLabel': result.get('organizationLabel', 'N/A'),
        }
        for record in data_list
        for result in record.get('decisionResultList', [])
    ]

else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
