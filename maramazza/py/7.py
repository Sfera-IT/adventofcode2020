import re
from collections import defaultdict

def dfs(graph, visited, source_vertex):
    visited[source_vertex] = True
    neighbors = graph[source_vertex]
    # print(neighbors)
    # return False
    for neighbor in neighbors:
        if not visited[neighbor[1]]:
            dfs(graph, visited, neighbor[1])

def res_part_1(graph):
    visited = defaultdict(bool) 
    dfs(graph, visited, 'shiny gold')
    return len(visited.keys()) - 1

def countBag(graph, source_vertex):
    neighbors = graph[source_vertex[1]]
    count = 0
    for neighbor in neighbors:
        count += neighbor[0] * (1 + countBag(graph, neighbor))
    return count

def res_part_2(graph):
    return countBag(graph, (0, 'shiny gold'))

def parse_values(data):
    contained_in_graph = defaultdict(list)
    contains_graph = defaultdict(list)
    pattern = re.compile(r"(.+) bags contain (.+)")
    for line in data:
        match = pattern.match(line)
        parent = match.group(1)
        others = match.group(2)
        children = re.findall(r'(\d+) (.+?) bags?', others)
        for count, child_bag_name in children:
            contained_in_graph[child_bag_name].append((count, parent))
            contains_graph[parent].append((int(count), child_bag_name))
    return contained_in_graph, contains_graph

if __name__ == '__main__':
    with open('./../data/7.txt') as f:
        values = f.read().splitlines()
        contained_in_graph, contains_graph = parse_values(values)
        result1 = res_part_1(contained_in_graph)
        print(result1)
        result2 = res_part_2(contains_graph)
        print(result2)
