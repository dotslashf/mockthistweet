import emoji
import random


class Emoji:
    def __init__(self, sentence):
        self.sentence = sentence
        self.list_emoji = emoji.unicode_codes.EMOJI_UNICODE
        self.emoji = ''

    def random(self):
        r = random.randint(0, len(self.list_emoji))
        return r

    def pick_emoji(self, r_emoji):
        for i, k in enumerate(self.list_emoji.items()):
            if i == r_emoji:
                char_emoji = emoji.emojize(k[0])
        self.emoji = char_emoji

    def create_pattern(self, pattern):

        finalText = ''
        if pattern == 'k':
            b1 = [0, 1, 12, 13]
            b2 = [0, 1, 7, 8]
            b3 = [0, 1, 2, 3]

            for i in range(6):
                for j in range(14):
                    if i == 0 and j in b1:
                        finalText += self.emoji
                        if j == 13:
                            finalText += '\n'
                    elif i == 1 and j in b2:
                        finalText += self.emoji
                        if j == 8:
                            finalText += '\n'
                    elif i == 2 and j in b3:
                        finalText += self.emoji
                        if j == 3:
                            finalText += '\n'
                    elif i == 3 and j in b3:
                        finalText += self.emoji
                        if j == 3:
                            finalText += '\n'
                    elif i == 4 and j in b2:
                        finalText += self.emoji
                        if j == 8:
                            finalText += '\n'
                    elif i == 5 and j in b1:
                        finalText += self.emoji
                        if j == 13:
                            finalText += self.sentence[1:(len(self.sentence))]

                    else:
                        if i == 0 and j in range(2, 11):
                            finalText += ' '
                        elif i == 1 and j in range(2, 9):
                            finalText += ' '
                        elif i == 4 and j in range(2, 9):
                            finalText += ' '
                        elif i == 5 and j in range(2, 11):
                            finalText += ' '

        elif pattern == 'b':
            b1 = [0, 1, 2, 3]
            b2 = [0, 1, 10, 11]

            for i in range(6):
                for j in range(12):
                    if i == 0 and j in b1:
                        finalText += self.emoji
                        if j == 3:
                            finalText += '\n'
                    elif i == 1 and j in b2:
                        finalText += self.emoji
                        if j == 11:
                            finalText += '\n'
                    elif i == 2 and j in b1:
                        finalText += self.emoji
                        if j == 3:
                            finalText += '\n'
                    elif i == 3 and j in b2:
                        finalText += self.emoji
                        if j == 11:
                            finalText += '\n'
                    elif i == 4 and j in b2:
                        finalText += self.emoji
                        if j == 11:
                            finalText += '\n'
                    elif i == 5 and j in b1:
                        finalText += self.emoji
                        if j == 3:
                            finalText += self.sentence[1:len(self.sentence)]
                    else:
                        if i == 1 and j in range(1, 10):
                            finalText += ' '
                        elif i == 3 and j in range(1, 10):
                            finalText += ' '
                        elif i == 4 and j in range(1, 10):
                            finalText += ' '

        elif pattern == 'j':
            b1 = [13, 14]
            b2 = [0, 1, 8, 9]
            b3 = [0, 1, 2, 3, 4]
            b4 = [4, 5, 6]

            for i in range(6):
                for j in range(15):
                    if i == 0 and j in b1:
                        finalText += self.emoji
                        if j == 14:
                            finalText += '\n'
                    elif i == 1 and j in b1:
                        finalText += self.emoji
                        if j == 14:
                            finalText += '\n'
                    elif i == 2 and j in b1:
                        finalText += self.emoji
                        if j == 14:
                            finalText += '\n'
                    elif i == 3 and j in b2:
                        finalText += self.emoji
                        if j == 9:
                            finalText += '\n'
                    elif i == 4 and j in b3:
                        finalText += self.emoji
                        if j == 4:
                            finalText += '\n'
                    elif i == 5 and j in b4:
                        finalText += self.emoji
                        if j == 6:
                            finalText += self.sentence[1:len(self.sentence)]
                    else:
                        if i == 0 and j in range(0, 14):
                            if j == 0 or j == 12:
                                finalText += u"\u2800"
                            else:
                                finalText += ' '
                        elif i == 1 and j in range(0, 14):
                            if j == 0 or j == 12:
                                finalText += u"\u2800"
                            else:
                                finalText += ' '
                        elif i == 2 and j in range(0, 14):
                            if j == 0 or j == 12:
                                finalText += u"\u2800"
                            else:
                                finalText += ' '
                        elif i == 3 and j in range(2, 7):
                            finalText += ' '
                        elif i == 5 and j in range(0, 4):
                            finalText += ' '

        return finalText


# e = Emoji("jancok raimu iku lho")

# re = e.random()
# print(re)
# e.pick_emoji(re)
# jadi = e.create_pattern('j')
# # jadi += "test"
# print(jadi)
