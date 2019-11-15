from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from kalimat import Kalimat

font = ImageFont.truetype("impact.ttf", 42)

# draw the text and outline
def drawTextOutline(text, x, y, draw):
    draw.text((x-2, y-2), text, (0, 0, 0), font=font)
    draw.text((x+2, y-2), text, (0, 0, 0), font=font)
    draw.text((x+2, y+2), text, (0, 0, 0), font=font)
    draw.text((x-2, y+2), text, (0, 0, 0), font=font)
    draw.text((x, y), text, (255, 255, 255), font=font)
    return

def splitLines(text, img, draw, pos):
    print("------------------------------------------------")
    w, h = draw.textsize(text, font)  # measure the size the text will take
    lineCount = 1
    if w > img.width:
        lineCount = int(round((w / img.width) + 1))

    print("lineCount: {}".format(lineCount))

    lines = []
    if lineCount > 1:

        lastCut = 0
        isLast = False
        for i in range(0, lineCount):
            if lastCut == 0:
                cut = (len(text) / lineCount) * i
            else:
                cut = lastCut

            if i < lineCount-1:
                nextCut = (len(text) / lineCount) * (i+1)
            else:
                nextCut = len(text)
                isLast = True

            print("cut: {} -> {}".format(cut, nextCut))

            nextCut = round(nextCut)
            cut = round(cut)

            # make sure we don't cut words in half
            if nextCut == len(text) or text[nextCut] == " ":
                print("may cut")
            else:
                print("may not cut")
                while text[nextCut] != " ":
                    nextCut += 1
                print("new cut: {}".format(nextCut))

            line = text[cut:nextCut].strip()

            # is line still fitting ?
            w, h = draw.textsize(line, font)
            if not isLast and w > img.width:
                print("overshot")
                nextCut -= 1
                while text[nextCut] != " ":
                    nextCut -= 1
                print("new cut: {}".format(nextCut))

            lastCut = nextCut
            lines.append(text[cut:nextCut].strip())

    else:
        lines.append(text)

    print(lines)

    if pos == "top":
        lastY = -h + 25
    elif pos == "bottom":
        lastY = img.height - h * (lineCount+1) - 25


    for i in range(0, lineCount):
        w, h = draw.textsize(lines[i], font)
        x = img.width/2 - w/2
        y = lastY + h
        drawTextOutline(lines[i], x, y, draw)
        lastY = y

    img.save("img/meme_new_format.png")


# draw text
def drawText(bottomText, memeLocation):
    img = Image.open(memeLocation)
    draw = ImageDraw.Draw(img)

    splitLines(bottomText, img, draw, "bottom")
    print("------------------------------------------------")


# k = Kalimat(
#     "coba dulu ini deh ya semoga bisa dong hehe coba dulu ini deh ya semoga bisa dong hehe")
# text = k.transform()
# drawText(text, "img/meme_new_2.png")
