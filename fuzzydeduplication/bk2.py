from typing import Callable, Optional, List, Tuple, Dict, Hashable, Any
from dataclasses import dataclass, field
from uuid import uuid4

@dataclass
class Node:
  word: Dict[Hashable, Any]
  children: Dict[int, 'Node'] = field(default_factory=dict)
  id: str = field(default_factory=lambda: str(uuid4()))
  used: bool = False

  def add_child(self, distance: int, child: 'Node') -> None:
    self.children[distance] = child


class BKTree:
  def __init__(self, distance_function: Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], int]):
    self.root = None
    self.distance_function = distance_function
    self.all_nodes: Dict[str, Node] = {}
    self.cnt = 0

  def insert(self, word: Dict[Hashable, Any]) -> None:
    if self.root is None:
      self.root = Node(word)
      self.all_nodes[self.root.id] = self.root
      return

    node = self.root
    while node:
      distance = self.distance_function(word, node.word)
      if distance == 0:
        return
      child = node.children.get(distance)
      if child is None:
        node.add_child(distance, Node(word))
        self.all_nodes[node.id] = node
        self.all_nodes[node.children[distance].id] = node.children[distance]
        return
      node = child

  def search(self, word: Dict[Hashable, Any], max_distance: int) -> List[Tuple[int, Dict[Hashable, Any]]]:
    if self.root is None:
      return []
    
    self.cnt = 0

    best_matches = []
    best_distance = max_distance or float('inf')
    nodes_to_visit = [(self.root, max_distance)]

    while nodes_to_visit:
      node, limit = nodes_to_visit.pop()
      distance = self.distance_function(word, node.word)
      self.cnt += 1

      if distance <= max_distance:
        node.used = True
        best_matches.append((distance, node.word))

      for edge_distance, child in node.children.items():
        if abs(edge_distance - distance) <= max_distance:
          nodes_to_visit.append((child, max_distance))

    return best_matches
  
  def find_duplicates(self, max_distance: int) -> List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]]:
    res: List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]] = []
    for id in self.all_nodes:
      self.all_nodes[id].used = False

    cnt = 0

    for id in self.all_nodes:
      if self.all_nodes[id].used:
        continue
      
      tmp = self.search(self.all_nodes[id].word, max_distance)
      cnt += self.cnt
      # if len(tmp) > 1:
      for (d, w) in tmp:
        if d > 0:
          res.append((w, self.all_nodes[id].word))

    self.cnt = cnt

    return res
      