from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from kalimat import Kalimat


# loading kalimat class
k = Kalimat("Ya kalau lu belajar budaya yg serius lah, bercandain tarian")
k.transform()
kalimat = k.kalimat

# importing image
img = Image.open("img/meme_squared.png")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("impact.ttf", 42)

# draw the text and outline


def drawText(text, x, y):
    draw.text((x-2, y-2), text, (0, 0, 0), font=font)
    draw.text((x+2, y-2), text, (0, 0, 0), font=font)
    draw.text((x+2, y+2), text, (0, 0, 0), font=font)
    draw.text((x-2, y+2), text, (0, 0, 0), font=font)
    draw.text((x, y), text, (255, 255, 255), font=font)
    return


wKalimat, hKalimat = draw.textsize(kalimat, font)
drawText(kalimat, img.width/2 - wKalimat/2,
         (img.height - img.height/10) - hKalimat/2)

# separated kalimat into more lines
if wKalimat > img.width:
    lineCount = int(round((wKalimat / img.width) + 1))

print("lineCount: {}".format(lineCount))

lines = []
if lineCount > 1:

    lastCut = 0
    isLast = False
    for i in range(0, lineCount):
        if lastCut == 0:
            cut = (len(kalimat) / lineCount) * i
        else:
            cut = lastCut

        if i < lineCount-1:
            nextCut = (len(kalimat) / lineCount) * (i+1)
        else:
            nextCut = len(kalimat)
            isLast = True

        nextCut = round(nextCut)
        cut = round(cut)

        print("cut: {} -> {}".format(cut, nextCut))

        # make sure we don't cut words in half
        if (nextCut == len(kalimat)) or (kalimat[nextCut] == " "):
            print("may cut")
        else:
            print("may not cut")
            while kalimat[nextCut] != " ":
                nextCut += 1
            print("new cut: {}".format(nextCut))

        line = kalimat[cut:nextCut].strip()

        # is line still fitting ?
        w, h = draw.textsize(line, font)
        if not isLast and w > img.width:
            print("overshot")
            nextCut -= 1
            while kalimat[nextCut] != " ":
                nextCut -= 1
            print("new cut: {}".format(nextCut))

        lastCut = nextCut
        lines.append(kalimat[cut:nextCut].strip())

else:
    lines.append(kalimat)

print(lines)


# img.save("test.png")
