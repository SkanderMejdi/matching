import csv

# Unique id
global_id = 0

# Array of nodes from graph
graph = []

# DICT FOR ENCODED FIELD

from_cd = {}
career_cd = {}
field_cd = {}
zip_cd = {}
undergra_cd = {}

# !DICT FOR ENCODED FIELD

# Used fields
use = [
    'id', 'gender', 'age', 'field', 'undergra', 'tuiton', 'race', 'imprace',
    'imprelig', 'from', 'zipcode', 'income', 'goal', 'date', 'go_out',
    'career', 'sports', 'tvsports', 'excersice', 'dining', 'museums', 'art',
    'hiking', 'gaming', 'clubbing', 'reading', 'tv', 'theater', 'movies',
    'concerts', 'music', 'shopping', 'yoga', 'exphappy', 'expnum',
    'match_es', 'length'
]

# Importance of each field for strenght calculation
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

# Minimum strenght for link creation
seuil = 25

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

# Get link strenght between to nodes
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

# Calculate percentages with top and bottom strenght of links
def linkToPercent(node, ratio, bottom):
    for link in node['links']:
        save = link['strength']
        if ratio == 0:
            link['strength'] = 100
        else:
            link['strength'] =  100 / ratio * (link['strength'] - bottom)

# Create link between to nodes
# Update top and bottom strength link for the node
def createLink(node, candidate, top, bottom, strength):
    for i in graph:
        if candidate['id'] == i['elem']['id']:
            candidateNode = i
            break
    node['links'].append({
        'node': candidateNode,
        'strength': strength,
        'avg': -1
    })
    if strength > top:
        top = strength
    if strength < bottom:
        bottom = strength
    return top, bottom

# Create graph from array of data and return an array of nodes
# Trigger strength calculation to create or not a link
def createGraph(data):
    for elem in data:
        graph.append({
            'elem': elem,
            'links': [],
            'sorted': 0
        })
    for node in graph:
        bottom = 2800
        top = 0
        i = 0
        for candidate in data:
            strength = getLinkStrength(node['elem'], candidate)
            if candidate != node['elem'] and strength > seuil:
                top, bottom = createLink(node, candidate, top, bottom, strength)
        linkToPercent(node, top - bottom, bottom)
    return graph

# METHODS FOR VARS ENCODING NORMALIZING

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

# !METHODS FOR VARS ENCODING NORMALIZING

# Association of field with encoding/normalizing function
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

# Count lines in dataset and determine jump to extract @max_lines lines
def getJmp(max_lines):
    with open('data.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        jmp = (sum(1 for line in reader) - 1) / max_lines
        csvfile.close()
    return jmp

# Get indexes of used field
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

# Read file and get a formatted array
def readFile():
    i = 0
    data = []
    jmp = getJmp(500)

    global global_id
    with open('data.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            row = row[:-1]
            if global_id == 0:
                indexes, keys = getIndexes(row)
            elif float(i) % jmp == 0:
                empty = 0
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
                    if row[j] == '':
                        empty += 1
                if empty > 10:
                    data = data[:-1]
                else:
                    global_id += 1
            i += 1
    csvfile.close()
    return data
