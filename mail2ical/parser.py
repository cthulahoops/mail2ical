from anthropic import Anthropic


def generate_ical_from_email(email_content, ai_config):
    anthropic = Anthropic(api_key=ai_config["api_key"])

    response = anthropic.messages.create(
        model=ai_config["model"],
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""Extract event details from this email and generate a valid iCal (.ics) file content:\n\n{email_content}\n\nProvide only the iCal file content, nothing else. Ensure it's a complete, valid iCal file.""",
            }
        ],
    )

    return response.content[0].text
