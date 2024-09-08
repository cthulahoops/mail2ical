import logging
import asyncio
import aiosmtpd.controller
from mail2ical.parser import generate_ical_from_email
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ICalEmailHandler:
    async def handle_DATA(self, server, session, envelope) -> str:
        try:
            message = envelope.content
            email_content = message.decode("utf-8")
            logger.info("Received e-mail - generating iCal")
            ical_content = generate_ical_from_email(email_content)
            logger.debug(f"Generated iCal content: {ical_content}")
            return "250 Message accepted for delivery"
        except Exception as e:
            logger.error(f"Error processing email: {str(e)}")
            return "550 Error processing message"


async def start_server(host: str, port: int) -> None:
    controller = aiosmtpd.controller.Controller(
        ICalEmailHandler(), hostname=host, port=port
    )
    server = controller.start()
    logger.info(f"Server listening on {host}:{port}")
    logger.info("Press Ctrl+C to stop the server")

    try:
        await asyncio.Future()  # Run forever
    except asyncio.CancelledError:
        logger.info("Server shutdown initiated")
    finally:
        server.stop()
        logger.info("Server stopped")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start an email server for generating iCal events from emails."
    )
    parser.add_argument("--host", default="localhost", help="Host to listen on")
    parser.add_argument("--port", type=int, default=8025, help="Port to listen on")

    args = parser.parse_args()

    try:
        asyncio.run(start_server(args.host, args.port))
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
