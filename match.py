from build_graph import *
import csv

csv_file = None
writer = None

# def link_force(graph, person, link):
#     match_with_elem = [elem for elem in link["node"]["links"] if elem["node"]["elem"]["id"] == person["elem"]["id"]][0]
#     return (match_with_elem["strength"] + link["strength"]) / 2, link["node"]["elem"]["id"]
#
# def matching(graph):
#     for person in graph:
#         link_forces = []
#         for link in person["links"]:
#             matching_strength, matching_id = link_force(graph, person, link)
#             link_forces.append({'strength': matching_strength, 'id': matching_id})
#             link_forces = sorted(link_forces, key=lambda person:person['strength'], reverse=True)
#         best_links = ""
#         for index, link_to_write in enumerate(link_forces):
#             if index == 5:
#                 break
#             if best_links:
#                 best_links = best_links + "," + str(link_to_write["id"])
#             else:
#                 best_links = str(link_to_write["id"])
#         with open('result.csv', 'a') as csvfile:
#             spamwriter = csv.writer(csvfile, delimiter=' ',
#                                     quotechar='|', quoting=csv.QUOTE_MINIMAL)
#             spamwriter.writerow([person["elem"]["id"], ";", best_links])

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
                if node['elem']['id'] == link2['node']['elem']['id']:
                    final_links.append(link)
    if len(final_links) < 5:
        for link3 in node['links']:
            if link3 not in final_links and len(final_links) < 5:
                final_links.append(link3)

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
