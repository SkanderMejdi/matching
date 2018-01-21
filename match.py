from build_graph import *
import csv

def link_force(graph, person, link):
    link_elem = [elem for elem in graph if elem["elem"]["id"] == link["elem"]["id"]][0]
    match_with_elem = [elem for elem in link_elem["links"] if elem["elem"]["id"] == person["elem"]["id"]][0]
    return (match_with_elem["strength"] + link["strength"]) / 2, link["elem"]["id"]

def matching(graph):
    for person in graph:
        link_forces = []
        for link in person["links"]:
            matching_strength, matching_id = link_force(graph, person, link)
            link_forces.append({'strength': matching_strength, 'id': matching_id})
            link_forces = sorted(link_forces, key=lambda person:person['strength'], reverse=True)
        best_links = ""
        for index, link_to_write in enumerate(link_forces):
            if index == 5:
                break
            if best_links:
                best_links = best_links + "," + str(link_to_write["id"])
            else:
                best_links = str(link_to_write["id"])
        with open('result.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([person["elem"]["id"], ";", best_links])

def deleteFileContent():
    with open('result.csv', 'w'):
        pass

def main():
    deleteFileContent()
    data = readFile()
    graph = createGraph(data)
    matching(graph)

main()
