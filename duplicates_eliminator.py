from typing import List, Tuple, Dict, Set, Hashable, Any
from copy import deepcopy

class DuplicatesEliminator:
  def __init__(self, data: List[Dict[Hashable, Any]]) -> None:
    self.data = deepcopy(data)
    self.cnt = 0

  def query(self, target: Dict[Hashable, Any], threshold: float = 0.85) -> List[Dict[Hashable, Any]]:
    raise NotImplementedError()
  
  def find_duplicates(self, threshold: float = 0.85) -> List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]]:
    raise NotImplementedError()
  
  def get_comparison_count(self) -> int:
    return self.cnt
  