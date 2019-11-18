import demoji  # for removing emoji


class Kalimat:
    def __init__(self, sentence):
        self.sentence = sentence

    def getSentence(self):
        text = self.removeWords()
        return text

    def removeWords(self):
        self.sentence = demoji.replace(self.sentence)
        finalText = ''
        excludedChars = [',', '.', '!', '?', '&', '-', '"']
        excludedWords = ['2beer!', 'mksfess',
                         '[askmf]', '[cm]', '[gmf]', '[tanyarl]', '/wal', '/rlt/']
        invisibleChar = [u"\u2800", u"\u2063"]
        words = [i for j in self.sentence.split() for i in (j, ' ')][:-1]
        for word in words:
            word = word.lower()

            # remove twt username, hashtag, and links
            if word[0] == '@' or word[0] == '#' or word[0:4] == 'http':
                word = word.replace(word, '')
            for ew in excludedWords:  # remove unnecassary words
                word = word.replace(ew, '')

            for char in word:
                if char in invisibleChar:  # remove invisible char
                    char = char.replace(char, '')
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

    def transformoji(self, emoji_type):
        finalText = ''
        text = self.removeWords()
        text = text.split()

        if emoji_type == "laugh":
            for word in text:
                word += "😂"
                finalText += word
            return finalText

        elif emoji_type == "clap":
            for word in text:
                word += "👏"
                finalText += word
            return finalText


# Testing purpose
# k = Kalimat("Mbanya ada masalah apasih sebenernya ? Psikologis mba keganggu ya ? Yuk mba kita meet up, biar mbayna ga bar bar di Twitter n bisa tau di rl ya !!! 🙃 Soalnya orang yg di twitter bar bar, pasti dirlnya ciut, ga berani ngomong apa apa, n malu ama yg dihujatmya 🙃")
# k.removeWords()
# kalimat = k.getSentence()
# print(k.sentence)
# print(k.transformoji("clap"))
# print(k.transformoji("laugh"))
# print(k.sentence)
