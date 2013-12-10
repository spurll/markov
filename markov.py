#!/usr/bin/env python

# Written by Gem Newman. This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.


import random


DEFAULT_KEY_SIZE = 3


class Markov(object):
    def __init__(self, filename, key_size=DEFAULT_KEY_SIZE):
        self.transitions = {}
        self.initial = []
        self.key_size = key_size

        with open(filename) as corpus:
            self.words = corpus.read().split()

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

    def generate_text(self, sentence=True, word_limit=None, char_limit=None):
        try_again = True

        while try_again:
            try_again = False

            present = random.choice(self.initial)
            chain = list(present[:self.key_size-1])

            if sentence:
                while True:
                    chain.append(present[-1])
                    present = present[1:] + \
                              (random.choice(self.transitions[present]),)
                    
                    if chain[-1][-1] in [".", "!", "?"]:
                        # Ensure that length constraints are met.
                        if (word_limit and len(chain) > word_limit) or \
                           (char_limit and len(" ".join(chain)) > char_limit):
                            print("Too long!")
                            try_again = True
                        break

            elif word_limit:
                for i in range(word_limit - len(chain)):
                    chain.append(present[-1])
                    present = present[1:] + \
                              (random.choice(self.transitions[present]),)

            elif character_limit:
                while len(" ".join(chain)) + len(present[-1]) < character_limit:
                    chain.append(present[-1])
                    present = present[1:] + \
                              (random.choice(self.transitions[present]),)

            text = " ".join(chain)

            # Check to make sure it's actually a new string of text.
            if text in self.corpus:
                print("This isn't a new string! It's straight from the text!")
                try_again = True

        return text
