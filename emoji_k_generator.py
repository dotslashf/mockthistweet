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

    def create_pattern(self):
        b1 = [0, 1, 12, 13]
        b2 = [0, 1, 7, 8]
        b3 = [0, 1, 2, 3]

        finalText = ''
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
        return finalText


# e = Emoji("kontol")
# # # b = Twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# re = e.random()
# print(re)
# e.pick_emoji(re)
# jadi = e.create_pattern()
# jadi += "test"
# print(jadi)
# # b.api.update_status(status=jadi)
