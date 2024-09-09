# Email to iCal Conversion Service

This is a proof of concept experiment. After building this I found an ical
link for the calendar I wanted to convert, so I've never deployed this. I
still think the idea is good, and I can imagine using this again. This was
built in about two hours using claude-3.5-sonnet (and other LLM tools) so
it wasn't a big use of time to prototype. (It makes this look much more
finished than it is!)

This service receives email newsletters, extracts event information, and
generates iCal files accessible via HTTP. It's designed for small-scale,
self-hosted use, prioritizing simplicity and ease of maintenance.

## Features

- SMTP server to receive emails
- AI-powered event extraction from email content
- iCal file generation for extracted events
- Configuration-based calendar management
- Simple security through secret email addresses

## Requirements

- Python 3.7+
- aiosmtpd
- PyYAML
- anthropic (Claude AI API)


## Installation

1. Clone the repository:
   ```
   git clone https://github.com/cthulahoops/mail2ical.git
   cd mail2ical
   ```

2. Install poetry if you haven't already:
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install the project dependencies using poetry:
   ```
   poetry install
   ```

4. Copy the example configuration file and edit it to your needs:
   ```
   cp config.example.yaml config.yaml
   nano config.yaml
   ```

Note: Full installation instructions for setting up on a server with a webserver are a work in progress. This guide covers the basic setup for local development and testing.

## Configuration

The `config.yaml` file contains all the necessary settings for the service:

- SMTP server settings
- Allowed email senders
- iCal file storage settings
- AI parser settings (Claude API)
- Calendar definitions (name, email address)

Each calendar is defined with a unique name and email address. The email address acts as a secret key for that calendar.

## Usage

1. Start the email server:
   ```
   python email_server.py --config config.yaml
   ```

2. To test the service, use the provided test client:
   ```
   python test_client.py --config config.yaml --calendar "Work Events"
   ```
   Replace "Work Events" with the name of the calendar you want to test.

3. Send emails containing event information to the email addresses defined in your config file. The service will process these emails and generate iCal files.

## Security

Security is maintained by keeping the email addresses for each calendar
confidential. Only emails sent to these addresses from allowed senders will be
processed.

## Limitations

- This service is designed for small-scale, personal use.
- It relies on the Claude AI API for event extraction, which may incur costs.
- There's no built-in encryption for SMTP (consider using a reverse proxy for TLS).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
