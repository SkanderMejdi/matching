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
    use = [
        'id', 'gender', 'age', 'field', 'undergrd', 'tuiton', 'race', 'imprace',
        'imprelig', 'from', 'zipcode', 'income', 'goal', 'date', 'go_out',
        'career', 'sport', 'tvsports', 'excersice', 'dining', 'museums', 'art',
        'hiking', 'gaming', 'clubbing', 'reading', 'tv', 'theater', 'movies',
        'concerts', 'music', 'shopping', 'yoga', 'exphappy', 'expnum',
        'match_es', 'length'
    ]
    indexes = []
    i = 0

    with open('data.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            row = row[:-1]
            if i == 0:
                j = 0
                for key in row:
                    if any(key in elem for elem in use):
                        indexes.append(j)
                    keys.append(key)
                    j += 1
            else:
                data.append({})
                for j in indexes:
                    data[i - 1].update({keys[j]: toInt(row[j])})
            i += 1
    print data[0]
    return data

def main():
    data = readFile()

main()
