from kalimat import Kalimat
from generator import drawText

k = Kalimat("test dulu ini coba yah anjay")
text = k.transform()

drawText(text, "bottom")
