class Kalimat:
    def __init__(self, sentence):
        self.sentence = sentence

    def getSentence(self):
        return self.sentence

    def transform(self):
        finalText = ''
        excludedChars = [',', '.', '!', '?']
        excludedChars = ''
        excludedWords = ['2beer', 'mksfess']
        words = [i for j in self.sentence.split() for i in (j, ' ')][:-1]
        for i, word in enumerate(words):
            for ew in excludedWords:  # remove unnecassary words
                word = word.replace(ew, '')
            for i, char in enumerate(word):
                for ec in excludedChars:  # remove unnecessary char
                    char = char.replace(ec, '')
                if char.isupper():  # make char all lowercase
                    char = char.lower()
                if i % 2 != 0:  # transform text based on meme
                    char = char.upper()
                finalText += char
        self.sentence = finalText
        return self.sentence
