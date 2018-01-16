import csv

global_id = 0
from_cd = {}
career_cd = {}
field_cd = {}
zip_cd = {}
use = [
    'id', 'gender', 'age', 'field', 'undergrd', 'tuiton', 'race', 'imprace',
    'imprelig', 'from', 'zipcode', 'income', 'goal', 'date', 'go_out',
    'career', 'sport', 'tvsports', 'excersice', 'dining', 'museums', 'art',
    'hiking', 'gaming', 'clubbing', 'reading', 'tv', 'theater', 'movies',
    'concerts', 'music', 'shopping', 'yoga', 'exphappy', 'expnum',
    'match_es', 'length'
]
percentage = {
    'age': 80, 'field': 50, 'undergrd': 50, 'tuiton': 40, 'race': 40,
    'imprace': 30, 'imprelig': 30, 'from': 60, 'zipcode': 15, 'income': 45,
    'goal': 30, 'date': 30, 'go_out': 40, 'career': 45, 'sport': 30,
    'tvsports': 30, 'excersice': 35, 'dining': 50, 'museums': 30, 'art': 55,
    'hiking': 30, 'gaming': 30, 'clubbing': 30, 'reading': 30, 'tv': 30,
    'theater': 40, 'movies': 45, 'concerts': 35, 'music': 60, 'shopping': 35,
    'yoga': 30, 'exphappy': 30, 'expnum': 30, 'match_es': 30, 'match': 30,
    'length': 45
}
seuil = 150

def toInt(s):
    try:
        ret = int(s)
        return ret
    except ValueError:
        return s

def get_percentage(dat, d):
    count_percentage = 0
    if dat['gender'] == d['gender']:
        return 0
    shared_items = set(dat.items()) & set(d.items())
    for key, val in shared_items:
        if val and key and key != "id":
            count_percentage += int(percentage[key])
    return count_percentage

def createGraph(data):
    graph = []
    for dat in data:
        i = 0
        graph.append([])
        for d in data:
            shared_items = get_percentage(dat, d)
            if d != dat and shared_items > seuil:
                graph[-1].append(i)
            i += 1
    # print(graph)
    return graph

def encodeFrom(value):
    if not value in from_cd.keys():
        from_cd[value] = len(from_cd)
    return from_cd[value]

def encodeZip(value):
    if not value in zip_cd.keys():
        zip_cd[value] = len(zip_cd)
    return zip_cd[value]

def encodeCareer(value):
    if not value in career_cd.keys():
        career_cd[value] = len(career_cd)
    return career_cd[value]

def encodeField(value):
    if not value in field_cd.keys():
        field_cd[value] = len(field_cd)
    return field_cd[value]

def normalizeIncome(value):
    if value > 0 and value < 40000:
        return 1
    elif value < 65000:
        return 2
    return 3

def setId(value):
    return global_id

vars_treatment = {
    'from': encodeFrom,
    'id': setId,
    'income': normalizeIncome,
    'zipcode': encodeZip,
    "field": encodeField,
    "career": encodeCareer
}

def readFile():
    keys = []
    data = []
    indexes = []

    global global_id
    with open('data.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            row = row[:-1]
            if global_id == 0:
                j = 0
                for key in row:
                    if any(key in elem for elem in use):
                        indexes.append(j)
                    keys.append(key)
                    j += 1
            else:
                data.append({})
                for j in indexes:
                    if row[j] != '' and keys[j] in vars_treatment.keys():
                        data[global_id - 1].update({
                            keys[j]: vars_treatment[keys[j]](row[j])
                        })
                    else:
                        data[global_id - 1].update({
                            keys[j]: toInt(row[j])
                        })
            global_id += 1
    # print data[:5]
    return data

def main():
    data = readFile()
    graph = createGraph(data)

main()
