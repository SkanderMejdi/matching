from build_graph import *
import csv

csv_file = None
writer = None

def writeFile(node):
    write = ''
    global writer

    for link in node['links']:
        if write == '':
            write += str(link['node']['elem']['id'])
        else:
            write += ',' + str(link['node']['elem']['id'])
    writer.writerow([
        node['elem']['id'],
        ":",
        ','.join([
            str(link['node']['elem']['id'])
            for link in node['links']
        ])
    ])

def matching(node):
    final_links = []
    for link in node['links']:
        if link['node']['sorted'] == 1:
            for link2 in link['node']['links']:
                if node['elem']['id'] == link2['node']['elem']['id'] and len(final_links) < 5:
                    final_links.append(link)

    if len(final_links) < 5:
        for link3 in node['links']:
            if link3 not in final_links and len(final_links) < 5:
                final_links.append(link3)
                if node['elem']['id'] not in (link4['node']['elem']['id'] for link4 in link3['node']['links']):
                    link3['node']['links'].append({
                        'node': node,
                        'strength': 0,
                        'avg': -1
                    })

    final_links = sorted(
        final_links,
        key=lambda node: node['avg'],
        reverse=True
    )
    node['links'] = final_links
    return node

def processGraph(nodes):
    for node in nodes:
        for link in node['links']:
            if link['avg'] == -1:
                for link2 in link['node']['links']:
                    if node['elem']['id'] == link2['node']['elem']['id']:
                        avg = (link['strength'] + link2['strength']) / 2
                        link['avg'] = avg
                        link2['avg'] = avg
        node['links'] = sorted(
            node['links'],
            key=lambda node:node['avg'],
            reverse=True
        )
        node['sorted'] = 1
        node = matching(node)

    for node in nodes:
        writeFile(node)

def openFile():
    global csv_file
    global writer

    csv_file = open('result.csv', 'w')
    writer = csv.writer(
        csv_file,
        delimiter=' ',
        quotechar='|',
        quoting=csv.QUOTE_MINIMAL
    )

def main():
    global csv_file

    openFile()
    data = readFile()
    nodes = createGraph(data)
    processGraph(graph)
    csv_file.close()

main()
