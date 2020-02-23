import demoji  # for removing emoji
from art import *


class Kalimat:
    def __init__(self, sentence):
        self.sentence = sentence
        self.excludedWords = ['2beer!', 'mksfess',
                              '[askmf]', '[cm]',
                              '[gmf]', 'tanyarl',
                              '/wal', '/rlt/',
                              '/krt/', 'fess',
                              'brl!', 'yeet!',
                              '/mahasantuy/', '(nyampah)']
        self.excludedChars = ['%']

    def getSentence(self):
        text = self.removeWords()
        return text

    def removeWords(self):
        self.sentence = demoji.replace(self.sentence)
        finalText = ''
        invisibleChar = [u"\u2800", u"\u2063", u'\xe3', u'\xa4']
        words = [i for j in self.sentence.split() for i in (j, ' ')][:-1]
        for word in words:
            word = word.lower()

            # remove twt username, hashtag, and links
            if word[0] == '@' or word[0] == '#' or word[0:4] == 'http':
                word = word.replace(word, '')
            if word[0:5] == '&amp;':
                word = word.replace(word, '&')
            for ew in self.excludedWords:  # remove unnecassary words
                word = word.replace(ew, '')

            for char in word:
                if char in invisibleChar:  # remove invisible char
                    char = char.replace(char, '')
                if char in self.excludedChars:  # remove unnecessary char
                    char = char.replace(char, '')
                finalText += char

        return finalText

    def transform(self):
        finalText = ''
        text = self.removeWords()
        for i, char in enumerate(text):
            if i % 2 != 0:
                char = char.replace(char, char.upper())
                finalText += char
            else:
                finalText += char

        return finalText

    def trinsfirm(self):
        finalText = ''
        text = self.removeWords()
        vokal = ['a', 'u', 'e', 'o']
        for char in text:
            if char in vokal:
                char = char.replace(char, 'i')
                finalText += char
            else:
                finalText += char

        return finalText

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

        elif emoji_type == "vomit":
            for word in text:
                word += "🤮"
                finalText += word
            return finalText

        elif emoji_type == "sick":
            for word in text:
                word += "🤢"
                finalText += word
            return finalText

        elif emoji_type == "poop":
            text = self.removeWords()
            for char in text:
                if char is not ' ':
                    char = char.replace(char, '💩')
                    finalText += char
                else:
                    finalText += char
            return finalText

    def transformalay(self):
        finalText = ''
        text = self.removeWords()
        finalText = text2art(text, 'mix')
        return finalText
