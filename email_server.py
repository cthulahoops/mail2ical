import logging
import asyncio
from typing import Any, Optional
import aiosmtpd.controller
from mail2ical.parser import generate_ical_from_email
import argparse
import yaml
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_calendar_config(config: dict, recipient: str) -> Optional[dict]:
    """
    Find the appropriate calendar configuration based on the recipient's email address.
    """
    for calendar in config["calendars"]:
        if calendar["email_address"] == recipient:
            return calendar
    return None


def save_ical(content: str, file_base: str, filename: str) -> str:
    """
    Save the iCal content to a file and return the file path.
    """
    file_path = os.path.join(file_base, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


class ICalEmailHandler:
    def __init__(self, config):
        self.config = config

    async def handle_DATA(self, server: Any, session: Any, envelope: Any) -> str:
        sender = envelope.mail_from
        if sender not in self.config["email"]["allowed_senders"]:
            logger.warning(f"Rejected email from unauthorized sender: {sender}")
            return "550 Sender not authorized"

        # Check if we have a valid recipient
        if not envelope.rcpt_tos:
            logger.warning("No recipients in the email")
            return "550 No recipients specified"

        recipient = envelope.rcpt_tos[0]  # We'll use the first recipient
        calendar_config = find_calendar_config(self.config, recipient)
        if not calendar_config:
            logger.warning(
                f"No calendar configuration found for recipient: {recipient}"
            )
            return "550 Invalid recipient"

        try:
            message = envelope.content
            email_content = message.decode("utf-8")
            logger.info(f"Received e-mail for calendar: {calendar_config['name']}")
            ical_content = generate_ical_from_email(
                email_content, self.config["ai_parser"]
            )

            # Save the iCal content to a file
            file_path = save_ical(
                ical_content,
                self.config["ical"]["file_base"],
                f"{calendar_config['uuid']}.ics",
            )

            logger.info(f"iCal file saved to {file_path}")
            return "250 Message accepted for delivery"
        except Exception as e:
            logger.error(f"Error processing email: {str(e)}")
            return "550 Error processing message"


async def start_server(config: dict) -> None:
    controller = aiosmtpd.controller.Controller(
        ICalEmailHandler(config),
        hostname=config["smtp"]["host"],
        port=config["smtp"]["port"],
    )
    server = controller.start()
    logger.info(
        f"Server listening on {config['smtp']['host']}:{config['smtp']['port']}"
    )
    logger.info("Press Ctrl+C to stop the server")

    try:
        await asyncio.Future()  # Run forever
    except asyncio.CancelledError:
        logger.info("Server shutdown initiated")
    finally:
        server.stop()
        logger.info("Server stopped")


def load_config(config_path: str) -> dict:
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start an email server for generating iCal events from emails."
    )
    parser.add_argument(
        "--config", default="config.yaml", help="Path to configuration file"
    )

    args = parser.parse_args()

    if not os.path.exists(args.config):
        logger.error(f"Config file not found: {args.config}")
        exit(1)

    config = load_config(args.config)

    try:
        asyncio.run(start_server(config))
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
