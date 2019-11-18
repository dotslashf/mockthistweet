import sys
import tweepy
import time
import os
import random
from kalimat import Kalimat
from generator import drawText
from auth import authentication
from load import loadData, writeData

:)))))))))))))))))))))) GANTI FILE


while True:
    last_id = loadData(FILE_LAST_ID)
    last_id = int(last_id[-1])
    since_id = getMentionTweet(triggeringWords, last_id, errorCode)

    print("------------------------------------------------",
          "\n| newest tweet: ", since_id,
          "\n| oldest tweet: ", last_id,
          "\n------------------------------------------------\n")

    if (last_id != since_id):
        writeData(FILE_LAST_ID, str(since_id))
    else:
        print('no new mention')

    for sec in range(180, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} second to check mention.\r".format(sec))
        sys.stdout.flush()
        time.sleep(1)
