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
DEFAULT_KEY_SIZE = 2
DEFAULT_LIMIT = 140


def send_markov(user, password, recipient, subject, host, filename, key_size,
                limit, limit_words):
    # Initialize Markov chain.
    m = Markov(filename, key_size)

    # Build message.
    verse = m.generate_text(limit, not limit_words)
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
    parser.add_argument("file", help="The file containing the corpus text from"
                        " which to generate the Markov chain.")
    parser.add_argument("-r", "--recipient", help="The recipient of the email."
                        " Defaults to {}.".format(DEFAULT_RECIPIENT),
                        default=DEFAULT_RECIPIENT)
    parser.add_argument("-s", "--subject", help="The subject of the email."
                        " Defaults to {}.".format(DEFAULT_SUBJECT),
                        default=DEFAULT_SUBJECT)
    parser.add_argument("-t", "--host", help="The SMTP host to use. Defaults "
                        "to {}.".format(DEFAULT_HOST), default=DEFAULT_HOST)
    parser.add_argument("-k", "--keysize", help="The key size to use for "
                        "Markov chain generation. Defaults to "
                        "{}.".format(DEFAULT_KEY_SIZE), type=int,
                        default=DEFAULT_KEY_SIZE)
    parser.add_argument("-l", "--limit", help="The character (or word) limit "
                        "to impose on the generated text. Defaults to "
                        "{}.".format(DEFAULT_LIMIT), type=int,
                        default=DEFAULT_LIMIT)
    parser.add_argument("-w", "--limit_words", help="Specify this flag to "
                        "limit the generated text by word count instead of "
                        "character count.", action="store_true")

    args = parser.parse_args()

    send_markov(args.user, args.password, args.recipient, args.subject,
                args.host, args.file, args.keysize, args.limit,
                args.limit_words)
