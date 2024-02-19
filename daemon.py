from bs4 import BeautifulSoup
import requests
import json
import os
import pickle
import branca
import lxml


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


