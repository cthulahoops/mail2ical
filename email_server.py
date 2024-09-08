import signal
import logging
import aiosmtpd.controller
from mail2ical.parser import generate_ical_from_email
import argparse

logging.basicConfig(level=logging.INFO)


class ICalEmailHandler:
    async def handle_DATA(self, server, session, envelope):
        message = envelope.content
        email_content = message.decode("utf-8")

        print("Received e-mail - generating ical:")
        ical_content = generate_ical_from_email(email_content)

        print(ical_content)
        return "250 Message accepted for delivery"


def start_server(host, port):
    controller = aiosmtpd.controller.Controller(
        ICalEmailHandler(), hostname=host, port=port
    )
    server = controller.start()
    logging.info(f"Server listening on {host}:{port}")
    logging.info("Waiting for SIGINT or SIGQUIT")
    sig = signal.sigwait([signal.SIGINT, signal.SIGQUIT])
    logging.warn(f"{sig} caught, shutting down")
    server.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start an email server for generating iCal events from emails."
    )
    parser.add_argument("--host", default="localhost", help="Host to listen on")
    parser.add_argument("--port", type=int, default=8025, help="Port to listen on")

    args = parser.parse_args()
    start_server(args.host, args.port)
