from bs4 import BeautifulSoup
import requests
import json
import os
import pickle
import branca
import lxml
import urllib.parse
from datetime import date, timedelta
import textract
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def add_company(companies, name, keywords,email, cpv):
    max_id = max((company.get('id', 0) for company in companies), default=0)

    new_id = max_id + 1

    new_company = {
        "id": new_id,
        "name": name,
        "keywords": keywords,
        "email": email,
        "cpv": cpv
    }

    # Add the new company to the list
    companies.append(new_company)


def delete_company(companies, company_id):
    # Find the index of the company with the specified ID
    index_to_remove = None
    for i, company in enumerate(companies):
        if company.get('id') == company_id:
            index_to_remove = i
            break

    # Remove the company if found
    if index_to_remove is not None:
        del companies[index_to_remove]


def send_email(subject, body, to_email, smtp_server, smtp_port, sender_email, sender_password, attachment_folder):
    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, "plain"))

    # Attach all PDF files in the folder
    for filename in os.listdir(attachment_folder):
        if filename.endswith(".pdf"):
            attachment_path = os.path.join(attachment_folder, filename)
            with open(attachment_path, "rb") as attachment_file:
                attachment = MIMEApplication(attachment_file.read(), "pdf")
                attachment.add_header("Content-Disposition", f"attachment; filename={filename}")
                message.attach(attachment)

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Use TLS if required by the SMTP server
        server.starttls()

        # Log in to the email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, to_email, message.as_string())


list_keywords = ['"ΛΑΜΠ"', '"ΚΙΝΗΤΗΡ"', '"ΗΛΕΚΤΡΟΛ"', '"ΜΕΛΑΝΙ"']

companies = [
    {
        "id": 1,
        "name": "ledison",
        "keywords": [list_keywords[0]],
        "email": "gkakias94@gmail.com",
        "cpv": ('44', '46')
    },
    {
        "id": 2,
        "name": "example_kinitires",
        "keywords": [list_keywords[1]],
        "email": "gkakias94@gmail.com",
        "cpv": ('44', '46')
    }
]

with open('credentials.json') as f:
    creds = json.load(f)

for company in companies:
    prefix = 'https://diavgeia.gov.gr/luminapi/api/search/export?q=q:['
    decision = '&fq=decisionType:%22%CE%A0%CE%95%CE%A1%CE%99%CE%9B%CE%97%CE%A8%CE%97%20%CE%94%CE%99%CE%91%CE%9A%CE%97%CE%A1%CE%A5%CE%9E%CE%97%CE%A3%22'
    start_date = str(date.today()) + 'T00:00:00'
    end_date = str(date.today() - timedelta(days=3)) + 'T00:00:00'
    date_range = '&fq=issueDate:[DT(' + end_date + ')%20TO%20DT(' + start_date + ')]'
    suffix = '&sort=recent&wt=json'
    for keyword_temp in company['keywords']:
        keyword = str(keyword_temp + ']')
        final_url = str(prefix + keyword + decision + date_range + suffix)

        response = requests.get(final_url)

        if response.status_code == 200:
            data_list = [json.loads(line) for line in response.text.strip().split('\n')]

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

            folder_path = os.path.join(os.getcwd(), 'diavgeia_files', company['name'], str(date.today().strftime('%Y%m%d')))
            os.makedirs(folder_path, exist_ok=True)

            for entry in field_values:
                ada_value = entry.get('ada', 'N/A')
                filename = os.path.join(folder_path, f"{ada_value}.pdf")

                with open(filename, "wb") as pdf_file:
                    pdf_file.write(requests.get(entry['documentUrl']).content)

            print(f"File download completed successfully for company: {company['name']}")

            # Example usage with multiple attachments from a folder:
            subject = f"Προκυρήξεις διαγωνισμών για {date.today()}"
            body = "This is a test email with multiple attachments sent"
            to_email = company['email']
            smtp_server = "smtp.gmail.com"  # Outlook SMTP server-- smtp.gmail.com smtp.office365.com
            smtp_port = 587  # Port for TLS 465
            sender_email = creds['EMAIL_ADDRESS']
            sender_password = creds['EMAIL_PASSWORD']
            #sender_email = "michaelbolotis@gmail.com"
            #sender_password = "xbdp qwgf bxfw cczh"  # xbdp qwgf bxfw cczh
            attachment_folder = os.path.join(os.getcwd(), 'diavgeia_files', company['name'], str(date.today().strftime('%Y%m%d')))

            send_email(subject, body, to_email, smtp_server, smtp_port, sender_email, sender_password, attachment_folder)
        else:
            print(company['name'])
            print(f"Failed to fetch data. Status code: {response.status_code}")
