Overview
========

markov.py
--------------

A Python program that generates strings of pseudorandom text using a simple Markov chain procedure.

### Arguments

Positional:
 * Files: Any number of plaintext files to serve as the corpus for generating the Markov chain. (If multiple files are provided, only text generated using input from each file will be accepted. As files can be radically different sizes, and the generation is more or less random, it's recommended that you use files that are 'round about the same size, and not too many of them.)

Options:
 * -k, --key_size: The number of words to use to constitute the "present state" of the chain. (Defaults to 2.)
 * -l, --limit: A word (or character) limit for the generated text. (Defaults to 300.)

Flags:
 * -c, --limit_chars: Limits Markov text generation to the specified number of words (instead of characters).
 * -q, --strip_quotes: Removes all quotation marks from the corpus text before generating chains.
 * -b, --strip_parens: Removes all parentheses from the corpus text before generating chains.
 * -p, --paragraphs: Generates paragraph breaks (two line feeds) every few sentences.


send_markov.py
--------------

A Python program that generates strings of pseudorandom text using a simple Markov chain procedure and sends them via email (intended for use with Twitter via IFTTT).

### Arguments

Positional:
 * User: The email account to use to send the email.
 * Password: The email account password.
 * Files: Any number of plaintext files to serve as the corpus for generating the Markov chain. (If multiple files are provided, only text generated using input from each file will be accepted. As files can be radically different sizes, and the generation is more or less random, it's recommended that you use files that are 'round about the same size, and not too many of them.)

Options:
 * -r, --recipient: The email address to which to send the generated message.
 * -s, --subject: The subject of the  email to send.
 * -t, --host: The SMTP host to use. (Defaults to Gmail.)
 * -k, --key_size: The number of words to use to constitute the "present state" of the chain. (Defaults to 2.)
 * -l, --limit: A character (or word) limit for the generated text. (Defaults to 140.)

Flags:
 * -w, --limit_words: Limits Markov text generation to the specified number of words (instead of characters).
 * -p, --paragraphs: Generates paragraph breaks (two line feeds) every few sentences.

Bugs and Feature Requests
=========================

Feature Requests
----------------

* None

Known Bugs
----------

* None

Special Thanks
==============

In writing the Markov chain generator, I read over some generators other developers had written, most notably:
http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/

License Information
===================

Written by Gem Newman.
http://www.startleddisbelief.com

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
