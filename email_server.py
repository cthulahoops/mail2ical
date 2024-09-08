import aiosmtpd.controller
from mail2ical.parser import generate_ical_from_email
import argparse
import yaml
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ICalEmailHandler:
    def __init__(self, config):
        self.config = config

    async def handle_DATA(self, server: Any, session: Any, envelope: Any) -> str:
        sender = envelope.mail_from
        if sender not in self.config['email']['allowed_senders']:
            logger.warning(f"Rejected email from unauthorized sender: {sender}")
            return "550 Sender not authorized"

        try:
            message = envelope.content
            email_content = message.decode("utf-8")
            logger.info("Received e-mail - generating iCal")
            ical_content = generate_ical_from_email(email_content, self.config['ai_parser'])

            # Here you would save the ical_content to a file
            # using the config['ical']['file_storage_path']
            # and generate a URL using config['ical']['url_base']

            logger.info("iCal generated successfully")
            return "250 Message accepted for delivery"
        except Exception as e:
            logger.error(f"Error processing email: {str(e)}")
            return "550 Error processing message"

async def start_server(config: dict) -> None:
    controller = aiosmtpd.controller.Controller(
        ICalEmailHandler(config),
        hostname=config['smtp']['host'],
        port=config['smtp']['port']
    )
    server = controller.start()
    logger.info(f"Server listening on {config['smtp']['host']}:{config['smtp']['port']}")
    logger.info("Press Ctrl+C to stop the server")

    try:
        await asyncio.Future()  # Run forever
    except asyncio.CancelledError:
        logger.info("Server shutdown initiated")
    finally:
        server.stop()
        logger.info("Server stopped")

def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start an email server for generating iCal events from emails."
    )
    parser.add_argument("--config", default="config.yaml", help="Path to configuration file")

    args = parser.parse_args()

    if not os.path.exists(args.config):
        logger.error(f"Config file not found: {args.config}")
        exit(1)

    config = load_config(args.config)

    try:
        asyncio.run(start_server(config))
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
pip install PyYAML
