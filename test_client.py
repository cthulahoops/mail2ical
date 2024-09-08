import argparse
import smtplib

from email.mime.text import MIMEText


def send_test_email(host, port, email_file):
    with open(email_file, "r") as file:
        email_content = file.read()

    message = MIMEText(email_content)
    message["From"] = "sender@example.com"
    message["To"] = "receiver@example.com"
    message["Subject"] = "Test Email"

    server = smtplib.SMTP(host, port)
    server.send_message(message)
    server.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send a test email to the specified host and port."
    )
    parser.add_argument("--host", default="localhost", help="Host of the email server")
    parser.add_argument(
        "--port", type=int, default=8025, help="Port of the email server"
    )
    parser.add_argument("email_file", help="File containing the email content")

    args = parser.parse_args()
    send_test_email(args.host, args.port, args.email_file)
