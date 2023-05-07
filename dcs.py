from typing import Callable, List, Set, Tuple, Dict, Optional
from collections import defaultdict
from distances.jaro import jaro_winkler_similarity
from distances.levenshtein import levenshtein_distance_memopt
# from typing import Dict, List, Set, Tuple

# def calculate_transitive_closure(duplicate_pairs: List[Tuple[str, str]]) -> List[Set[str]]:
#     class UnionFind:
#         def __init__(self):
#             self.parent: Dict[str, str] = {}
#             self.rank: Dict[str, int] = {}

#         def find(self, item: str) -> str:
#             if item not in self.parent:
#                 self.parent[item] = item
#                 self.rank[item] = 0
#             elif self.parent[item] != item:
#                 self.parent[item] = self.find(self.parent[item])
#             return self.parent[item]

#         def union(self, item1: str, item2: str) -> None:
#             root1 = self.find(item1)
#             root2 = self.find(item2)

#             if root1 == root2:
#                 return

#             if self.rank[root1] > self.rank[root2]:
#                 self.parent[root2] = root1
#             else:
#                 self.parent[root1] = root2
#                 if self.rank[root1] == self.rank[root2]:
#                     self.rank[root2] += 1

#     uf = UnionFind()

#     for item1, item2 in duplicate_pairs:
#         uf.union(item1, item2)

#     groups: Dict[str, Set[str]] = {}

#     for item1, item2 in duplicate_pairs:
#         root1 = uf.find(item1)
#         root2 = uf.find(item2)

#         if root1 != root2:
#             if root1 not in groups:
#                 groups[root1] = {item1}
#             groups[root1].add(item2)

#             if root2 not in groups:
#                 groups[root2] = {item2}
#             groups[root2].add(item1)

#     return list(groups.values())

def calculate_transitive_closure(duplicate_pairs: List[Tuple[str, str]]) -> Set[Tuple[str, str]]:
  def dfs(node: str, graph: Dict[str, List[str]], visited: Set[str]) -> Set[str]:
    visited.add(node)
    connected_nodes = {node}

    for neighbor in graph[node]:
      if neighbor not in visited:
        connected_nodes |= dfs(neighbor, graph, visited)

    return connected_nodes

  graph = defaultdict(list)

  for item1, item2 in duplicate_pairs:
    graph[item1].append(item2)
    graph[item2].append(item1)

  visited = set()
  transitive_closure: Set[Tuple[str, str]] = set()

  for node in graph:
    if node not in visited:
      connected_nodes = dfs(node, graph, visited)
      for item1, item2 in zip(connected_nodes, list(connected_nodes)[1:]):
        transitive_closure.add((item1, item2))

  return transitive_closure

# def calculate_transitive_closure(duplicate_pairs: List[Tuple[str, str]]) -> Set[Tuple[str, str]]:
#     class UnionFind:
#         def __init__(self):
#             self.parent: Dict[str, str] = {}
#             self.rank: Dict[str, int] = {}

#         def find(self, item: str) -> str:
#             if item not in self.parent:
#                 self.parent[item] = item
#                 self.rank[item] = 0
#             elif self.parent[item] != item:
#                 self.parent[item] = self.find(self.parent[item])
#             return self.parent[item]

#         def union(self, item1: str, item2: str) -> None:
#             root1 = self.find(item1)
#             root2 = self.find(item2)

#             if root1 == root2:
#                 return

#             if self.rank[root1] > self.rank[root2]:
#                 self.parent[root2] = root1
#             else:
#                 self.parent[root1] = root2
#                 if self.rank[root1] == self.rank[root2]:
#                     self.rank[root2] += 1

#     uf = UnionFind()

#     for item1, item2 in duplicate_pairs:
#         uf.union(item1, item2)

#     transitive_closure: Set[Tuple[str, str]] = set()

#     for item1, item2 in duplicate_pairs:
#         root1 = uf.find(item1)
#         root2 = uf.find(item2)
#         if root1 != root2:
#             transitive_closure.add((root1, root2))

#     return transitive_closure

# def calculate_transitive_closure(duplicate_pairs: List[Tuple[str, str]]) -> List[Set[str]]:
#     def dfs(node: str, graph: Dict[str, List[str]], visited: Set[str]) -> Set[str]:
#         visited.add(node)
#         connected_nodes = {node}

#         for neighbor in graph[node]:
#             if neighbor not in visited:
#                 connected_nodes |= dfs(neighbor, graph, visited)

#         return connected_nodes

#     graph = defaultdict(list)

#     for item1, item2 in duplicate_pairs:
#         graph[item1].append(item2)
#         graph[item2].append(item1)

#     visited = set()
#     transitive_closure: List[Set[str]] = []

#     for node in graph:
#         if node not in visited:
#             connected_nodes = dfs(node, graph, visited)
#             transitive_closure.append(connected_nodes)

#     return transitive_closure

def calculate_transitive_closure_warshall(duplicate_pairs: List[Tuple[str, str]]) -> List[Set[str]]:
  vertices = set()
  for pair in duplicate_pairs:
    vertices.add(pair[0])
    vertices.add(pair[1])

  vertices = sorted(list(vertices))
  vertex_count = len(vertices)
  vertex_indices = {vertex: index for index, vertex in enumerate(vertices)}

  adjacency_matrix = [[0] * vertex_count for _ in range(vertex_count)]

  for item1, item2 in duplicate_pairs:
    adjacency_matrix[vertex_indices[item1]][vertex_indices[item2]] = 1
    adjacency_matrix[vertex_indices[item2]][vertex_indices[item1]] = 1

  for k in range(vertex_count):
    for i in range(vertex_count):
      for j in range(vertex_count):
        adjacency_matrix[i][j] = adjacency_matrix[i][j] or (adjacency_matrix[i][k] and adjacency_matrix[k][j])

  groups: List[Set[str]] = []
  visited = set()

  for i in range(vertex_count):
    if i not in visited:
      group = set()
      for j in range(vertex_count):
        if adjacency_matrix[i][j]:
          group.add(vertices[j])
          visited.add(j)
      groups.append(group)

  return groups


def dcs_plus_plus(records: List[str], key: Callable[[str], str], w: int = 3, phi: Optional[float] = None) -> Set[Tuple[str, str]]:
  def is_duplicate(record1: str, record2: str) -> bool:
    # Реализуйте функцию для определения дубликатов
    return jaro_winkler_similarity(record1, record2) > 0.9

  records.sort(key=key)
  win = records[:w]
  skip_records: Set[str] = set()
  duplicate_pairs: List[Tuple[str, str]] = []
  j = 1
  n = len(records)
  k = 0  # Инициализируем переменную k

  if phi is None:
    phi = 1/(w-1)

  while j < n:
    if win[0] not in skip_records:
      num_duplicates = 0
      num_comparisons = 0
      k = 1

      while k < len(win):
        if is_duplicate(win[0], win[k]):
          duplicate_pairs.append((win[0], win[k]))
          skip_records.add(win[k])
          num_duplicates += 1

          while len(win) < k + w - 1 and j + len(win) < n:
            win.append(records[j + len(win)])

        num_comparisons += 1

        if k == len(win) - 1 and j + k < n and (num_duplicates / num_comparisons) >= phi:
          win.append(records[j + k])

        k += 1

    win.pop(0)

    if len(win) < w and j + k < n:
      win.append(records[j + k])
    else:
      while len(win) > w:
        win.pop()

    j += 1

  transitive_closure: Set[Tuple[str, str]] = calculate_transitive_closure_warshall(duplicate_pairs)
  return transitive_closure

test_records = [
  '0,Kevis,Scott,USA,38',
  '1,John,Smith,USA,25',
  '2,Robert,Williams,USA,34',
  '3,Michael,Jones,USA,56',
  '4,William,Brown,USA,19',
  '5,David,Davis,USA,29',
  '6,Richard,Miller,USA,45',
  '7,Charles,Wilson,USA,23',
  '8,Joseph,Moore,USA,37',
  '9,Thomas,Taylor,USA,51',
  '10,Christopher,Anderson,USA,47',
  '11,Daniel,Thomas,USA,21',
  '12,Paul,Jackson,USA,32',
  '13,Mark,White,USA,41',
  '14,Donald,Harris,USA,27',
  '15,George,Martin,USA,31',
  '16,Kenneth,Thompson,USA,35',
  '17,Steven,Robinson,USA,49',
  '18,Edward,Clark,USA,55',
  '19,Brian,Rodriguez,USA,39',
  '20,Ronald,Lewis,USA,43',
  '21,Brian,Rodriguez,USA,39',
  '22,Anthony,Walker,USA,33',
  '23,Kevin,Scott,USA,38',
  '24,Jason,Green,USA,22',
  '25,Kevis,Scot,USA,38',
]

def get_key(record: str) -> str:
  return (record.split(','))[1]

print(dcs_plus_plus(test_records, get_key, w=6, phi=0.5))

