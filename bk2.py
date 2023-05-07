from typing import Callable, Optional, List, Tuple, Dict
from dataclasses import dataclass, field

from distances.levenshtein import levenshtein_distance_memopt

@dataclass
class Node:
  word: str
  children: Dict[int, 'Node'] = field(default_factory=dict)

  def add_child(self, distance: int, child: 'Node') -> None:
    self.children[distance] = child


class BKTree:
  def __init__(self, distance_function: Callable[[str, str], int]):
    self.root = None
    self.distance_function = distance_function

  def insert(self, word: str) -> None:
    if self.root is None:
      self.root = Node(word)
      return

    node = self.root
    while node:
      distance = self.distance_function(word, node.word)
      if distance == 0:
        return
      child = node.children.get(distance)
      if child is None:
        node.add_child(distance, Node(word))
        return
      node = child

  def search(self, word: str, max_distance: Optional[int] = None) -> List[Tuple[str, int]]:
    if self.root is None:
      return []

    best_matches = []
    best_distance = max_distance or float('inf')
    nodes_to_visit = [(self.root, best_distance)]

    while nodes_to_visit:
      node, limit = nodes_to_visit.pop()
      distance = self.distance_function(word, node.word)

      if distance < best_distance:
        best_matches.clear()
        best_distance = distance
        best_matches.append((node.word, best_distance))
      elif distance == best_distance:
        best_matches.append((node.word, best_distance))

      for edge_distance, child in node.children.items():
        if abs(edge_distance - distance) <= best_distance:
          nodes_to_visit.append((child, limit))

    return best_matches


bk_tree = BKTree(levenshtein_distance_memopt)

words = ["apple", "banana", "orange", "grape", "watermelon", "pineapple"]
tree = BKTree(levenshtein_distance_memopt)
for word in words:
    tree.insert(word)

query_word = "appla"
max_distance = 4

for word in words:
    distance = levenshtein_distance_memopt(query_word, word)
    print(f"Distance between '{query_word}' and '{word}': {distance}")

results = tree.search(query_word, max_distance)
print(f"Words within {max_distance} edit distance from '{query_word}':")
for word, distance in results:
    print(f"{word} (distance: {distance})")