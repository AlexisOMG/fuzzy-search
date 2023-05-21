from typing import Dict, Any, Hashable, List, Callable
from distances.similarity_metric import SimilarityMetric

from distances.levenshtein import LevenshteinMetric
from distances.damerau_levenstein import DamerauLevenshteinMetric
from distances.jaro import JaroWinklerMetric
from distances.jaccard import JaccardSimilarityMetric

def get_sim_mean(a: Dict[Hashable, Any], b: Dict[Hashable, Any], column_names: List[str], sim: SimilarityMetric) -> float:
  sm = 0
  cnt = 0
  for k in column_names:
    if a[k] is not None and b[k] is not None and isinstance(a[k], str) and a[k] != '' and isinstance(b[k], str) and b[k] != '':
      sm += sim.similarity(a[k], b[k])
      cnt += 1
  if cnt == 0:
    return 0
  return sm / cnt

def get_lev_sim(column_names: List[str]) -> Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], float]:
  return lambda a, b: get_sim_mean(a, b, column_names, LevenshteinMetric())
def get_dam_lev_sim(column_names: List[str]) -> Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], float]:
  return lambda a, b: get_sim_mean(a, b, column_names, DamerauLevenshteinMetric())
def get_jaro_sim(column_names: List[str]) -> Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], float]:
  return lambda a, b: get_sim_mean(a, b, column_names, JaroWinklerMetric())
def get_jaccard_sim(column_names: List[str]) -> Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], float]:
  return lambda a, b: get_sim_mean(a, b, column_names, JaccardSimilarityMetric())