import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


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


# Example usage with multiple attachments from a folder:
subject = "Test Email with Multiple Attachments"
body = "This is a test email with multiple attachments sent"
to_email = "michael-94@windowslive.com"
smtp_server = "smtp.office365.com"  # Outlook SMTP server
smtp_port = 587  # Port for TLS
sender_email = "michael-94@windowslive.com"
sender_password = "19941994"
attachment_folder = os.path.join(os.getcwd(), 'diavgeia_files', 'ledison', '20240221')

send_email(subject, body, to_email, smtp_server, smtp_port, sender_email, sender_password, attachment_folder)
