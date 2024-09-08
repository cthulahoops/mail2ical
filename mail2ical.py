import argparse
import sys
from mail2ical_converter import generate_ical_from_email

def main(input_file, output_file=None):
    with open(input_file, 'r') as email_file:
        email_content = email_file.read()

    ical_content = generate_ical_from_email(email_content)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(ical_content)
        print(f"iCal file generated: {output_file}")
    else:
        sys.stdout.write(ical_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert email content to iCal file')
    parser.add_argument('input_file', help='Input email file')
    parser.add_argument('-o', '--output', help='Output iCal file')
    args = parser.parse_args()

    main(args.input_file, args.output)
