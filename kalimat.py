class Kalimat:
    def __init__(self, sentence):
        self.sentence = sentence

    def getSentence(self):
        text = self.removeWords()
        return text

    def removeWords(self):
        finalText = ''
        excludedChars = [',', '.', '!', '?']
        excludedWords = ['2beer!', 'mksfess', '[askmf]', '[cm]', '[gmf]', ]
        words = [i for j in self.sentence.split() for i in (j, ' ')][:-1]

        for word in words:
            word = word.lower()
            if word[0] == '@' or word[0] == '#' or word[0:4] == 'http':
                word = word.replace(word, '')

            for ew in excludedWords:  # remove unnecassary words
                word = word.replace(ew, '')
            for char in word:
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

    def trinsfirm(self):
        finalText = ''
        text = self.removeWords()
        consonant = ['a', 'u', 'e', 'o']
        for char in text:
            if char in consonant:
                char = char.replace(char, 'i')
                finalText += char
            else:
                finalText += char
        self.sentence = finalText
        return self.sentence


# Testing purpose
# k = Kalimat(
#     "@fadhlu heh gaboleh GITU tapi #fadhlu bener, juga sih haha norak 2beer!")
# k.trinsfirm()
# print(k.sentence)
