import requests
import httplib2
from bs4 import BeautifulSoup, SoupStrainer



def digger(dig_link):
    SiteAddress = 'http://it.wikipedia.org' + dig_link
    WebPage = requests.get(SiteAddress)

    http = httplib2.Http()
    status, response = http.request(SiteAddress)

    links = []
    for link in BeautifulSoup(response, features="html.parser", parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            links.append(link['href'])

    links = list(dict.fromkeys(links))
    updated_links = []
    for i in links:
        if i.startswith('/wiki/'):
            updated_links.append(i)
    return updated_links


visited = []  # List to keep track of visited nodes.
queue = []  # Initialize a queue


def shortest_path(graph, node1, node2):
    path_list = [[node1]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes = {node1}
    if node1 == node2:
        return len(path_list[0])

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = graph[last_node]
        # Search goal node
        if node2 in next_nodes:
            current_path.append(node2)
            return len(current_path)-1
        # Add new paths
        for next_node in next_nodes:
            if not next_node in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return 0


graph = {}
graph['/wiki/Birra'] = set(digger('/wiki/Birra'))
for i in graph['/wiki/Birra']:
    graph[i] = set(digger(i))
# for i in list(graph.keys())[1:50]:
#     graph[i] = set(digger(i))

print(shortest_path(graph, '/wiki/Birra', '/wiki/Petrolio'))

