import csv

def toInt(s):
    try:
        ret = int(s)
        return ret
    except ValueError:
        return s

def readFile():
    keys = []
    data = []
    i = 0

    with open('dataset.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            row = row[:-1]
            if i == 0:
                for key in row:
                    keys.append(key)
            else:
                data.append({})
                for j in range(0, len(keys)):
                    data[i - 1].update({keys[j]: toInt(row[j])})
            i += 1
    # print data[0]
    return data

# readFile()
