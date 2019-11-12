def loadData(file):
    with open(file, "r") as f:
        b = f.readlines()

    return b


def writeData(file, last_id):
    f = open(file, "a+")
    f.write(last_id+'\n')
