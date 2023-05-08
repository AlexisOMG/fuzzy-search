from typing import Callable, Optional, List, Tuple, Dict, Hashable, Any
from dataclasses import dataclass, field

@dataclass
class Node:
  word: Dict[Hashable, Any]
  children: Dict[int, 'Node'] = field(default_factory=dict)

  def add_child(self, distance: int, child: 'Node') -> None:
    self.children[distance] = child


class BKTree:
  def __init__(self, distance_function: Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], int]):
    self.root = None
    self.distance_function = distance_function

  def insert(self, word: Dict[Hashable, Any]) -> None:
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

  def search(self, word: Dict[Hashable, Any], max_distance: int) -> List[Tuple[int, Dict[Hashable, Any]]]:
    if self.root is None:
      return []

    best_matches = []
    best_distance = max_distance or float('inf')
    nodes_to_visit = [(self.root, max_distance)]

    while nodes_to_visit:
      node, limit = nodes_to_visit.pop()
      distance = self.distance_function(word, node.word)

      # if distance < best_distance:
      #   best_matches.clear()
      #   best_distance = distance
      #   best_matches.append((node.word, best_distance))
      # el
      if distance <= max_distance:
        best_matches.append((distance, node.word))

      for edge_distance, child in node.children.items():
        if abs(edge_distance - distance) <= max_distance:
          nodes_to_visit.append((child, max_distance))

    return best_matches