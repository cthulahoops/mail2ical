import os
from anthropic import Anthropic

# Setup Anthropic client
anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Read email file
with open('sample_email.txt', 'r') as email_file:
    email_content = email_file.read()

# Parse with Claude and generate iCal
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

# Save iCal file
with open('output.ics', 'w') as f:
    f.write(response.content[0].text)

print("iCal file generated: output.ics")
