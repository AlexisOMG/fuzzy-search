from typing import List, Tuple, Callable, Dict, Optional, Hashable, Any
from distances.levenshtein import levenshtein_distance_memopt

class BKTreeNode:
  def __init__(self, value: Dict[Hashable, Any]):
    self.value: Dict[Hashable, Any] = value
    self.children: Dict[int, BKTreeNode] = {}

  def insert(self, value: Dict[Hashable, Any], distance_func: Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], int]):
    distance = distance_func(self.value, value)
    if distance in self.children:
      self.children[distance].insert(value, distance_func)
    else:
      self.children[distance] = BKTreeNode(value)

  def query(self, value: Dict[Hashable, Any], max_distance: int, distance_func: Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], int]) -> List[Tuple[int, Dict[Hashable, Any]]]:
    results: List[Tuple[int, Dict[Hashable, Any]]] = []

    distance_to_value = distance_func(self.value, value)
    if distance_to_value <= max_distance:
      results.append((distance_to_value, self.value))

    for i in range(distance_to_value - max_distance, distance_to_value + max_distance + 1):
      child = self.children.get(i)
      if child:
        results.extend(child.query(value, max_distance, distance_func))

    return results


class BKTree:
  def __init__(self, distance_func: Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], int]):
    self.root: Optional[BKTreeNode] = None
    self.distance_func = distance_func

  def insert(self, value: Dict[Hashable, Any]):
    if not self.root:
      self.root = BKTreeNode(value)
    else:
      self.root.insert(value, self.distance_func)

  def query(self, value: Dict[Hashable, Any], max_distance: int) -> List[Tuple[int, Dict[Hashable, Any]]]:
    if not self.root:
      return []
    return self.root.query(value, max_distance, self.distance_func)
