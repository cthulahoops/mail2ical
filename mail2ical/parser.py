import os
from anthropic import Anthropic

def generate_ical_from_email(email_content):
    anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""Extract event details from this email and generate a valid iCal (.ics) file content:

{email_content}

Provide only the iCal file content, nothing else. Ensure it's a complete, valid iCal file."""
            }
        ]
    )

    return response.content[0].text
