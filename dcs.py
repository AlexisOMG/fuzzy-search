from typing import Callable, List, Set, Tuple, Dict, Optional, Hashable, Any
from collections import defaultdict
from copy import deepcopy
from uuid import uuid4

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

def dcs_plus_plus(data: List[Dict[Hashable, Any]], key: Callable[[Dict[Hashable, Any]], str], is_duplicate: Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], bool],w: int = 3, phi: Optional[float] = None) -> List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]]:
  records = deepcopy(data)
  records.sort(key=key)
  skip_records: Set[str] = set()
  duplicate_pairs: List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]] = []
  j = 0
  n = len(records)
  k = 0  # Инициализируем переменную k

  for i in range(n):
    records[i]['__unique_dcs_id__'] = str(uuid4())

  print([record['__unique_dcs_id__'] for record in records[:10]])

  win = records[:w]

  if win[0]['__unique_dcs_id__'] == win[1]['__unique_dcs_id__']:
    print('dhedhefgrh', k)

  if phi is None:
    phi = 1/(w-1)

  i = 0

  while i < len(records)-1:
    if win[0]['__unique_dcs_id__'] not in skip_records:
      num_duplicates = 0
      num_comparisons = 0
      j = 1
      while j < len(win):
        if is_duplicate(win[0], win[j]):
          duplicate_pairs.append((win[0], win[j]))
          skip_records.add(win[j]['__unique_dcs_id__'])
          num_duplicates += 1

          while len(win) < j + w and i + len(win) < len(records):
            win.append(records[i+len(win)])

        num_comparisons += 1
        if j == len(win) - 1 and i+j+1 < len(records) and (num_duplicates / num_comparisons) >= phi:
          win.append(records[i+j+1])
        
        j += 1

    win.pop(0)

    if len(win) < w and i + len(win) < len(records)-1:
      win.append(records[i+len(win)+1])
    else:
      while len(win) > w:
        win.pop()
    
    i += 1

  return duplicate_pairs
