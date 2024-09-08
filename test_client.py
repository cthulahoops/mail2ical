import smtplib
import argparse
import yaml

from email.message import EmailMessage


def load_config(config_path: str) -> dict:
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)


def send_test_email(config: dict, calendar_name: str, content: str):
    # Find the calendar configuration
    calendar_config = next(
        (cal for cal in config["calendars"] if cal["name"] == calendar_name), None
    )
    if not calendar_config:
        print(f"No calendar found with name: {calendar_name}")
        return

    # Create the email
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = f"Test Event for {calendar_name}"
    msg["From"] = config["email"]["allowed_senders"][0]  # Use the first allowed sender
    msg["To"] = calendar_config["email_address"]

    # Send the email
    try:
        with smtplib.SMTP(config["smtp"]["host"], config["smtp"]["port"]) as server:
            server.send_message(msg)
        print(
            f"Test email sent to {calendar_config['email_address']} for calendar: {calendar_name}"
        )
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send a test email to the iCal conversion service."
    )
    parser.add_argument(
        "--config", default="config.yaml", help="Path to configuration file"
    )
    parser.add_argument(
        "--calendar", required=True, help="Name of the calendar to send the test to"
    )
    args = parser.parse_args()

    config = load_config(args.config)

    test_content = """
    Hello,

    Here's a test event:

    Event: Team Meeting
    Date: 2023-07-15
    Time: 14:00-15:30
    Location: Conference Room A
    Description: Weekly team sync-up to discuss project progress.

    Best regards,
    Test Client
    """

    send_test_email(config, args.calendar, test_content)
