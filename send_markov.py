#!/usr/bin/env python

# Written by Gem Newman. This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.


from markov import Markov

from argparse import ArgumentParser
from email.mime.text import MIMEText
from smtplib import SMTP


DEFAULT_RECIPIENT = "trigger@ifttt.com"
DEFAULT_SUBJECT = "#bible"
DEFAULT_HOST = "smtp.gmail.com:587"
DEFAULT_FILE = "bible.txt"
DEFAULT_KEY_SIZE = 3
DEFAULT_CHAR_LIMIT = 140


def send_markov(user, password, recipient, subject, host, filename, key_size,
                char_limit):
    # Initialize Markov chain.
    m = Markov(filename, key_size)

    # Build message.
    verse = m.generate_text(char_limit=char_limit)
    message = MIMEText(verse)
    message["subject"] = subject
    message["to"] = recipient
    message = message.as_string()

    # Connect
    smtp = SMTP(host)
    smtp.starttls()
    smtp.login(user, password)

    # Send.
    smtp.sendmail(user, recipient, message)

    # Disconnect.
    smtp.close()


if __name__ == "__main__":
    parser = ArgumentParser(description="Generate a pseudorandom Bible verse "
                            "using a Markov chain and email it for IFTTT.")
    parser.add_argument("user", help="Send email from this account.")
    parser.add_argument("password", help="Password for email account.")
    parser.add_argument("-r", "--recipient", help="The recipient of the email."
                        " Defaults to {}.".format(DEFAULT_RECIPIENT),
                        default=DEFAULT_RECIPIENT)
    parser.add_argument("-s", "--subject", help="The subject of the email."
                        " Defaults to {}.".format(DEFAULT_SUBJECT),
                        default=DEFAULT_SUBJECT)
    parser.add_argument("-t", "--host", help="The SMTP host to use. Defaults "
                        "to {}.".format(DEFAULT_HOST), default=DEFAULT_HOST)
    parser.add_argument("-f", "--filename", help="The file containing the "
                        "corpus text from which to generate the Markov chain. "
                        "Defaults to {}.".format(DEFAULT_FILE),
                        default=DEFAULT_FILE)
    parser.add_argument("-k", "--keysize", help="The key size to use for "
                        "Markov chain generation. Defaults to "
                        "{}.".format(DEFAULT_KEY_SIZE), type=int,
                        default=DEFAULT_KEY_SIZE)
    parser.add_argument("-c", "--characters", help="The character limit to"
                        "impose on the generated text. Defaults to "
                        "{}.".format(DEFAULT_CHAR_LIMIT), type=int,
                        default=DEFAULT_CHAR_LIMIT)

    send_markov(parser.parse_args().user, parser.parse_args().password,
                parser.parse_args().recipient, parser.parse_args().subject,
                parser.parse_args().host, parser.parse_args().filename,
                parser.parse_args().keysize, parser.parse_args().characters)
