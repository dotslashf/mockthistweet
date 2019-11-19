def loadData(file):
    with open(file, "r") as f:
        b = f.readlines()

    return b


def writeData(file, last_id):
    f = open(file, "a+")
    f.write(last_id+'\n')


def writeDataError(tweet, error):
    f = open("error_log.txt", "a+")
    f.write("tweet id: "+tweet.id_str+" error code: "+str(error)+'\n')
