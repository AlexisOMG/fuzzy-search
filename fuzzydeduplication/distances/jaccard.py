from fuzzydeduplication.distances.similarity_metric import SimilarityMetric

def jaccard_similarity(set1: set, set2: set) -> float:
  intersection = set1.intersection(set2)
  union = set1.union(set2)
  if not union:
    return 0.0
  similarity = len(intersection) / len(union)
  return similarity

def jaccard_similarity_str(s1: str, s2: str) -> float:
  set_s1 = set(s1)
  set_s2 = set(s2)

  return jaccard_similarity(set_s1, set_s2)

class JaccardSimilarityMetric(SimilarityMetric):
  def similarity(self, s: str, t: str) -> float:
    return jaccard_similarity_str(s, t)
