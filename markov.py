#!/usr/bin/env python

# Written by Gem Newman. This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.


import random


DEFAULT_KEY_SIZE = 2
MINIMUM_WORDS = 5


class Markov(object):
    def __init__(self, filename, key_size=DEFAULT_KEY_SIZE):
        self.transitions = {}
        self.initial = []
        self.key_size = key_size

        with open(filename) as corpus:
            text = corpus.read()
            text = text.replace('"', "").replace("(", "").replace(")", "")
            self.words = text.split()

        self.corpus = " ".join(self.words)
        self.define_transitions()

    def define_transitions(self):
        for k, w in self.transition_generator():
            # Add to transition dictionary.
            if k in self.transitions:
                self.transitions[k].append(w)
            else:
                self.transitions[k] = [w]

            # Check to see if it qualifies as a starting place.
            first_letter = k[0][0]
            if first_letter >= "A" and first_letter <= "Z":
                self.initial.append(k)

    def transition_generator(self):
        if len(self.words) < self.key_size + 1:
            return

        for i in range(len(self.words) - self.key_size):
            yield (tuple(self.words[i:i+self.key_size]),
                   self.words[i+self.key_size])

    def generate_text(self, limit=None, limit_by_char=False):
        if not limit:
            print "A word (or character) limit must be specified."
            return

        try_again = True

        while try_again:
            try_again = False

            present = random.choice(self.initial)
            chain = list(present[:self.key_size-1])

            length = len(" ".join(chain)) if limit_by_char else len(chain)

            while length < limit:
                chain.append(present[-1])
                present = present[1:] + \
                          (random.choice(self.transitions[present]),)
                length = len(" ".join(chain)) if limit_by_char else len(chain)

            # Because words are added one at a time, but characters aren't, we
            # may need to prune if we used a character limit.
            if limit_by_char and length > limit:
                chain = chain[:-1]

            # Now we don't want to end on an incomplete thought, so prune until
            # we hit an appropriate punctuation mark.
            while chain and chain[-1][-1] not in [".", "!", "?"]:
                chain = chain[:-1]

            text = " ".join(chain)

            # Make sure that what we've generated is worthwhile.
            if len(chain) < MINIMUM_WORDS or text in self.corpus:
                try_again = True
                print("Trying again.")

        return text
