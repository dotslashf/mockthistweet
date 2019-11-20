import time

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)


def loadData(file):
    with open(file, "r") as f:
        b = f.readlines()

    return b


def writeData(file, last_id):
    f = open(file, "a+")
    f.write(last_id+'\n')


def writeDataError(tweet, error):
    f = open("text/error_log.txt", "a+")
    f.write("tweet id: "+tweet.id_str+" error code: " +
            str(error)+current_time+'\n')
