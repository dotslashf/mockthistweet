class Kalimat:
    def __init__(self, sentence):
        self.sentence = sentence

    def getSentence(self):
        text = self.removeWords()
        return text

    def removeWords(self):
        finalText = ''
        excludedChars = [',', '.', '!', '?']
        excludedWords = ['2beer', 'mksfess']
        words = [i for j in self.sentence.split() for i in (j, ' ')][:-1]
        for i, word in enumerate(words):
            if word[0] == '@':
                word = word.replace(word, '')
            for ew in excludedWords:  # remove unnecassary words
                word = word.replace(ew, '')
            for i, char in enumerate(word):
                for ec in excludedChars:  # remove unnecessary char
                    char = char.replace(ec, '')
                finalText += char
        self.sentence = finalText
        return self.sentence

    def transform(self):
        finalText = ''
        text = self.removeWords()
        for i, char in enumerate(text):
            if i % 2 != 0:
                char = char.replace(char, char.upper())
                finalText += char
            else:
                finalText += char
        self.sentence = finalText
        return self.sentence


# k = Kalimat("heh gaboleh gitu tapi bener, juga sih haha norak")
# k.transform()
# print(k.sentence)
