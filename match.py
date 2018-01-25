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

def get_best_matchs(node):
    final_links = []
    for link in node['links']:
        if link['node']['sorted'] == 1:
            for link2 in link['node']['links']:
                if node['elem']['id'] == link2['node']['elem']['id'] and len(final_links) < 5:
                    final_links.append(link)

    for link in node['links']:
        if link['node']['sorted'] == 0 and len(final_links) < 5:
            final_links.append(link)

    final_links = sorted(
        final_links,
        key=lambda node: node['avg'],
        reverse=True
    )
    node['links'] = final_links
    return node

def matching(nodes):
    for node in nodes:
        for link1 in node['links']:
            if link1['avg'] == -1:
                for link2 in link1['node']['links']:
                    if node['elem']['id'] == link2['node']['elem']['id']:
                        avg = (link1['strength'] + link2['strength']) / 2
                        link1['avg'] = avg
                        link2['avg'] = avg
        node['links'] = sorted(
            node['links'],
            key=lambda node:node['avg'],
            reverse=True
        )
        node['sorted'] = 1
        node = get_best_matchs(node)
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
    matching(graph)
    csv_file.close()

main()
