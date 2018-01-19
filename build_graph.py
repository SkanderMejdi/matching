import csv

global_id = 0
from_cd = {}
career_cd = {}
field_cd = {}
zip_cd = {}
undergra_cd = {}
use = [
    'id', 'gender', 'age', 'field', 'undergra', 'tuiton', 'race', 'imprace',
    'imprelig', 'from', 'zipcode', 'income', 'goal', 'date', 'go_out',
    'career', 'sports', 'tvsports', 'excersice', 'dining', 'museums', 'art',
    'hiking', 'gaming', 'clubbing', 'reading', 'tv', 'theater', 'movies',
    'concerts', 'music', 'shopping', 'yoga', 'exphappy', 'expnum',
    'match_es', 'length'
]
percentage = {
    'age': 80, 'field': 50, 'undergra': 50, 'tuiton': 40, 'race': 40,
    'imprace': 30, 'imprelig': 30, 'from': 60, 'zipcode': 15, 'income': 45,
    'goal': 30, 'date': 30, 'go_out': 40, 'career': 45, 'sports': 30,
    'tvsports': 30, 'excersice': 35, 'dining': 50, 'museums': 30, 'art': 55,
    'hiking': 30, 'gaming': 30, 'clubbing': 30, 'reading': 30, 'tv': 30,
    'theater': 40, 'movies': 45, 'concerts': 35, 'music': 60, 'shopping': 35,
    'yoga': 30, 'exphappy': 30, 'expnum': 30, 'match_es': 30, 'match': 30,
    'length': 45
}
seuil = 200

def toInt(s):
    try:
        ret = int(s)
        return ret
    except ValueError:
        return s

def getLinkStrength(elem, candidate):
    strength = 0
    if elem['gender'] == candidate['gender']:
        return 0
    shared_items = set(elem.items()) & set(candidate.items())
    for key, val in shared_items:
        if val and key and key != "id":
            strength += int(percentage[key])
    return strength

def createGraph(data):
    graph = []
    for elem in data:
        graph.append({
            'elem': elem,
            'links': []
        })
    for node in graph:
        for candidate in data:
            strength = getLinkStrength(elem, candidate)
            if candidate != node['elem'] and strength > seuil:
                # print str(candidate['id']) + ':' + str(node['elem']['id'])
                node['links'].append({
                    'elem': candidate,
                    'strength': strength
                })
    return graph

def encodeFrom(value):
    if not value in from_cd.keys():
        from_cd[value] = len(from_cd)
    return from_cd[value]

def encodeUndergra(value):
    if not value in undergra_cd.keys():
        undergra_cd[value] = len(undergra_cd)
    return undergra_cd[value]

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

def normalizeMatch(value):
    if value > 0 and value < 2:
        return 1
    elif value < 4:
        return 2
    return 3

def normalizeMatchEs(value):
    if value > 0 and value < 2:
        return 1
    elif value < 4:
        return 2
    return 3

def setId(value):
    return global_id

vars_treatment = {
    'from': encodeFrom,
    'id': setId,
    'income': normalizeIncome,
    'match': normalizeMatch,
    'match_es': normalizeMatchEs,
    'zipcode': encodeZip,
    "field": encodeField,
    "undergra": encodeUndergra,
    "career": encodeCareer
}

def getJmp():
    with open('data.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        jmp = (sum(1 for line in reader) - 1) / 500
        csvfile.close()
    return jmp

def getIndexes(row):
    j = 0
    keys = []
    indexes = []
    global global_id

    for key in row:
        if any(key in elem for elem in use):
            indexes.append(j)
        keys.append(key)
        j += 1
    global_id += 1
    return indexes, keys

def readFile():
    data = []

    i = 0
    jmp = getJmp()
    global global_id
    with open('data.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            row = row[:-1]
            if global_id == 0:
                indexes, keys = getIndexes(row)
            elif float(i) % jmp == 0:
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
            i += 1
    return data
