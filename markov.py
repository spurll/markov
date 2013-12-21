#!/usr/bin/env python

# Written by Gem Newman. This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.


import random, re
from argparse import ArgumentParser


DEFAULT_KEY_SIZE = 2
DEFAULT_LIMIT = 300
PARAGRAPH_LENGTH = 4
MINIMUM_WORDS = 5
STRIP_QUOTES = True
STRIP_PARENS = True


class Markov(object):
    def __init__(self, files, key_size=DEFAULT_KEY_SIZE,
                 strip_quotes=STRIP_QUOTES, strip_parens=STRIP_PARENS):
        self.initial = []
        self.key_size = key_size
        self.transitions = []   # List of transition dictionaries for files.
        self.corpus = ""        # Full text of all files.
        self.words = []         # List of lists of words in each file.

        if isinstance(files, basestring):
            files = [files]

        for f in files:
            with open(f) as current:
                text = current.read()

                if strip_quotes:
                    text = text.replace('"', "")
                if strip_parens:
                    text = text.replace("(", "").replace(")", "")

                self.words.append(text.split())     # Add words to next slot.

        self.corpus = " ".join([" ".join(w) for w in self.words])
        self.define_transitions()

    def define_transitions(self):
        for f in self.words:
            transitions = {}
            for k, w in self.transition_generator(f):
                # Add to transition dictionary.
                if k in self.transitions:
                    transitions[k].append(w)
                else:
                    transitions[k] = [w]

                # Check to see if it qualifies as a starting place.
                first_letter = k[0][0]
                if first_letter >= "A" and first_letter <= "Z":
                    self.initial.append(k)

            # Add this file's transition dictionary to the list of
            # dictionaries. (They're kept separate so that we can make sure we
            # use some from each wihle generating our chain.)
            self.transitions.append(transitions)

    def transition_generator(self, words):
        if len(words) < self.key_size + 1:
            return

        for i in range(len(words) - self.key_size):
            yield (tuple(words[i:i+self.key_size]), words[i+self.key_size])

    def generate_text(self, limit=None, limit_by_char=False, paragraphs=True):
        if not limit:
            print "A word (or character) limit must be specified."
            return

        try_again = True

        while try_again:
            try_again = False

            present = random.choice(self.initial)
            chain = list(present[:self.key_size-1])

            length = len(" ".join(chain)) if limit_by_char else len(chain)

            # Keep track of which files' transition dictionaries are used.
            used = []

            select_dictionary = range(len(self.transitions))
            while length < limit:
                chain.append(present[-1])

                random.shuffle(select_dictionary)
                for i in select_dictionary:
                    if present in self.transitions[i]:
                        next_word = (random.choice(self.transitions[i][present]),)
                        used.append(i)  # Record that we used this dictionary.
                        break

                present = present[1:] + next_word
                length = len(" ".join(chain)) if limit_by_char else len(chain)

            # Because words are added one at a time, but characters aren't, we
            # may need to prune if we used a character limit.
            if limit_by_char and length > limit:
                chain = chain[:-1]
                used = used[:-1]

            # Now we don't want to end on an incomplete thought, so prune until
            # we hit an appropriate punctuation mark.
            while chain and chain[-1][-1] not in [".", "!", "?"]:
                chain = chain[:-1]
                used = used[:-1]

            text = " ".join(chain)

            # Check that the chain is long enough and that the text is actually
            # a new string (not in the input files). 
            if len(chain) < MINIMUM_WORDS or text in self.corpus:
                try_again = True
                print "Chain not worthwhile. Trying again."

            # Check that the text contains items from all files.
            if not set(range(len(self.transitions))).issubset(used):
                try_again = True
                print "Only transitions from files {} were used. Trying " \
                      "again.".format(list(set(used)))

            # Generate random paragraph breaks, if requested.
            if paragraphs:
                # Find all instances of ". ".
                indices = [match.start() for match in
                           re.finditer(re.escape(". "), text)]

                # Replace every third instance of it with ".\n\n".
                for i in xrange(PARAGRAPH_LENGTH - 1, len(indices), PARAGRAPH_LENGTH):
                    text = "|".join([text[:indices[i]+1], text[indices[i]+2:]])

                text = text.replace("|", "\n\n")

        return text


if __name__ == "__main__":
    parser = ArgumentParser(description="Generates a pseudorandom string of "
                            "text using a Markov chain.")
    parser.add_argument("files", help="The file(s) containing the raw text to "
                        " use in generating the Markov chain.", nargs="+")
    parser.add_argument("-k", "--key_size", help="The key size to use for "
                        "Markov chain generation. Defaults to "
                        "{}.".format(DEFAULT_KEY_SIZE), type=int,
                        default=DEFAULT_KEY_SIZE)
    parser.add_argument("-l", "--limit", help="The word (or character) limit "
                        "to impose on the generated text. Defaults to "
                        "{}.".format(DEFAULT_LIMIT), type=int,
                        default=DEFAULT_LIMIT)
    parser.add_argument("-c", "--limit_chars", help="Specify this flag to "
                        "limit the generated text by character count instead "
                        "of by word count.", action="store_true")
    parser.add_argument("-q", "--strip_quotes", help="Specify this flag to "
                        "strip all quotation marks from the input files.",
                        action="store_true")
    parser.add_argument("-b", "--strip_parens", help="Specify this flag to "
                        "strip all parentheses from the input files.",
                        action="store_true")
    parser.add_argument("-p", "--paragraphs", help="Specify this flag to "
                        "add paragraph breaks to the text every once in a "
                        "while.", action="store_true")

    args = parser.parse_args()

    m = Markov(args.files, args.key_size, args.strip_quotes, args.strip_parens)
    print m.generate_text(args.limit, args.limit_chars, args.paragraphs)
