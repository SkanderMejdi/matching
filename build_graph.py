import csv

def toInt(s):
    try:
        ret = int(s)
        return ret
    except ValueError:
        return s

def createGraph(data):
    graph = []
    for dat in data:
        i = 0
        if len(graph) == 0 or (len(graph) > 0 and graph[-1]):
            graph.append([])
        for d in data:
            shared_items = set(dat.items()) & set(d.items())
            if d != dat and len(shared_items) > 0:
                graph[-1].append(i)
            i += 1
    print(graph)
    return graph

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
    graph = createGraph(data)

main()
