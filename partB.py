import urllib.request
from collections import defaultdict, deque, Counter
import sys
sys.setrecursionlimit(10000)

def load_words():
    url = "http://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt"
    response = urllib.request.urlopen(url)
    lines = response.read().decode("utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]

# --- Kiểm tra điều kiện tạo cạnh có hướng u -> v ---
def can_link(u, v):
    last4 = u[-4:]
    count_last4 = Counter(last4)
    count_v = Counter(v)
    for char in count_last4:
        if count_last4[char] > count_v.get(char, 0):
            return False
    return True

def build_directed_graph(words):
    graph = defaultdict(list)
    for u in words:
        for v in words:
            if u != v and can_link(u, v):
                graph[u].append(v)
    return graph

def dfs1(node, graph, visited, stack):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs1(neighbor, graph, visited, stack)
    stack.append(node)
def dfs2(node, reversed_graph, visited, component):
    visited.add(node)
    component.append(node)
    for neighbor in reversed_graph[node]:
        if neighbor not in visited:
            dfs2(neighbor, reversed_graph, visited, component)

def kosaraju_scc(graph):
    visited = set()
    stack = []
    for node in list(graph.keys()):
        if node not in visited:
            dfs1(node, graph, visited, stack)

    reversed_graph = defaultdict(list)
    for u in graph:
        for v in graph[u]:
            reversed_graph[v].append(u)

    visited.clear()
    sccs = []
    while stack:
        node = stack.pop()
        if node not in visited:
            component = []
            dfs2(node, reversed_graph, visited, component)
            sccs.append(component)
    return sccs

def shortest_directed_path(graph, start, end):
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
    return path[::-1]

if __name__ == "__main__":
    print("Đang tải từ...")
    words = load_words()

    print("Đang xây dựng đồ thị có hướng...")
    G = build_directed_graph(words)

    print("Đang tìm thành phần liên thông mạnh (SCC)...")
    sccs = kosaraju_scc(G)
    print(f"Số SCCs tìm được: {len(sccs)}")

    word = input("Nhập từ để tìm SCC chứa nó: ").strip().lower()
    found = False
    for comp in sccs:
        if word in comp:
            print(f"Các từ trong SCC của '{word}':")
            print(", ".join(comp))
            found = True
            break
    if not found:
        print("Từ không nằm trong bất kỳ SCC nào!")

    u = input("Nhập từ bắt đầu: ").strip().lower()
    v = input("Nhập từ kết thúc: ").strip().lower()
    path = shortest_directed_path(G, u, v)
    if path:
        print("Đường đi ngắn nhất có hướng:")
        print(" → ".join(path))
    else:
        print("Không tìm được đường đi giữa hai từ.")
