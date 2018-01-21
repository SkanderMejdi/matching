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
imp = {
    'age': 84, 'field': 5, 'undergra': 5, 'tuiton': 4, 'race': 4,
    'imprace': 32, 'imprelig': 32, 'from': 6, 'zipcode': 1, 'income': 4,
    'goal': 3, 'date': 32, 'go_out': 43, 'career': 4, 'sports': 34,
    'tvsports': 32, 'excersice': 35, 'dining': 55, 'museums': 35, 'art': 55,
    'hiking': 36, 'gaming': 32, 'clubbing': 36, 'reading': 36, 'tv': 36,
    'theater': 41, 'movies': 41, 'concerts': 32, 'music': 62, 'shopping': 35,
    'yoga': 31, 'exphappy': 3, 'expnum': 3, 'match_es': 36, 'match': 36,
    'length': 4
}
seuil = 20

def checkInt(s):
    try:
        ret = int(s)
        return 1
    except ValueError:
        return 0

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
            if imp[key] > 10:
                diff = abs(elem[key] - candidate[key])
                if diff <= imp[key] % 10:
                    strength += int(abs(imp[key]) / 10)
            else:
                strength += imp[key]
    return strength

def linkToPercent(node, ratio):
    for link in node['links']:
        link['strength'] = ratio / 100 * link['strength']

def createLink(node, candidate, top, bottom, strength):
    node['links'].append({
        'elem': candidate,
        'strength': strength
    })
    if strength > top:
        top = strength
    if strength < bottom:
        bottom = strength
    return top, bottom

def createGraph(data):
    graph = []

    for elem in data:
        graph.append({
            'elem': elem,
            'links': []
        })
    for node in graph:
        bottom = 2800
        top = 0
        for candidate in data:
            strength = getLinkStrength(node['elem'], candidate)
            if candidate != node['elem'] and strength > seuil:
                top, bottom = createLink(node, candidate, top, bottom, strength)
        linkToPercent(node, top - bottom)
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
    # TODO: delete cut
    return data[:10]
