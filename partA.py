import urllib.request
from collections import defaultdict, deque

def load_words():
    url = "http://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt"
    response = urllib.request.urlopen(url)
    lines = response.read().decode('utf-8').splitlines()
    words = [line.strip() for line in lines if line.strip()]
    return words

def differ_by_one(w1, w2):
    count = 0
    for a, b in zip(w1, w2):
        if a != b:
            count += 1
            if count > 1:
                return False
    return count == 1

def build_graph(words):
    graph = defaultdict(list)
    word_set = set(words)
    for word in words:
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c != word[i]:
                    new_word = word[:i] + c + word[i+1:]
                    if new_word in word_set:
                        graph[word].append(new_word)
    return graph

def count_connected_components(graph):
    visited = set()
    count = 0

    for node in graph:
        if node not in visited:
            count += 1
            queue = deque([node])
            visited.add(node)

            while queue:
                current = queue.popleft()
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
    return count

def shortest_path(graph, start, end):
    if start not in graph or end not in graph:
        return None
    
    queue = deque([start])
    parent = {start: None}
    visited = set([start])

    while queue:
        current = queue.popleft()
        if current == end:
            break
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    if end not in parent:
        return None
    
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path

if __name__ == "__main__":
    words = load_words()
    G = build_graph(words)
    
    # Example usage
    print("Number of connected components:", count_connected_components(G))
    
    u = input("start word: ").strip().lower()
    v = input("end word: ").strip().lower()
    path = shortest_path(G, u, v)
    
    if path:
        print(f"Shortest path from {u} to {v}: {' -> '.join(path)}")
    else:
        print(f"No path found from {u} to {v}.")