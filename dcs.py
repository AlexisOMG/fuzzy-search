from typing import Callable, List, Set, Tuple, Dict, Optional
from collections import defaultdict
from jaro import jaro_winkler_distance
# from typing import Dict, List, Set, Tuple

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


def dcs_plus_plus(records: List[str], key: Callable[[str], str], w: int = 3, phi: Optional[float] = None) -> Set[Tuple[str, str]]:
  def is_duplicate(record1: str, record2: str) -> bool:
    # Реализуйте функцию для определения дубликатов
    return jaro_winkler_distance(record1, record2) > 0.9

  # def calculate_transitive_closure(duplicate_pairs: List[Tuple[str, str]]) -> Set[Tuple[str, str]]:
  #     # Реализуйте функцию для вычисления транзитивного замыкания
  #     pass

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

  transitive_closure: Set[Tuple[str, str]] = calculate_transitive_closure(duplicate_pairs)
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
  '25,Kevis,Scott,USA,38',
]

def get_key(record: str) -> str:
  return (record.split(','))[1]

print(dcs_plus_plus(test_records, get_key, w=6, phi=0.5))

