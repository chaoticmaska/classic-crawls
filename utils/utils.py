import json


def writeToFile(data, filename):
    file = open(filename, 'w')
    file.write(json.dumps(data))
    file.close()
