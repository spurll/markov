Overview
========

send_markov.py
--------------

A Python program that generates strings of pseudorandom text using a simple Markov chain procedure and sends them via email (intended for use with Twitter via IFTTT).

### Arguments

Positional:
 * User: The email account to use to send the email.
 * Password: The email account password.
 * File: A plaintext file to serve as the corpus for generating the Markov chain.

Options:
 * -r, --recipient: The email address to which to send the generated message.
 * -s, --subject: The subject of the  email to send.
 * -t, --host: The SMTP host to use. (Defaults to Gmail.)
 * -k, --keysize: The number of words to use to constitute the "present state" of the chain. (Defaults to 3.)
 * -l, --limit: A character (or word) limit for the generated text. (Defaults to 140.)

Flags:
 * -w, --limit_words: Limits Markov text generation to the specified number of words (instead of characters).

Bugs and Feature Requests
=========================

Feature Requests
----------------

* Support for multiple input files with a guarentee that text generated contains at least a little of each.

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
